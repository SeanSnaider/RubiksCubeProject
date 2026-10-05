/**
 * Random scramble generation for Cube mode, Learn mode and Solve mode's
 * "Random cube" button.
 */

const faces: string[] = ['U', 'D', 'L', 'R', 'F', 'B']
const modifiers: string[] = ['', "'", '2']

/** Scramble length; 20 face turns is the WCA-style standard. */
const SCRAMBLE_LENGTH = 20

/**
 * Generate a random WCA-style scramble of face turns.
 *
 * Never turns the same face twice in a row, since `R R'` or `R R2` would just
 * collapse into fewer moves. Only face turns are used, so the centers never
 * move and the cube stays white-up, green-front.
 *
 * @returns The scramble as space-separated standard notation.
 */
export function generateScramble(): string {
    const result: string[] = []
    let prevFace = ''
    while (result.length < SCRAMBLE_LENGTH) {
        const curFace = faces[Math.floor(Math.random() * faces.length)]
        if (curFace === prevFace) continue
        const modifier = modifiers[Math.floor(Math.random() * modifiers.length)]
        result.push(curFace + modifier)
        prevFace = curFace
    }
    return result.join(' ')
}
