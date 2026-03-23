import type { Solve } from '../types'

// ── Timer solves ────────────────────────────────────────────────────────────

const TIMER_KEY = 'rubiks_timer_solves'

function loadTimer(): Solve[] {
    try {
        return JSON.parse(localStorage.getItem(TIMER_KEY) ?? '[]')
    } catch {
        return []
    }
}

function persistTimer(solves: Solve[]): void {
    localStorage.setItem(TIMER_KEY, JSON.stringify(solves))
}

export function getTimerSolves(): Solve[] {
    return loadTimer()
}

export function addTimerSolve(timeMs: number): Solve {
    const solve: Solve = {
        _id: crypto.randomUUID(),
        time_ms: timeMs,
        scramble: '',
        penalty: null,
        mode: 'timer',
        created_at: new Date().toISOString(),
    }
    persistTimer([solve, ...loadTimer()])
    return solve
}

export function removeTimerSolve(id: string): void {
    persistTimer(loadTimer().filter(s => s._id !== id))
}

export function setTimerPenalty(id: string, penalty: '+2' | 'DNF' | null): void {
    persistTimer(loadTimer().map(s => s._id === id ? { ...s, penalty } : s))
}

// ── Cube solves ─────────────────────────────────────────────────────────────

const CUBE_KEY = 'rubiks_cube_solves'

function loadCube(): Solve[] {
    try {
        return JSON.parse(localStorage.getItem(CUBE_KEY) ?? '[]')
    } catch {
        return []
    }
}

function persistCube(solves: Solve[]): void {
    localStorage.setItem(CUBE_KEY, JSON.stringify(solves))
}

export function getCubeSolves(): Solve[] {
    return loadCube()
}

export function addCubeSolve(timeMs: number, scramble: string): Solve {
    const solve: Solve = {
        _id: crypto.randomUUID(),
        time_ms: timeMs,
        scramble,
        penalty: null,
        mode: 'cube',
        created_at: new Date().toISOString(),
    }
    persistCube([solve, ...loadCube()])
    return solve
}

export function removeCubeSolve(id: string): void {
    persistCube(loadCube().filter(s => s._id !== id))
}

export function setCubePenalty(id: string, penalty: '+2' | 'DNF' | null): void {
    persistCube(loadCube().map(s => s._id === id ? { ...s, penalty } : s))
}
