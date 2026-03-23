import type { CubeState } from '../types'

// Color mapping: pygame color → face letter
// white=U, yellow=D, orange=L, green=F, red=R, blue=B

export function isFlowerComplete(s: CubeState): boolean {
    // Yellow center on top with 4 white edges around it
    return s.U[1][1] === 'D' &&
        s.U[0][1] === 'U' &&
        s.U[1][0] === 'U' &&
        s.U[1][2] === 'U' &&
        s.U[2][1] === 'U'
}

export function isCrossComplete(s: CubeState): boolean {
    // White cross on bottom
    return s.D[1][1] === 'U' &&
        s.D[0][1] === 'U' &&
        s.D[1][0] === 'U' &&
        s.D[1][2] === 'U' &&
        s.D[2][1] === 'U'
}

export function isFirstLayerComplete(s: CubeState): boolean {
    if (!isCrossComplete(s)) return false
    // All bottom corners white
    if (s.D[0][0] !== 'U' || s.D[0][2] !== 'U' || s.D[2][0] !== 'U' || s.D[2][2] !== 'U') return false
    // Bottom row of each side matches its center
    for (const face of ['F', 'L', 'R', 'B'] as const) {
        const f = s[face]
        if (f[1][1] !== f[2][0] || f[1][1] !== f[2][1] || f[1][1] !== f[2][2]) return false
    }
    return true
}

export function isSecondLayerComplete(s: CubeState): boolean {
    if (!isFirstLayerComplete(s)) return false
    // Middle row of each side matches its center
    for (const face of ['F', 'L', 'R', 'B'] as const) {
        const f = s[face]
        if (f[1][1] !== f[1][0] || f[1][1] !== f[1][2]) return false
    }
    return true
}

export function isYellowCrossComplete(s: CubeState): boolean {
    if (!isSecondLayerComplete(s)) return false
    return s.U[1][1] === 'D' &&
        s.U[0][1] === 'D' &&
        s.U[1][0] === 'D' &&
        s.U[1][2] === 'D' &&
        s.U[2][1] === 'D'
}

export function isOLLComplete(s: CubeState): boolean {
    if (!isYellowCrossComplete(s)) return false
    return s.U[0][0] === 'D' &&
        s.U[0][2] === 'D' &&
        s.U[2][0] === 'D' &&
        s.U[2][2] === 'D'
}

export function isCPLLComplete(s: CubeState): boolean {
    if (!isOLLComplete(s)) return false
    return s.F[0][0] === s.F[0][2] &&
        s.R[0][0] === s.R[0][2] &&
        s.L[0][0] === s.L[0][2] &&
        s.B[0][0] === s.B[0][2]
}

export function isCubeSolved(s: CubeState): boolean {
    if (!isCPLLComplete(s)) return false
    for (const face of ['F', 'L', 'R', 'B'] as const) {
        const f = s[face]
        if (f[1][1] !== f[0][0] || f[1][1] !== f[0][1] || f[1][1] !== f[0][2]) return false
    }
    return true
}
