import type { CubeState } from '../types'

// 
export function isSolved(curState: CubeState) {
    let states = [curState.U, curState.F, curState.R, 
        curState.L, curState.B, curState.D]

    for (let index: number = 0; index < 6; index++) {
        for (let row: number = 0; row < 3; row++) {
            for (let col: number = 0; col < 3; col++) {
                if (states[index][row][col] != states[index][1][1]) {
                    return false
                }
            }
        }
    }
    return true
}

