/**
 * Tests for the editable-cube helpers behind Solve mode's sticker entry, and
 * for the plain-English move descriptions shown while stepping a solution.
 */
import { describe, expect, it } from 'vitest'
import { countBlankStickers, countColors, createBlankCube, isComplete, setSticker, toEditable } from './editableCube'
import { getSolvedState } from './cubeMoves'
import { describeMove } from './moveDescriptions'

describe('editable cube', () => {
    it('starts blank apart from the six fixed centers', () => {
        const cube = createBlankCube()
        expect(countBlankStickers(cube)).toBe(48)
        expect(countColors(cube)).toEqual({ U: 1, D: 1, L: 1, R: 1, F: 1, B: 1 })
        expect(cube.F[1][1]).toBe('F')
    })

    it('paints a sticker without changing the original cube', () => {
        const cube = createBlankCube()
        const painted = setSticker(cube, 'R', 0, 2, 'D')
        expect(painted.R[0][2]).toBe('D')
        expect(cube.R[0][2]).toBeNull()
    })

    it('refuses to recolor a center', () => {
        expect(() => setSticker(createBlankCube(), 'U', 1, 1, 'D')).toThrow('fixed')
    })

    it('refuses a position outside the face', () => {
        expect(() => setSticker(createBlankCube(), 'U', 3, 0, 'D')).toThrow('out of range')
    })

    it('counts as complete only when no sticker is blank', () => {
        expect(isComplete(createBlankCube())).toBe(false)
        expect(isComplete(toEditable(getSolvedState()))).toBe(true)
    })
})

describe('describeMove', () => {
    it('describes quarter, counter and half turns', () => {
        expect(describeMove('R')).toBe('Turn the right face a quarter turn (front stickers move up).')
        expect(describeMove("U'")).toBe('Turn the top face a quarter turn (front stickers move to the right).')
        expect(describeMove('F2')).toMatch(/front face twice/)
    })

    it('rejects anything that is not a face turn', () => {
        expect(() => describeMove('M')).toThrow('Not a face turn')
        expect(() => describeMove('R3')).toThrow('Not a face turn')
    })
})
