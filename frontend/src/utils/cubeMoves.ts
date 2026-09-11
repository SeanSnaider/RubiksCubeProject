/**
 * Client-side Rubik's Cube move engine.
 *
 * A faithful TypeScript port of `backend/app/services/cube_service.py` so that
 * cube manipulation happens locally in the browser instead of over the network.
 * Applying a move used to cost an HTTP round trip per keypress, which added
 * visible latency between pressing a key and seeing the cube turn; these
 * functions run synchronously in well under a millisecond.
 *
 * Contents:
 * - `getSolvedState()`      — canonical solved cube
 * - 18 face moves, 6 slice moves, 8 wide moves, 6 whole-cube rotations
 * - `MOVE_MAP`              — notation string → move function
 * - `parseMoves()`          — split a notation string into individual moves
 * - `applyMove()` / `applyMoves()` — the public entry points
 *
 * Usage notes:
 * - Every function is pure: the input state is never mutated, a new state is
 *   returned. This is what lets React detect the change and re-render.
 * - The move tables must stay behaviourally identical to the backend engine.
 *   The backend still exposes `/api/cube/move` and is the authority for the
 *   solver, so a divergence here would produce two different cubes for the
 *   same move sequence. If you change a move, change it in both places.
 */
import type { CubeState, Face } from '../types'

/** A move: takes a cube state and returns the state after the turn. */
export type MoveFn = (state: CubeState) => CubeState

/**
 * Return a solved cube state.
 *
 * Each face is a 3x3 grid where every cell holds the letter of the face it
 * belongs to, which doubles as that sticker's color.
 *
 * @returns A fresh solved cube; safe for the caller to mutate.
 */
