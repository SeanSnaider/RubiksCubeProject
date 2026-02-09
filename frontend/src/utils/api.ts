import type { CubeState } from '../types'
const base_api = `http://localhost:8000/api`

export async function fetchScramble() {
    const response = await fetch(`${base_api}/cube/scramble`)
    const data = await response.json()
    return data
}

//our post method
export async function saveSolve(timeMs: number, scramble: string) {
    const response = await fetch(`${base_api}/solves`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            time_ms: timeMs,
            scramble: scramble
        })
     })
    const data = await response.json()
    return data;
}

// our get function for fetching SOLVES, not solve
export async function fetchSolves() {
    const response = await fetch(`${base_api}/solves`)
    const data = await response.json()
    return data
}

// function that goes and will actually apply the move to the puzzle
export async function applyMove(state: CubeState, move: string) {
    const response = await fetch (`${base_api}/cube/move`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            state: state,
            moves: move
        })
    })
    const data = await response.json()
    return data;
}