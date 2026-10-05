/**
 * In-browser Kociemba two-phase solver, wrapping the vendored cubejs
 * (`src/vendor/cubejs`).
 *
 * This is the solver logic itself, with no knowledge of Web Workers, so it can
 * be unit tested directly. `solver.worker.ts` runs it off the main thread and
 * `solverClient.ts` is what UI code talks to.
 *
 * Usage notes:
 * - `prepareSolver()` builds the two-phase tables (about a second of blocking
 *   work). `solveCube()` calls it automatically, but calling it early hides
 *   the delay.
 * - Solutions are in standard face-turn notation (`R`, `U'`, `F2`) and assume
 *   the cube is held white-up, green-front. They are typically 20–22 moves.
 */
import Cube from '../vendor/cubejs/index.js'
import type { CubeState } from '../types'
import { findCubeProblems, toFaceletString } from '../utils/cubeValidation'
import { isSolved } from '../utils/isSolved'
import { parseMoves } from '../utils/cubeMoves'

/** Longest solution the search will look for. cubejs's own default. */
const MAX_SOLUTION_LENGTH = 22

/** Whether the two-phase tables have been built in this thread. */
let tablesReady = false

/** Thrown when a cube can't be solved because it was entered incorrectly. */
export class UnsolvableCubeError extends Error {
    /** The problems found, each written for the user. */
    readonly problems: string[]

    /**
     * @param problems - Problem messages from `findCubeProblems()`. Must not be empty.
     */
    constructor(problems: string[]) {
        super(problems.join(' '))
        this.name = 'UnsolvableCubeError'
        this.problems = problems
    }
}

/**
 * Build the solver's move and pruning tables if they haven't been built yet.
 *
 * Blocks the calling thread for about a second the first time; later calls
 * return immediately.
 */
export function prepareSolver(): void {
    if (tablesReady) return
    Cube.initSolver()
    tablesReady = true
}

/**
 * Solve a cube with Kociemba's two-phase algorithm.
 *
 * @param state - A complete cube in the standard orientation (white center on
 *   top, green center in front), such as one entered in Solve mode.
 * @returns The solution as a list of moves; empty if the cube is already solved.
 * @throws {UnsolvableCubeError} If the cube can't exist on a real puzzle.
 * @throws {Error} If the search fails to find a solution (should not happen
 *   for a validated cube).
 */
export function solveCube(state: CubeState): string[] {
    const problems = findCubeProblems(state)
    if (problems.length > 0) throw new UnsolvableCubeError(problems)

    // cubejs returns a non-empty (identity) sequence for a solved cube.
    if (isSolved(state)) return []

    prepareSolver()
    const solution = Cube.fromString(toFaceletString(state)).solve(MAX_SOLUTION_LENGTH)
    if (!solution) {
        throw new Error('The solver did not find a solution within its move limit')
    }
    return parseMoves(solution)
}
