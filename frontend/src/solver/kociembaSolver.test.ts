/**
 * Tests for the in-browser Kociemba solver.
 *
 * The key property: applying the returned solution to the cube with our own
 * move engine must give a solved cube. That checks the facelet serialization
 * and the notation round trip between cubejs and `cubeMoves` together.
 */
import { beforeAll, describe, expect, it } from 'vitest'
import { prepareSolver, solveCube, UnsolvableCubeError } from './kociembaSolver'
import { applyMoves, getSolvedState } from '../utils/cubeMoves'
import { isSolved } from '../utils/isSolved'
import { generateScramble } from '../utils/scramble'

/** Building the tables takes about a second; allow for slow CI machines. */
const TABLE_BUILD_TIMEOUT_MS = 30_000

describe('solveCube', () => {
    beforeAll(() => prepareSolver(), TABLE_BUILD_TIMEOUT_MS)

    it('returns no moves for a solved cube', () => {
        expect(solveCube(getSolvedState())).toEqual([])
    })

    it('solves a single turn', () => {
        const state = applyMoves(getSolvedState(), 'R')
        expect(isSolved(applyMoves(state, solveCube(state).join(' ')))).toBe(true)
    })

    it('solves random scrambles in at most 22 moves', () => {
        for (let i = 0; i < 25; i++) {
            const state = applyMoves(getSolvedState(), generateScramble())
            const moves = solveCube(state)
            expect(moves.length).toBeLessThanOrEqual(22)
            expect(isSolved(applyMoves(state, moves.join(' ')))).toBe(true)
        }
    }, TABLE_BUILD_TIMEOUT_MS)

    it('returns only face turns in standard notation', () => {
        const moves = solveCube(applyMoves(getSolvedState(), "R U R' U' F2 D B'"))
        for (const move of moves) expect(move).toMatch(/^[URFDLB]['2]?$/)
    })

    it('refuses an impossible cube instead of searching', () => {
        const broken = getSolvedState()
        broken.U[2][1] = 'F'
        broken.F[0][1] = 'U' // flipped edge
        expect(() => solveCube(broken)).toThrow(UnsolvableCubeError)
    })
})