export function getSolvedState(): CubeState {
    return {
        U: [['U', 'U', 'U'], ['U', 'U', 'U'], ['U', 'U', 'U']], // White (Up)
        D: [['D', 'D', 'D'], ['D', 'D', 'D'], ['D', 'D', 'D']], // Yellow (Down)
        L: [['L', 'L', 'L'], ['L', 'L', 'L'], ['L', 'L', 'L']], // Orange (Left)
        R: [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']], // Red (Right)
        F: [['F', 'F', 'F'], ['F', 'F', 'F'], ['F', 'F', 'F']], // Green (Front)
        B: [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']], // Blue (Back)
    }
}

/**
 * Copy a single 3x3 face.
 *
 * @param face - The face to copy.
 * @returns A new face with new row arrays.
 */
function cloneFace(face: Face): Face {
    return [[...face[0]], [...face[1]], [...face[2]]]
}

/**
 * Deep-copy a cube state so a move can mutate its working copy freely.
 *
 * @param state - The state to copy.
 * @returns A structurally independent copy.
 */
function cloneState(state: CubeState): CubeState {
    return {
        U: cloneFace(state.U),
        D: cloneFace(state.D),
        L: cloneFace(state.L),
        R: cloneFace(state.R),
        F: cloneFace(state.F),
        B: cloneFace(state.B),
    }
}

/**
 * Rotate a 3x3 face 90 degrees clockwise.
 *
 * The pattern is `new[row][col] = old[2 - col][row]`.
 *
 * @param face - The face to rotate.
 * @returns A new, rotated face.
 */
function rotateFaceCw(face: Face): Face {
    return [
        [face[2][0], face[1][0], face[0][0]],
        [face[2][1], face[1][1], face[0][1]],
        [face[2][2], face[1][2], face[0][2]],
    ]
}

// =============================================================================
// BASIC FACE MOVES (U, D, L, R, F, B and their primes)
// =============================================================================

/**
 * U move: rotate the Up (white) face clockwise.
 *
 * Also cycles the top row of F → L → B → R → F.
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveU(state: CubeState): CubeState {
    const next = cloneState(state)

    next.U = rotateFaceCw(next.U)

    // Top row of Front goes to Left, Left to Back, Back to Right, Right to Front
    const temp = [...next.F[0]]
    next.F[0] = [...next.R[0]]
    next.R[0] = [...next.B[0]]
    next.B[0] = [...next.L[0]]
    next.L[0] = temp

    return next
}

/**
 * U' move — three U moves.
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveUPrime(state: CubeState): CubeState {
    let next = state
    for (let i = 0; i < 3; i++) next = moveU(next)
    return next
}

/**
 * D move: rotate the Down (yellow) face clockwise.
 *
 * Cycles the bottom row of F → L → B → R → F (opposite direction to U).
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveD(state: CubeState): CubeState {
    const next = cloneState(state)

    next.D = rotateFaceCw(next.D)

    const temp = [...next.F[2]]
    next.F[2] = [...next.L[2]]
    next.L[2] = [...next.B[2]]
    next.B[2] = [...next.R[2]]
    next.R[2] = temp

    return next
}

/**
 * D' move — three D moves.
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveDPrime(state: CubeState): CubeState {
    let next = state
    for (let i = 0; i < 3; i++) next = moveD(next)
    return next
}

/**
 * R move: rotate the Right (red) face clockwise.
 *
 * Cycles the right column through U → F → D → B. The B face is stored
 * "upside down" relative to the others, so its column is read in reverse.
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveR(state: CubeState): CubeState {
    const next = cloneState(state)

    next.R = rotateFaceCw(next.R)

    const temp = [next.U[0][2], next.U[1][2], next.U[2][2]]

    // U right col <- F right col
    next.U[0][2] = next.F[0][2]
    next.U[1][2] = next.F[1][2]
    next.U[2][2] = next.F[2][2]

    // F right col <- D right col
    next.F[0][2] = next.D[0][2]
    next.F[1][2] = next.D[1][2]
    next.F[2][2] = next.D[2][2]

    // D right col <- B left col (reversed)
    next.D[0][2] = next.B[2][0]
    next.D[1][2] = next.B[1][0]
    next.D[2][2] = next.B[0][0]

    // B left col <- temp (reversed)
    next.B[0][0] = temp[2]
    next.B[1][0] = temp[1]
    next.B[2][0] = temp[0]

    return next
}

/**
 * R' move — three R moves.
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveRPrime(state: CubeState): CubeState {
    let next = state
    for (let i = 0; i < 3; i++) next = moveR(next)
    return next
}

/**
 * L move: rotate the Left (orange) face clockwise.
 *
 * Cycles the left column through U → B → D → F, with the B face reversed.
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveL(state: CubeState): CubeState {
    const next = cloneState(state)

    next.L = rotateFaceCw(next.L)

    const temp = [next.U[0][0], next.U[1][0], next.U[2][0]]

    // U left col <- B right col (reversed)
    next.U[0][0] = next.B[2][2]
    next.U[1][0] = next.B[1][2]
    next.U[2][0] = next.B[0][2]

    // B right col <- D left col (reversed)
    next.B[0][2] = next.D[2][0]
    next.B[1][2] = next.D[1][0]
    next.B[2][2] = next.D[0][0]

    // D left col <- F left col
    next.D[0][0] = next.F[0][0]
    next.D[1][0] = next.F[1][0]
    next.D[2][0] = next.F[2][0]

    // F left col <- temp
    next.F[0][0] = temp[0]
    next.F[1][0] = temp[1]
    next.F[2][0] = temp[2]

    return next
}

/**
 * L' move — three L moves.
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveLPrime(state: CubeState): CubeState {
    let next = state
    for (let i = 0; i < 3; i++) next = moveL(next)
    return next
}

/**
 * F move: rotate the Front (green) face clockwise.
 *
 * Cycles the bottom row of U, right column of L, top row of D and left
 * column of R.
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveF(state: CubeState): CubeState {
    const next = cloneState(state)

    next.F = rotateFaceCw(next.F)

    const temp = [next.U[2][0], next.U[2][1], next.U[2][2]]

    // U bottom row <- L right col (rotated)
    next.U[2][0] = next.L[2][2]
    next.U[2][1] = next.L[1][2]
    next.U[2][2] = next.L[0][2]

    // L right col <- D top row
    next.L[0][2] = next.D[0][0]
    next.L[1][2] = next.D[0][1]
    next.L[2][2] = next.D[0][2]

    // D top row <- R left col (rotated)
    next.D[0][0] = next.R[2][0]
    next.D[0][1] = next.R[1][0]
    next.D[0][2] = next.R[0][0]

    // R left col <- temp
    next.R[0][0] = temp[0]
    next.R[1][0] = temp[1]
    next.R[2][0] = temp[2]

    return next
}

/**
 * F' move — three F moves.
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveFPrime(state: CubeState): CubeState {
    let next = state
    for (let i = 0; i < 3; i++) next = moveF(next)
    return next
}

/**
 * B move: rotate the Back (blue) face clockwise.
 *
 * Cycles the top row of U, right column of R, bottom row of D and left
 * column of L.
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveB(state: CubeState): CubeState {
    const next = cloneState(state)

    next.B = rotateFaceCw(next.B)

    const temp = [next.U[0][0], next.U[0][1], next.U[0][2]]

    // U top row <- R right col
    next.U[0][0] = next.R[0][2]
    next.U[0][1] = next.R[1][2]
    next.U[0][2] = next.R[2][2]

    // R right col <- D bottom row (reversed)
    next.R[0][2] = next.D[2][2]
    next.R[1][2] = next.D[2][1]
    next.R[2][2] = next.D[2][0]

    // D bottom row <- L left col
    next.D[2][0] = next.L[0][0]
    next.D[2][1] = next.L[1][0]
    next.D[2][2] = next.L[2][0]

    // L left col <- temp (reversed)
    next.L[0][0] = temp[2]
    next.L[1][0] = temp[1]
    next.L[2][0] = temp[0]

    return next
}

/**
 * B' move — three B moves.
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveBPrime(state: CubeState): CubeState {
    let next = state
    for (let i = 0; i < 3; i++) next = moveB(next)
    return next
}

// =============================================================================
// SLICE MOVES (M, E, S)
// =============================================================================

/**
 * M move: middle slice between L and R, turning in the same direction as L.
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveM(state: CubeState): CubeState {
    const next = cloneState(state)

    const temp = [next.U[0][1], next.U[1][1], next.U[2][1]]

    // U middle col <- B middle col (reversed)
    next.U[0][1] = next.B[2][1]
    next.U[1][1] = next.B[1][1]
    next.U[2][1] = next.B[0][1]

    // B middle col <- D middle col (reversed)
    next.B[0][1] = next.D[2][1]
    next.B[1][1] = next.D[1][1]
    next.B[2][1] = next.D[0][1]

    // D middle col <- F middle col
    next.D[0][1] = next.F[0][1]
    next.D[1][1] = next.F[1][1]
    next.D[2][1] = next.F[2][1]

    // F middle col <- temp (from U)
    next.F[0][1] = temp[0]
    next.F[1][1] = temp[1]
    next.F[2][1] = temp[2]

    return next
}

/**
 * M' move — three M moves.
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveMPrime(state: CubeState): CubeState {
    let next = state
    for (let i = 0; i < 3; i++) next = moveM(next)
    return next
}

/**
 * E move: equator slice between U and D, turning in the same direction as D.
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveE(state: CubeState): CubeState {
    const next = cloneState(state)

    // Middle row cycles: F → L → B → R → F
    const temp = [...next.F[1]]
    next.F[1] = [...next.L[1]]
    next.L[1] = [...next.B[1]]
    next.B[1] = [...next.R[1]]
    next.R[1] = temp

    return next
}

/**
 * E' move — three E moves.
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveEPrime(state: CubeState): CubeState {
    let next = state
    for (let i = 0; i < 3; i++) next = moveE(next)
    return next
}

/**
 * S move: standing slice between F and B, turning in the same direction as F.
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveS(state: CubeState): CubeState {
    const next = cloneState(state)

    const temp = [next.U[1][0], next.U[1][1], next.U[1][2]]

    // U middle row <- L middle col (rotated)
    next.U[1][0] = next.L[2][1]
    next.U[1][1] = next.L[1][1]
    next.U[1][2] = next.L[0][1]

    // L middle col <- D middle row
    next.L[0][1] = next.D[1][0]
    next.L[1][1] = next.D[1][1]
    next.L[2][1] = next.D[1][2]

    // D middle row <- R middle col (rotated)
    next.D[1][0] = next.R[2][1]
    next.D[1][1] = next.R[1][1]
    next.D[1][2] = next.R[0][1]

    // R middle col <- temp
    next.R[0][1] = temp[0]
    next.R[1][1] = temp[1]
    next.R[2][1] = temp[2]

    return next
}

/**
 * S' move — three S moves.
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveSPrime(state: CubeState): CubeState {
    let next = state
    for (let i = 0; i < 3; i++) next = moveS(next)
    return next
}

// =============================================================================
// WIDE MOVES (two layers at once)
// =============================================================================

/**
 * Rw: right two layers turn like R (R + M').
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveRw(state: CubeState): CubeState {
    return moveR(moveMPrime(state))
}

/**
 * Rw': right two layers turn like R' (R' + M).
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveRwPrime(state: CubeState): CubeState {
    return moveRPrime(moveM(state))
}

/**
 * Lw: left two layers turn like L (L + M).
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveLw(state: CubeState): CubeState {
    return moveL(moveM(state))
}

/**
 * Lw': left two layers turn like L' (L' + M').
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveLwPrime(state: CubeState): CubeState {
    return moveLPrime(moveMPrime(state))
}

/**
 * Uw: top two layers turn like U (U + E').
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveUw(state: CubeState): CubeState {
    return moveU(moveEPrime(state))
}

/**
 * Uw': top two layers turn like U' (U' + E).
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveUwPrime(state: CubeState): CubeState {
    return moveUPrime(moveE(state))
}

/**
 * Dw: bottom two layers turn like D (D + E).
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveDw(state: CubeState): CubeState {
    return moveD(moveE(state))
}

/**
 * Dw': bottom two layers turn like D' (D' + E').
 *
 * @param state - The cube before the turn.
 * @returns The cube after the turn.
 */
export function moveDwPrime(state: CubeState): CubeState {
    return moveDPrime(moveEPrime(state))
}

// =============================================================================
// WHOLE-CUBE ROTATIONS (x, y, z)
// =============================================================================

/**
 * x rotation: the whole cube turns like R (R + M' + L').
 *
 * @param state - The cube before the rotation.
 * @returns The cube after the rotation.
 */
export function moveX(state: CubeState): CubeState {
    return moveR(moveMPrime(moveLPrime(state)))
}

/**
 * x' rotation: the whole cube turns like R' (R' + M + L).
 *
 * @param state - The cube before the rotation.
 * @returns The cube after the rotation.
 */
export function moveXPrime(state: CubeState): CubeState {
    return moveRPrime(moveM(moveL(state)))
}

/**
 * y rotation: the whole cube turns like U (U + E' + D').
 *
 * @param state - The cube before the rotation.
 * @returns The cube after the rotation.
 */
export function moveY(state: CubeState): CubeState {
    return moveU(moveEPrime(moveDPrime(state)))
}

/**
 * y' rotation: the whole cube turns like U' (U' + E + D).
 *
 * @param state - The cube before the rotation.
 * @returns The cube after the rotation.
 */
export function moveYPrime(state: CubeState): CubeState {
    return moveUPrime(moveE(moveD(state)))
}

/**
 * z rotation: the whole cube turns like F (F + S + B').
 *
 * @param state - The cube before the rotation.
 * @returns The cube after the rotation.
 */
export function moveZ(state: CubeState): CubeState {
    return moveF(moveS(moveBPrime(state)))
}

/**
 * z' rotation: the whole cube turns like F' (F' + S' + B).
 *
 * @param state - The cube before the rotation.
 * @returns The cube after the rotation.
 */
export function moveZPrime(state: CubeState): CubeState {
    return moveFPrime(moveSPrime(moveB(state)))
}

// =============================================================================
// MOVE DISPATCHER
// =============================================================================

/**
 * Every supported move in standard notation, mapped to its implementation.
 *
 * Half turns (`R2`, `Uw2`, `x2`, …) are expressed as the quarter turn applied
 * twice rather than given their own implementation.
 */
export const MOVE_MAP: Record<string, MoveFn> = {
    U: moveU, "U'": moveUPrime, U2: (s) => moveU(moveU(s)),
    D: moveD, "D'": moveDPrime, D2: (s) => moveD(moveD(s)),
    R: moveR, "R'": moveRPrime, R2: (s) => moveR(moveR(s)),
    L: moveL, "L'": moveLPrime, L2: (s) => moveL(moveL(s)),
    F: moveF, "F'": moveFPrime, F2: (s) => moveF(moveF(s)),
    B: moveB, "B'": moveBPrime, B2: (s) => moveB(moveB(s)),
    M: moveM, "M'": moveMPrime, M2: (s) => moveM(moveM(s)),
    E: moveE, "E'": moveEPrime, E2: (s) => moveE(moveE(s)),
    S: moveS, "S'": moveSPrime, S2: (s) => moveS(moveS(s)),
    // Wide moves
    Rw: moveRw, "Rw'": moveRwPrime, Rw2: (s) => moveRw(moveRw(s)),
    Lw: moveLw, "Lw'": moveLwPrime, Lw2: (s) => moveLw(moveLw(s)),
    Uw: moveUw, "Uw'": moveUwPrime, Uw2: (s) => moveUw(moveUw(s)),
    Dw: moveDw, "Dw'": moveDwPrime, Dw2: (s) => moveDw(moveDw(s)),
    // Whole-cube rotations
    x: moveX, "x'": moveXPrime, x2: (s) => moveX(moveX(s)),
    y: moveY, "y'": moveYPrime, y2: (s) => moveY(moveY(s)),
    z: moveZ, "z'": moveZPrime, z2: (s) => moveZ(moveZ(s)),
}

/** Face letters that may be followed by a `w`, `'` or `2` modifier. */
const FACE_LETTERS = 'URFDLBMES'

/**
 * Parse a move string such as `"R U R' U'"` into individual moves.
 *
 * Handles single moves (`R`), primes (`R'`), half turns (`R2`), wide moves
 * (`Rw`, `Rw'`) and whole-cube rotations (`x`, `x'`, `x2`). Face letters are
 * upper-cased, so `"r u"` parses as `R U`. Unrecognised characters are
 * skipped, matching the backend parser.
 *
 * @param moves - A whitespace-separated move sequence.
 * @returns The moves in order, one notation string per entry.
 */
export function parseMoves(moves: string): string[] {
    const result: string[] = []
    const source = moves.trim()
    let i = 0

    while (i < source.length) {
        const ch = source[i]

        // Skip whitespace
        if (/\s/.test(ch)) {
            i += 1
            continue
        }

        // Whole-cube rotations: x, y, z (lowercase only)
        if (ch === 'x' || ch === 'y' || ch === 'z') {
            let move = ch
            i += 1
            if (source[i] === "'") {
                move += "'"
                i += 1
            } else if (source[i] === '2') {
                move += '2'
                i += 1
            }
            result.push(move)

        // Standard and wide face moves
        } else if (FACE_LETTERS.includes(ch.toUpperCase())) {
            let move = ch.toUpperCase()
            i += 1
            if (source[i] === 'w') {
                move += 'w'
                i += 1
            }
            if (source[i] === "'") {
                move += "'"
                i += 1
            } else if (source[i] === '2') {
                move += '2'
                i += 1
            }
            result.push(move)

        } else {
            i += 1 // Skip unknown characters
        }
    }

    return result
}

/**
 * Apply a single move to the cube state.
 *
 * @param state - The cube before the move. Not mutated.
 * @param move - A single move in standard notation, e.g. `"R'"`.
 * @returns A new state with the move applied.
 * @throws {Error} If the move is not recognised.
 */
export function applyMove(state: CubeState, move: string): CubeState {
    const fn = MOVE_MAP[move]
    if (!fn) throw new Error(`Unknown move: ${move}`)
    return fn(state)
}

/**
 * Apply a sequence of moves to the cube state.
 *
 * @param state - The cube before the sequence. Not mutated.
 * @param moves - A move sequence such as a scramble or algorithm.
 * @returns A new state with every move applied in order.
 * @throws {Error} If any parsed move is not recognised.
 */
export function applyMoves(state: CubeState, moves: string): CubeState {
    let next = state
    for (const move of parseMoves(moves)) {
        next = applyMove(next, move)
    }
    return next
}
