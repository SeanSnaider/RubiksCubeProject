/**
 * Plain-English descriptions of face turns, for people following a solution
 * on a physical cube who may not know the notation yet.
 *
 * Descriptions assume the cube is held the way Solve mode asks: white center
 * on top, green center facing you. Each one says which face turns and which way
 * the stickers nearest you move, since "clockwise" for the back or bottom face
 * is easy to get backwards.
 */

/** Face letter → the face's name and which way its quarter turns go. */
const FACE_TURNS: Record<string, { name: string; clockwise: string; counterClockwise: string }> = {
    R: { name: 'right', clockwise: 'front stickers move up', counterClockwise: 'front stickers move down' },
    L: { name: 'left', clockwise: 'front stickers move down', counterClockwise: 'front stickers move up' },
    U: { name: 'top', clockwise: 'front stickers move to the left', counterClockwise: 'front stickers move to the right' },
    D: { name: 'bottom', clockwise: 'front stickers move to the right', counterClockwise: 'front stickers move to the left' },
    F: { name: 'front', clockwise: 'clockwise as you look at it', counterClockwise: 'counter-clockwise as you look at it' },
    B: { name: 'back', clockwise: 'its top stickers move to your left', counterClockwise: 'its top stickers move to your right' },
}

/**
 * Describe a single face turn in words.
 *
 * @param move - A face turn in standard notation: a face letter (`URFDLB`)
 *   optionally followed by `'` or `2`.
 * @returns A sentence such as "Turn the right face a quarter turn (front
 *   stickers move up)."
 * @throws {Error} If the move isn't a single face turn.
 */
export function describeMove(move: string): string {
    const face = FACE_TURNS[move[0]]
    const suffix = move.slice(1)
    if (!face || !['', "'", '2'].includes(suffix)) {
        throw new Error(`Not a face turn: ${move}`)
    }
    if (suffix === '2') return `Turn the ${face.name} face twice (a half turn; either direction works).`
    const direction = suffix === "'" ? face.counterClockwise : face.clockwise
    return `Turn the ${face.name} face a quarter turn (${direction}).`
}
