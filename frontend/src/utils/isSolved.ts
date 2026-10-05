/**
 * Solved-state check used to stop the Cube mode timer.
 */
import type { CubeState } from '../types'

/**
 * Report whether every face is a single color.
 *
 * Compares each sticker to its own face's center rather than to a fixed
 * color, so a solved cube still counts as solved after whole-cube rotations.
 *
 * @param curState - The cube to check.
 * @returns True if the cube is solved in any orientation.
 */
export function isSolved(curState: CubeState): boolean {
    const faces = [curState.U, curState.F, curState.R, curState.L, curState.B, curState.D]
    return faces.every(face => face.every(row => row.every(sticker => sticker === face[1][1])))
}
