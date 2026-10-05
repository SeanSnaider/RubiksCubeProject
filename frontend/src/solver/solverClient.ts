/**
 * Promise-based front door to the solver Web Worker.
 *
 * UI code calls `prepareSolver()` and `solveCube()` from here and never sees
 * the worker. A single worker is created lazily on first use and kept for the
 * life of the page, so its tables are only built once however often the user
 * switches tabs.
 *
 * Usage notes:
 * - `solveCube()` rejects with `CubeProblemsError` when the cube is
 *   impossible; its `problems` are ready to show to the user. Any other
 *   rejection is an unexpected failure of the solver itself.
 */
import type { CubeState } from '../types'
import type { SolverRequest, SolverResponse } from './protocol'

/** Distributive omit, so each member of a request union keeps its own fields. */
type WithoutId<T> = T extends unknown ? Omit<T, 'id'> : never

/** Raised in the UI thread when the worker reports the cube is impossible. */
export class CubeProblemsError extends Error {
    /** One message per problem, written for the user. */
    readonly problems: string[]

    /**
     * @param problems - The problems the worker found. Must not be empty.
     */
    constructor(problems: string[]) {
        super(problems.join(' '))
        this.name = 'CubeProblemsError'
        this.problems = problems
    }
}

/** A request that has been sent and is waiting for its response. */
interface PendingRequest {
    resolve: (moves: string[]) => void
    reject: (error: Error) => void
}

/** The shared worker, created on first use. */
let worker: Worker | null = null
/** Requests awaiting a response, by id. */
const pending = new Map<number, PendingRequest>()
/** The id for the next request. */
let nextId = 1

/**
 * Fail every waiting request and drop the worker so the next call starts a
 * fresh one.
 *
 * @param error - The error to reject each waiting request with.
 */
function failAll(error: Error): void {
    for (const request of pending.values()) request.reject(error)
    pending.clear()
    worker?.terminate()
    worker = null
}

/**
 * Get the shared worker, starting it if needed.
 *
 * @returns The running worker.
 */
function getWorker(): Worker {
    if (worker) return worker
    const created = new Worker(new URL('./solver.worker.ts', import.meta.url), { type: 'module' })
    created.addEventListener('message', (event: MessageEvent<SolverResponse>) => {
        const response = event.data
        const request = pending.get(response.id)
        if (!request) return
        pending.delete(response.id)
        if (response.ok) {
            request.resolve(response.moves)
        } else if (response.problems && response.problems.length > 0) {
            request.reject(new CubeProblemsError(response.problems))
        } else {
            request.reject(new Error(response.error))
        }
    })
    created.addEventListener('error', (event: ErrorEvent) => {
        failAll(new Error(`The solver stopped unexpectedly: ${event.message || 'unknown error'}`))
    })
    worker = created
    return created
}

/**
 * Send a request to the worker.
 *
 * @param request - The request, without its id (one is assigned here).
 * @returns The moves from a successful response.
 */
function send(request: WithoutId<SolverRequest>): Promise<string[]> {
    const id = nextId++
    return new Promise((resolve, reject) => {
        pending.set(id, { resolve, reject })
        getWorker().postMessage({ ...request, id } as SolverRequest)
    })
}

/**
 * Build the solver tables in the background, so the first solve is quick.
 *
 * Safe to call repeatedly; the worker only builds the tables once.
 *
 * @returns Resolves when the solver is ready.
 */
export async function prepareSolver(): Promise<void> {
    await send({ type: 'prepare' })
}

/**
 * Solve a cube in the background with Kociemba's two-phase algorithm.
 *
 * @param state - A complete cube held white-up, green-front.
 * @returns The solution moves in standard notation; empty if already solved.
 * @throws {CubeProblemsError} If the cube is impossible as entered.
 * @throws {Error} If the solver fails for any other reason.
 */
export function solveCube(state: CubeState): Promise<string[]> {
    return send({ type: 'solve', state })
}
