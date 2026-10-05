/**
 * Tests for the client-side move engine.
 *
 * These check algebraic properties every correct cube engine has (a quarter
 * turn repeated four times is the identity, a move undoes its inverse, a few
 * well-known sequences have known orders) rather than hand-written sticker
 * layouts, so they catch a broken move without restating its implementation.
 */
import { describe, expect, it } from 'vitest'
import { applyMove, applyMoves, getSolvedState, MOVE_MAP, parseMoves } from './cubeMoves'

/** Quarter-turn moves with a prime counterpart. */
const QUARTER_TURNS = Object.keys(MOVE_MAP).filter(move => !move.endsWith("'") && !move.endsWith('2'))

describe('move engine', () => {
    it.each(QUARTER_TURNS)('returns to solved after four %s turns', move => {
        expect(applyMoves(getSolvedState(), `${move} ${move} ${move} ${move}`)).toEqual(getSolvedState())
    })

    it.each(QUARTER_TURNS)('undoes %s with its prime', move => {
        const scrambled = applyMoves(getSolvedState(), "R U F' L2 D B'")
        expect(applyMoves(scrambled, `${move} ${move}'`)).toEqual(scrambled)
    })

    it.each(QUARTER_TURNS)('makes %s2 the same as two %s turns', move => {
        expect(applyMove(getSolvedState(), `${move}2`)).toEqual(applyMoves(getSolvedState(), `${move} ${move}`))
    })

    it('returns to solved after the sexy move six times', () => {
        expect(applyMoves(getSolvedState(), "R U R' U' ".repeat(6))).toEqual(getSolvedState())
    })

    it('returns to solved after the T-perm twice', () => {
        const tPerm = "R U R' U' R' F R2 U' R' U' R U R' F'"
        expect(applyMoves(getSolvedState(), `${tPerm} ${tPerm}`)).toEqual(getSolvedState())
    })

    it('does not mutate the state it is given', () => {
        const state = getSolvedState()
        applyMove(state, 'R')
        expect(state).toEqual(getSolvedState())
    })

    it('rejects an unknown move', () => {
        expect(() => applyMove(getSolvedState(), 'Q')).toThrow('Unknown move')
    })
})

describe('parseMoves', () => {
    it('splits primes, doubles, wide moves and rotations', () => {
        expect(parseMoves("R U' F2 Rw x' y2")).toEqual(['R', "U'", 'F2', 'Rw', "x'", 'y2'])
    })

    it('skips grouping parentheses used in algorithms', () => {
        expect(parseMoves("(R U R' U')")).toEqual(['R', 'U', "R'", "U'"])
    })
})
