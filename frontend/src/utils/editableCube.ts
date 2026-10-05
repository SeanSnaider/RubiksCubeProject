/**
 * Helpers for a cube whose stickers are being entered by hand in Solve mode.
 *
 * An `EditableCube` is a `CubeState` whose stickers may still be `null`
 * (blank). The centers are always filled in: Solve mode fixes them so the
 * entered cube is in the white-up, green-front orientation the solver and the
 * user both assume.
 *
 * Every function is pure and returns a new cube instead of mutating its input,
 * so the result can go straight into React state.
 */
import type { Color, CubeState, EditableCube, FaceName, Sticker } from '../types'

/** Every face, in a stable order for iteration. */
export const FACE_NAMES: readonly FaceName[] = ['U', 'R', 'F', 'D', 'L', 'B']

/** Index of the center sticker in a face's rows and columns. */
const CENTER = 1

/**
 * Report whether a sticker position is a face's center.
 *
 * @param row - Row within the face, 0–2.
 * @param col - Column within the face, 0–2.
 * @returns True for the middle sticker, which Solve mode never lets the user change.
 */
export function isCenter(row: number, col: number): boolean {
    return row === CENTER && col === CENTER
}

/**
 * Create a cube with every sticker blank except the six fixed centers.
 *
 * @returns A new blank cube.
 */
export function createBlankCube(): EditableCube {
    const cube = {} as EditableCube
    for (const face of FACE_NAMES) {
        cube[face] = [0, 1, 2].map(row =>
            [0, 1, 2].map(col => (isCenter(row, col) ? face : null)),
        )
    }
    return cube
}

/**
 * Copy a complete cube into editable form, so it can be shown and edited.
 *
 * @param state - A fully colored cube.
 * @returns A structurally independent editable copy.
 */
export function toEditable(state: CubeState): EditableCube {
    const cube = {} as EditableCube
    for (const face of FACE_NAMES) {
        cube[face] = state[face].map(row => [...row])
    }
    return cube
}

/**
 * Return a copy of the cube with one sticker changed.
 *
 * @param cube - The cube to change. Not mutated.
 * @param face - The face the sticker is on.
 * @param row - Row within the face, 0–2.
 * @param col - Column within the face, 0–2.
 * @param sticker - The new color, or null to blank the sticker.
 * @returns The updated cube.
 * @throws {Error} If the position is a center, or outside the 3x3 grid.
 */
export function setSticker(
    cube: EditableCube, face: FaceName, row: number, col: number, sticker: Sticker,
): EditableCube {
    if (![0, 1, 2].includes(row) || ![0, 1, 2].includes(col)) {
        throw new Error(`Sticker position out of range: ${face}[${row}][${col}]`)
    }
    if (isCenter(row, col)) {
        throw new Error(`The ${face} center is fixed and can't be recolored`)
    }
    const next = { ...cube, [face]: cube[face].map(r => [...r]) }
    next[face][row][col] = sticker
    return next
}

/**
 * Count how many stickers of each color have been placed.
 *
 * @param cube - The cube to count.
 * @returns The number of stickers of each color, centers included.
 */
export function countColors(cube: EditableCube): Record<Color, number> {
    const counts: Record<Color, number> = { U: 0, D: 0, L: 0, R: 0, F: 0, B: 0 }
    for (const face of FACE_NAMES) {
        for (const row of cube[face]) {
            for (const sticker of row) {
                if (sticker !== null) counts[sticker] += 1
            }
        }
    }
    return counts
}

/**
 * Count the stickers that are still blank.
 *
 * @param cube - The cube to inspect.
 * @returns The number of null stickers.
 */
export function countBlankStickers(cube: EditableCube): number {
    let blanks = 0
    for (const face of FACE_NAMES) {
        for (const row of cube[face]) {
            blanks += row.filter(sticker => sticker === null).length
        }
    }
    return blanks
}

/**
 * Narrow an editable cube to a complete one once every sticker is filled in.
 *
 * @param cube - The cube to check.
 * @returns True if no sticker is blank.
 */
export function isComplete(cube: EditableCube): cube is CubeState {
    return countBlankStickers(cube) === 0
}
