/**
 * Facelet serialization and solvability checks for a hand-entered cube.
 *
 * Kociemba's solver works on a 54-character "facelet string": the faces in
 * `URFDLB` order, each read row by row. Our `CubeState` already uses the same
 * per-face layout (this is what `backend/app/services/cube_service.py` relies
 * on too), so serializing is a straight read.
 *
 * Contents:
 * - `toFaceletString()`   — CubeState → Kociemba facelet string
 * - `findCubeProblems()`  — everything that stops a hand-entered cube being
 *                           solvable, as messages a user can act on
 *
 * Usage notes:
 * - Always run `findCubeProblems()` before handing a cube to the solver. The
 *   `cubejs` search does no validation of its own, and an impossible cube
 *   (a twisted corner, say) sends it searching for a very long time instead of
 *   failing.
 * - The piece tables below use Kociemba's facelet numbering. U1..U9 are
 *   indices 0..8, R1..R9 are 9..17, and so on, matching `FACELET_FACE_ORDER`.
 */
import type { Color, CubeState, EditableCube, FaceName, Sticker } from '../types'
import { COLOR_NAME, FACE_POSITION_NAME } from './colors'
import { countBlankStickers, countColors } from './editableCube'

/** Face order of the Kociemba facelet string. */
export const FACELET_FACE_ORDER: readonly FaceName[] = ['U', 'R', 'F', 'D', 'L', 'B']

/** Number of stickers of each color on a real cube. */
const STICKERS_PER_COLOR = 9

/**
 * The three facelets of each corner position, listed clockwise starting with
 * the U or D facelet. Order: URF, UFL, ULB, UBR, DFR, DLF, DBL, DRB.
 */
const CORNER_FACELETS: readonly (readonly [number, number, number])[] = [
    [8, 9, 20], [6, 18, 38], [0, 36, 47], [2, 45, 11],
    [29, 26, 15], [27, 44, 24], [33, 53, 42], [35, 17, 51],
]

/** The colors of each corner piece, in the same order as `CORNER_FACELETS`. */
const CORNER_COLORS: readonly (readonly [Color, Color, Color])[] = [
    ['U', 'R', 'F'], ['U', 'F', 'L'], ['U', 'L', 'B'], ['U', 'B', 'R'],
    ['D', 'F', 'R'], ['D', 'L', 'F'], ['D', 'B', 'L'], ['D', 'R', 'B'],
]

/**
 * The two facelets of each edge position. Order: UR, UF, UL, UB, DR, DF, DL,
 * DB, FR, FL, BL, BR.
 */
const EDGE_FACELETS: readonly (readonly [number, number])[] = [
    [5, 10], [7, 19], [3, 37], [1, 46],
    [32, 16], [28, 25], [30, 43], [34, 52],
    [23, 12], [21, 41], [50, 39], [48, 14],
]

/** The colors of each edge piece, in the same order as `EDGE_FACELETS`. */
const EDGE_COLORS: readonly (readonly [Color, Color])[] = [
    ['U', 'R'], ['U', 'F'], ['U', 'L'], ['U', 'B'],
    ['D', 'R'], ['D', 'F'], ['D', 'L'], ['D', 'B'],
    ['F', 'R'], ['F', 'L'], ['B', 'L'], ['B', 'R'],
]

/** A piece found at a position: which piece it is and how it is turned. */
interface PlacedPiece {
    /** Index into `CORNER_COLORS` / `EDGE_COLORS`. */
    piece: number
    /** Twist (0–2) for a corner, flip (0–1) for an edge. */
    orientation: number
}

/**
 * Serialize a cube into Kociemba's facelet string.
 *
 * @param state - A complete cube in the standard orientation (U center white,
 *   F center green).
 * @returns The 54-character facelet string, faces in `URFDLB` order.
 */
export function toFaceletString(state: CubeState): string {
    return FACELET_FACE_ORDER.map(face => state[face].flat().join('')).join('')
}

/**
 * Read the sticker at a Kociemba facelet index.
 *
 * @param cube - The cube to read.
 * @param index - Facelet index, 0–53.
 * @returns The sticker there.
 */
function stickerAt(cube: EditableCube, index: number): Sticker {
    const face = FACELET_FACE_ORDER[Math.floor(index / 9)]
    const withinFace = index % 9
    return cube[face][Math.floor(withinFace / 3)][withinFace % 3]
}

