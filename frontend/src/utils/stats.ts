import type { Solve } from '../types'

export function effectiveTime(solve: Solve): number {
    if (solve.penalty === 'DNF') return Infinity
    if (solve.penalty === '+2') return solve.time_ms + 2000
    return solve.time_ms
}

export function calcSolveCount(solves: Solve[]): number {
    return solves.length
}

export function calcBest(solves: Solve[]): number | null {
    if (solves.length === 0) return null
    let best = Infinity
    for (const s of solves) {
        const t = effectiveTime(s)
        if (t < best) best = t
    }
    return best === Infinity ? null : best
}

export function calcWorst(solves: Solve[]): number | null {
    if (solves.length === 0) return null
    let hasNonDNF = false
    let worst = -Infinity
    for (const s of solves) {
        const t = effectiveTime(s)
        if (t === Infinity) return Infinity
        hasNonDNF = true
        if (t > worst) worst = t
    }
    return hasNonDNF ? worst : null
}

export function calcMean(solves: Solve[]): number | null {
    if (solves.length === 0) return null
    let total = 0
    let count = 0
    for (const s of solves) {
        const t = effectiveTime(s)
        if (t !== Infinity) {
            total += t
            count++
        }
    }
    return count === 0 ? null : total / count
}

export function calcStdDev(solves: Solve[]): number | null {
    if (solves.length < 2) return null
    const times = solves.map(effectiveTime).filter(t => t !== Infinity)
    if (times.length < 2) return null
    const mean = times.reduce((a, b) => a + b, 0) / times.length
    const variance = times.reduce((sum, t) => sum + (t - mean) ** 2, 0) / times.length
    return Math.sqrt(variance)
}

// Generic trimmed average of N solves (solves array is most-recent-first).
// WCA rules: drop best and worst by index, average the remaining N-2.
// If more than 1 DNF → DNF average (Infinity).
export function calcAoN(solves: Solve[], n: number): number | null {
    if (solves.length < n) return null
    const times = solves.slice(0, n).map(effectiveTime)

    if (times.filter(t => t === Infinity).length > 1) return Infinity

    let bestIdx = 0
    let worstIdx = 0
    for (let i = 1; i < n; i++) {
        if (times[i] < times[bestIdx]) bestIdx = i
        if (times[i] > times[worstIdx]) worstIdx = i
    }

    // If all times are equal, bestIdx and worstIdx are both 0 — use 0 and 1
    if (bestIdx === worstIdx) {
        bestIdx = 0
        worstIdx = 1
    }

    let total = 0
    for (let i = 0; i < n; i++) {
        if (i !== bestIdx && i !== worstIdx) {
            total += times[i]
        }
    }
    return total / (n - 2)
}

export function calcAo5(solves: Solve[]): number | null {
    return calcAoN(solves, 5)
}

export function calcAo12(solves: Solve[]): number | null {
    return calcAoN(solves, 12)
}

export function calcAo50(solves: Solve[]): number | null {
    return calcAoN(solves, 50)
}

export function calcAo100(solves: Solve[]): number | null {
    return calcAoN(solves, 100)
}

// Best AoN: slide a window across all solves and return the minimum average.
// Caps at the 200 most recent solves for performance.
export function calcBestAoN(solves: Solve[], n: number): number | null {
    if (solves.length < n) return null
    const pool = solves.slice(0, Math.min(solves.length, 200))
    let best: number | null = null
    for (let i = 0; i <= pool.length - n; i++) {
        const avg = calcAoN(pool.slice(i, i + n), n)
        if (avg !== null && avg !== Infinity && (best === null || avg < best)) {
            best = avg
        }
    }
    return best
}

export function calcBestAo5(solves: Solve[]): number | null {
    return calcBestAoN(solves, 5)
}

export function calcBestAo12(solves: Solve[]): number | null {
    return calcBestAoN(solves, 12)
}
