/**
 * Tests for hand-entered cube validation.
 *
 * Valid cubes are produced by scrambling with the move engine, so they are
 * guaranteed reachable. Invalid cubes are made by the kinds of mistake a
 * person makes when copying colors: a blank, a wrong color, a corner entered
 * rotated, an edge entered backwards, two stickers swapped.
 */
import { describe, expect, it } from 'vitest'
import type { CubeState, EditableCube } from '../types'
import { findCubeProblems, toFaceletString } from './cubeValidation'
import { applyMoves, getSolvedState } from './cubeMoves'
import { createBlankCube, setSticker, toEditable } from './editableCube'
import { generateScramble } from './scramble'

/** Apply a scramble to a solved cube and return it in editable form. */
function scrambled(moves: string): EditableCube {
    return toEditable(applyMoves(getSolvedState(), moves))
}

describe('findCubeProblems', () => {
    it('accepts a solved cube', () => {
        expect(findCubeProblems(toEditable(getSolvedState()))).toEqual([])
    })

    it('accepts randomly scrambled cubes', () => {
        for (let i = 0; i < 200; i++) {
            expect(findCubeProblems(scrambled(generateScramble()))).toEqual([])
        }
    })

    it('reports how many stickers are still blank', () => {
        expect(findCubeProblems(createBlankCube())).toEqual(['48 stickers are still blank.'])
    })

    it('reports a color used the wrong number of times', () => {
        const cube = setSticker(toEditable(getSolvedState()), 'F', 0, 0, 'R')
        const problems = findCubeProblems(cube)
        expect(problems).toContain('Red is used 10 times; a real cube has exactly 9.')
        expect(problems).toContain('Green is used 8 times; a real cube has exactly 9.')
    })

    it('reports a corner that is not a real piece', () => {
        // Swap two stickers within the top-front-right corner: same colors, mirror image.
        let cube = toEditable(getSolvedState())
        cube = setSticker(cube, 'R', 0, 0, 'F')
        cube = setSticker(cube, 'F', 0, 2, 'R')
        expect(findCubeProblems(cube)).toEqual([
            "The top-right-front corner is white-green-red, which isn't a real corner piece. Re-check those three stickers.",
        ])
    })

    it('reports a twisted corner', () => {
        // Rotate the colors of the top-front-right corner one step.
        let cube = toEditable(getSolvedState())
        cube = setSticker(cube, 'U', 2, 2, 'F')
        cube = setSticker(cube, 'R', 0, 0, 'U')
        cube = setSticker(cube, 'F', 0, 2, 'R')
        const problems = findCubeProblems(cube)
        expect(problems).toHaveLength(1)
        expect(problems[0]).toMatch(/corner is twisted/)
    })

    it('reports a flipped edge', () => {
        let cube = toEditable(getSolvedState())
        cube = setSticker(cube, 'U', 2, 1, 'F')
        cube = setSticker(cube, 'F', 0, 1, 'U')
        const problems = findCubeProblems(cube)
        expect(problems).toHaveLength(1)
        expect(problems[0]).toMatch(/edge is flipped/)
    })

    it('reports two swapped pieces', () => {
        // Swap the front-right and front-left edges' front stickers and side stickers.
        let cube = scrambled("R U F")
        const original = cube
        cube = setSticker(cube, 'F', 1, 2, original.F[1][0])
        cube = setSticker(cube, 'F', 1, 0, original.F[1][2])
        cube = setSticker(cube, 'R', 1, 0, original.L[1][2])
        cube = setSticker(cube, 'L', 1, 2, original.R[1][0])
        const problems = findCubeProblems(cube)
        expect(problems).toHaveLength(1)
        expect(problems[0]).toMatch(/Two pieces are swapped/)
    })

    it('reports a piece that appears twice', () => {
        // Put a second white-red-green corner where white-green-orange belongs, and a
        // second yellow-orange-green where yellow-green-red belongs. Red and orange
        // trade places, so every color count stays at nine.
        let cube = toEditable(getSolvedState())
        cube = setSticker(cube, 'F', 0, 0, 'R')
        cube = setSticker(cube, 'L', 0, 2, 'F')
        cube = setSticker(cube, 'F', 2, 2, 'L')
        cube = setSticker(cube, 'R', 2, 0, 'F')
        expect(findCubeProblems(cube)).toEqual([
            'The white-red-green corner appears 2 times; each piece exists only once.',
            'The yellow-orange-green corner appears 2 times; each piece exists only once.',
        ])
    })

    it('rejects a cube whose centers are not white-up, green-front', () => {
        const rotated = toEditable(applyMoves(getSolvedState(), 'x'))
        expect(findCubeProblems(rotated).length).toBeGreaterThan(0)
    })
})

describe('toFaceletString', () => {
    it('serializes a solved cube in URFDLB order', () => {
        expect(toFaceletString(getSolvedState())).toBe(
            'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB',
        )
    })

    it('reads each face row by row', () => {
        const state: CubeState = getSolvedState()
        state.U[0][1] = 'B'
        expect(toFaceletString(state)[1]).toBe('B')
    })
})