/**
 * Describe a position by the faces it touches, e.g. "top-front-right".
 *
 * @param facelets - The facelet indices of the position.
 * @returns A lowercase, hyphenated description.
 */
function describePosition(facelets: readonly number[]): string {
    return facelets
        .map(index => FACE_POSITION_NAME[FACELET_FACE_ORDER[Math.floor(index / 9)]].toLowerCase())
        .join('-')
}

/**
 * Describe a piece by its colors, e.g. "white-red-green".
 *
 * @param colors - The piece's sticker colors.
 * @returns A lowercase, hyphenated description.
 */
function describeColors(colors: readonly Sticker[]): string {
    return colors.map(c => (c === null ? 'blank' : COLOR_NAME[c].toLowerCase())).join('-')
}

/**
 * Identify the corner piece sitting at a corner position.
 *
 * @param cube - A cube with no blank stickers.
 * @param position - Index into `CORNER_FACELETS`.
 * @returns The piece and its twist, or null if the stickers there don't form
 *   any real corner (wrong colors, or a mirror-image arrangement).
 */
function identifyCorner(cube: EditableCube, position: number): PlacedPiece | null {
    const stickers = CORNER_FACELETS[position].map(index => stickerAt(cube, index))
    const twist = stickers.findIndex(s => s === 'U' || s === 'D')
    if (twist === -1) return null
    const clockwise1 = stickers[(twist + 1) % 3]
    const clockwise2 = stickers[(twist + 2) % 3]
    // Matching the U/D sticker too (Kociemba's own check skips it) means a
    // mirror-image corner is reported as impossible, not as a duplicate of the
    // opposite layer's piece.
    const piece = CORNER_COLORS.findIndex(
        ([c0, c1, c2]) => c0 === stickers[twist] && c1 === clockwise1 && c2 === clockwise2,
    )
    return piece === -1 ? null : { piece, orientation: twist }
}

/**
 * Identify the edge piece sitting at an edge position.
 *
 * @param cube - A cube with no blank stickers.
 * @param position - Index into `EDGE_FACELETS`.
 * @returns The piece and its flip, or null if no real edge has those colors.
 */
function identifyEdge(cube: EditableCube, position: number): PlacedPiece | null {
    const [a, b] = EDGE_FACELETS[position].map(index => stickerAt(cube, index))
    for (let piece = 0; piece < EDGE_COLORS.length; piece++) {
        const [c0, c1] = EDGE_COLORS[piece]
        if (a === c0 && b === c1) return { piece, orientation: 0 }
        if (a === c1 && b === c0) return { piece, orientation: 1 }
    }
    return null
}

/**
 * Compute whether a permutation is odd.
 *
 * @param permutation - A permutation of 0..n-1.
 * @returns True if it takes an odd number of swaps to sort.
 */
function isOddPermutation(permutation: readonly number[]): boolean {
    let inversions = 0
    for (let i = 0; i < permutation.length; i++) {
        for (let j = i + 1; j < permutation.length; j++) {
            if (permutation[i] > permutation[j]) inversions += 1
        }
    }
    return inversions % 2 === 1
}

/**
 * Check that the centers are white-up, green-front, the orientation Solve
 * mode enters cubes in.
 *
 * @param cube - The cube to check.
 * @returns A problem message per misplaced center.
 */
function findCenterProblems(cube: EditableCube): string[] {
    return FACELET_FACE_ORDER
        .filter(face => cube[face][1][1] !== face)
        .map(face => `The ${FACE_POSITION_NAME[face].toLowerCase()} center must be ${COLOR_NAME[face].toLowerCase()}.`)
}

/**
 * Check that every color has been used exactly nine times.
 *
 * @param cube - The cube to check.
 * @returns A problem message per color with the wrong count.
 */
function findCountProblems(cube: EditableCube): string[] {
    const counts = countColors(cube)
    return (Object.keys(counts) as Color[])
        .filter(color => counts[color] !== STICKERS_PER_COLOR)
        .map(color => `${COLOR_NAME[color]} is used ${counts[color]} times; a real cube has exactly ${STICKERS_PER_COLOR}.`)
}

/**
 * Identify every piece, checking each is real and appears exactly once.
 *
 * @param cube - A complete cube with correct color counts.
 * @returns The corners and edges found (null where no piece could be
 *   identified), and a problem message for each bad or repeated piece.
 */
