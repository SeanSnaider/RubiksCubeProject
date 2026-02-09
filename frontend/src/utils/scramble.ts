const faces: string[] = ['U', 'D', 'L', 'R', 'F', 'B'];
const modifiers: string[] = ['', "'", '2'];

// function to gen a WCA type scramble
export function generateScramble() {
    let result: string[] = [] // empty array to start
    let prevFace: string = ""
    let curFace: string = ""
    let modifier: string = ""
    // continue looping until the length is 20
    while (result.length < 20) {
        curFace = faces[Math.floor(Math.random() * faces.length)]
        if (curFace === prevFace) {
            continue 
        }
        modifier = modifiers[Math.floor(Math.random() * modifiers.length)]

        result.push(curFace + modifier)
        prevFace = curFace
    } 
    return result.join(" ");
}