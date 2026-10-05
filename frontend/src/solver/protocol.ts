/**
 * Message types exchanged between `solverClient.ts` and `solver.worker.ts`.
 *
 * Every request carries an `id` that its response echoes back, so the client
 * can match responses to the promises waiting on them.
 */
import type { CubeState } from '../types'

/** Ask the worker to build the solver tables ahead of the first solve. */
export interface PrepareRequest {
    id: number
    type: 'prepare'
}

/** Ask the worker to solve a cube. */
export interface SolveRequest {
    id: number
    type: 'solve'
    state: CubeState
}

/** Anything the client can send to the worker. */
export type SolverRequest = PrepareRequest | SolveRequest

/** The request succeeded. `moves` is set for solve requests. */
export interface SolverSuccess {
    id: number
    ok: true
    moves: string[]
}

/** The request failed. */
export interface SolverFailure {
    id: number
    ok: false
    /** A summary of what went wrong. */
    error: string
    /** Set when the cube itself is impossible: one message per problem, written for the user. */
    problems?: string[]
}

/** Anything the worker can send back. */
export type SolverResponse = SolverSuccess | SolverFailure
