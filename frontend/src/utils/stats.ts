import type { Solve } from '../types'

// Helper: get the effective time for a solve (accounting for penalties)
// +2 adds 2000ms, DNF = Infinity
function effectiveTime(solve: Solve): number {
    if (solve.penalty === 'DNF') return Infinity
    if (solve.penalty === '+2') return solve.time_ms + 2000
    return solve.time_ms
}

// TODO(human): Implement these four statistics functions
// Each takes an array of Solve objects (most recent first)

// Best single: return the lowest effective time, or null if no solves
export function calcBest(solves: Solve[]): number | null {
    if (solves.length === 0) return null
    const times = solves.map(s => effectiveTime(s))
    let best = Infinity
    for (let index: number = 0; index < times.length; index++) {
        if (times[index] < best) {
            best = times[index]
        }
    }
    return best
}

// Mean: return the simple average of all effective times, or null if empty
// If ANY solve is DNF, you could either skip it or return Infinity — your choice
export function calcMean(solves: Solve[]): number | null {
    if (solves.length === 0) return null
    const times = solves.map(s => effectiveTime(s))
    let count = 0
    let total = 0
    for (let index: number = 0; index < times.length; index++) {
        if (times[index] !== Infinity) {
            total += times[index]
            count++
        }
    }
    return total / count
}

// Average of 5: use the 5 most recent solves
// Drop the best and worst, average the remaining 3
// Return null if fewer than 5 solves
export function calcAo5(solves: Solve[]): number | null {
    if (solves.length < 5) return null
    const times = solves.map(s => effectiveTime(s)).slice(0, 5)
    let best = Infinity
    let worst = -1
    let total = 0
    for (let index: number = 0; index < 5; index++) {
        if (times[index] > worst) {
            worst = times[index]
        }
        if (times[index] < best) {
            best = times[index]
        }
    }
    for (let index: number = 0; index < 5; index++) {
        if (times[index] !== best && times[index] !== worst) {
            total += times[index]
        }
    }
    return total / 3
}

// Average of 12: use the 12 most recent solves
// Drop the best and worst, average the remaining 10
// Return null if fewer than 12 solves
export function calcAo12(solves: Solve[]): number | null {
    if (solves.length < 12) return null
    const times = solves.map(s => effectiveTime(s)).slice(0, 12)
    let best = Infinity
    let worst = -1
    let total = 0
    for (let index: number = 0; index < 12; index++) {
        if (times[index] > worst) {
            worst = times[index]
        }
        if (times[index] < best) {
            best = times[index]
        }
    }
    for (let index: number = 0; index < 12; index++) {
        if (times[index] !== best && times[index] !== worst) {
            total += times[index]
        }
    }
    return total / 10
}