function identifyPieces(cube: EditableCube): {
    corners: (PlacedPiece | null)[]
    edges: (PlacedPiece | null)[]
    problems: string[]
} {
    const problems: string[] = []
    const corners = CORNER_FACELETS.map((_, position) => identifyCorner(cube, position))
    const edges = EDGE_FACELETS.map((_, position) => identifyEdge(cube, position))

    corners.forEach((found, position) => {
        if (found === null) {
            const facelets = CORNER_FACELETS[position]
            problems.push(
                `The ${describePosition(facelets)} corner is ${describeColors(facelets.map(i => stickerAt(cube, i)))}, ` +
                'which isn\'t a real corner piece. Re-check those three stickers.',
            )
        }
    })
    edges.forEach((found, position) => {
        if (found === null) {
            const facelets = EDGE_FACELETS[position]
            problems.push(
                `The ${describePosition(facelets)} edge is ${describeColors(facelets.map(i => stickerAt(cube, i)))}, ` +
                'which isn\'t a real edge piece. Re-check those two stickers.',
            )
        }
    })

    problems.push(...findRepeatedPieces(corners, CORNER_COLORS, 'corner'))
    problems.push(...findRepeatedPieces(edges, EDGE_COLORS, 'edge'))
    return { corners, edges, problems }
}

/**
 * Report any piece that was found in more than one position.
 *
 * @param found - The piece identified at each position.
 * @param pieceColors - The color table for this kind of piece.
 * @param kind - "corner" or "edge", for the message.
 * @returns A problem message per repeated piece.
 */
function findRepeatedPieces(
    found: readonly (PlacedPiece | null)[],
    pieceColors: readonly (readonly Color[])[],
    kind: 'corner' | 'edge',
): string[] {
    const occurrences = new Array<number>(pieceColors.length).fill(0)
    for (const placed of found) {
        if (placed !== null) occurrences[placed.piece] += 1
    }
    return occurrences.flatMap((count, piece) =>
        count > 1
            ? [`The ${describeColors(pieceColors[piece])} ${kind} appears ${count} times; each piece exists only once.`]
            : [],
    )
}

/**
 * Find everything that prevents a hand-entered cube from being solved.
 *
 * Checks run from the most to the least obvious mistake, and later checks only
 * run once earlier ones pass, so the user sees the problem they can fix first:
 * blank stickers, wrong color counts, impossible or repeated pieces, then the
 * three invariants a real cube always satisfies (corner twist, edge flip,
 * permutation parity).
 *
 * @param cube - The cube as entered, possibly with blank stickers.
 * @returns Problem messages written for the user; empty if the cube is solvable.
 */
export function findCubeProblems(cube: EditableCube): string[] {
    const centerProblems = findCenterProblems(cube)
    if (centerProblems.length > 0) return centerProblems

    const blanks = countBlankStickers(cube)
    if (blanks > 0) {
        return [`${blanks} sticker${blanks === 1 ? ' is' : 's are'} still blank.`]
    }

    const countProblems = findCountProblems(cube)
    if (countProblems.length > 0) return countProblems

    const { corners, edges, problems } = identifyPieces(cube)
    if (problems.length > 0) return problems

    // Every piece is real and unique, so none of these are null.
    const placedCorners = corners as PlacedPiece[]
    const placedEdges = edges as PlacedPiece[]
    const invariantProblems: string[] = []

    const totalTwist = placedCorners.reduce((sum, c) => sum + c.orientation, 0)
    if (totalTwist % 3 !== 0) {
        invariantProblems.push(
            'A corner is twisted in place, which can\'t happen by turning a real cube. ' +
            'One corner\'s three colors were probably entered rotated around it.',
        )
    }

    const totalFlip = placedEdges.reduce((sum, e) => sum + e.orientation, 0)
    if (totalFlip % 2 !== 0) {
        invariantProblems.push(
            'An edge is flipped in place, which can\'t happen by turning a real cube. ' +
            'One edge\'s two colors were probably entered the wrong way round.',
        )
    }

    const cornerOdd = isOddPermutation(placedCorners.map(c => c.piece))
    const edgeOdd = isOddPermutation(placedEdges.map(e => e.piece))
    if (cornerOdd !== edgeOdd) {
        invariantProblems.push(
            'Two pieces are swapped, which can\'t happen by turning a real cube. ' +
            'Two stickers were probably entered in each other\'s places.',
        )
    }

    return invariantProblems
}
