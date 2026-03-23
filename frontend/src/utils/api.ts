import type { CubeState } from '../types'
const base_api = import.meta.env.VITE_API_URL || `http://localhost:8000/api`

export async function fetchScramble() {
    const response = await fetch(`${base_api}/cube/scramble`)
    const data = await response.json()
    return data
}

export async function saveSolve(timeMs: number, scramble: string, mode: 'cube' | 'timer' = 'cube') {
    const response = await fetch(`${base_api}/solves`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ time_ms: timeMs, scramble: scramble, mode })
    })
    const data = await response.json()
    return data
}

export async function fetchSolves(mode?: 'cube' | 'timer') {
    const url = mode ? `${base_api}/solves?mode=${mode}` : `${base_api}/solves`
    const response = await fetch(url)
    const data = await response.json()
    return data
}

export async function deleteSolve(id: string) {
    const response = await fetch(`${base_api}/solves/${id}`, { method: 'DELETE' })
    if (!response.ok) throw new Error('Failed to delete solve')
    return response.json()
}

export async function updatePenalty(id: string, penalty: '+2' | 'DNF' | null) {
    const response = await fetch(`${base_api}/solves/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ penalty })
    })
    if (!response.ok) throw new Error('Failed to update penalty')
    return response.json()
}

export async function applyMove(state: CubeState, move: string) {
    const response = await fetch(`${base_api}/cube/move`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ state: state, moves: move })
    })
    const data = await response.json()
    return data
}
