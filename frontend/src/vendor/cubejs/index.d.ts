/**
 * Type declarations for the vendored cubejs (`index.js`), which ships without
 * types.
 *
 * Only the part of the API this app uses is declared. The signatures were
 * taken from the source (`cube.js` and `solve.js` in this directory, v1.3.2)
 * rather than from documentation, so if the vendored copy is updated, re-check
 * them there.
 *
 * Usage notes:
 * - `Cube.initSolver()` must run once before `solve()`. It builds the
 *   two-phase move and pruning tables, which takes about a second and blocks
 *   the thread it runs on, so call it from a Web Worker.
 * - `solve()` does no validation. An impossible cube (twisted corner, flipped
 *   edge, swapped pair) makes the search run until it exhausts its depth limit,
 *   which can take a very long time. Validate first.
 */
/** A 3x3x3 cube in cubie representation (permutation + orientation). */
export default class Cube {
    /** Create a solved cube. */
    constructor()

    /**
     * Build a cube from a 54-character facelet string in Kociemba's
     * `URFDLB` order.
     *
     * @param facelets - The facelet string; each character is a face letter.
     * @returns The cube those facelets describe.
     */
    static fromString(facelets: string): Cube

    /** Precompute the move and pruning tables the solver needs. */
    static initSolver(): void

    /**
     * Find a solution with Kociemba's two-phase algorithm.
     *
     * @param maxDepth - Maximum solution length to search for (default 22).
     * @returns The solution as space-separated standard notation
     *   (`"R U2 F'"`). Not empty for a solved cube: see `isSolved()`.
     */
    solve(maxDepth?: number): string

    /**
     * Apply a move sequence in place.
     *
     * @param moves - Moves in standard notation.
     * @returns This cube, for chaining.
     */
    move(moves: string): Cube

    /** @returns Whether every piece is in its home position and orientation. */
    isSolved(): boolean

    /** @returns The cube as a 54-character facelet string. */
    asString(): string
}
