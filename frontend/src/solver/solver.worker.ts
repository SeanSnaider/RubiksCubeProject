/**
 * Web Worker that runs the Kociemba solver off the main thread.
 *
 * Building the solver tables blocks for about a second, and a solve can take
 * a few hundred milliseconds. Doing either on the main thread would freeze the
 * page, so this worker owns the solver and answers requests from
 * `solverClient.ts` (see `protocol.ts` for the message shapes).
 *
 * Usage note: don't import this file directly. The client creates it with
 * `new Worker(new URL('./solver.worker.ts', import.meta.url))` so Vite bundles
 * it as a separate worker script.
 */
import { prepareSolver, solveCube, UnsolvableCubeError } from './kociembaSolver'
import type { SolverRequest, SolverResponse } from './protocol'

/**
 * Handle one request and build its response.
 *
 * @param request - The request from the client.
 * @returns The response to send back; failures are reported, never thrown.
 */
function handleRequest(request: SolverRequest): SolverResponse {
    try {
        if (request.type === 'prepare') {
            prepareSolver()
            return { id: request.id, ok: true, moves: [] }
        }
        return { id: request.id, ok: true, moves: solveCube(request.state) }
    } catch (error) {
        if (error instanceof UnsolvableCubeError) {
            return { id: request.id, ok: false, error: error.message, problems: error.problems }
        }
        const message = error instanceof Error ? error.message : String(error)
        return { id: request.id, ok: false, error: message }
    }
}

self.addEventListener('message', (event: MessageEvent<SolverRequest>) => {
    self.postMessage(handleRequest(event.data))
})
