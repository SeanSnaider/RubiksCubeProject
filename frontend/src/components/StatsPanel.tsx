import React from 'react'
import type { Solve } from '../types'
import { formatTime } from '../utils/formatTime'
import {
    calcSolveCount,
    calcBest,
    calcWorst,
    calcMean,
    calcStdDev,
    calcAo5,
    calcAo12,
    calcAo50,
    calcAo100,
    calcBestAo5,
    calcBestAo12,
} from '../utils/stats'
import styles from './StatsPanel.module.css'

interface StatsPanelProps {
    solves: Solve[]
}

function showStat(val: number | null, best?: number | null) {
    if (val === null) return <span className={styles.value}>--</span>
    if (val === Infinity) return <span className={`${styles.value} ${styles.valueDnf}`}>DNF</span>
    const isBest = best !== null && best !== undefined && val === best && val !== Infinity
    return (
        <span className={`${styles.value} ${isBest ? styles.valueBest : ''}`}>
            {formatTime(val)}
        </span>
    )
}

function StatRow({ label, value }: { label: string; value: React.ReactNode }) {
    return (
        <div className={styles.row}>
            <span className={styles.label}>{label}</span>
            {value}
        </div>
    )
}

export function StatsPanel({ solves }: StatsPanelProps) {
    const count = calcSolveCount(solves)
    const best = calcBest(solves)
    const worst = calcWorst(solves)
    const mean = calcMean(solves)
    const stdDev = calcStdDev(solves)
    const ao5 = calcAo5(solves)
    const ao12 = calcAo12(solves)
    const ao50 = calcAo50(solves)
    const ao100 = calcAo100(solves)
    const bestAo5 = calcBestAo5(solves)
    const bestAo12 = calcBestAo12(solves)

    return (
        <div className={styles.panel}>
            <div className={styles.title}>Statistics</div>
            <div className={styles.grid}>
                <div>
                    <StatRow label="Solves" value={<span className={styles.value}>{count}</span>} />
                    <StatRow label="Best" value={showStat(best)} />
                    <StatRow label="Worst" value={showStat(worst)} />
                    <StatRow label="Mean" value={showStat(mean)} />
                    <StatRow label="Std Dev" value={showStat(stdDev)} />
                </div>
                <div>
                    <StatRow label="Ao5" value={showStat(ao5, bestAo5)} />
                    <StatRow label="Best Ao5" value={showStat(bestAo5)} />
                    <StatRow label="Ao12" value={showStat(ao12, bestAo12)} />
                    <StatRow label="Best Ao12" value={showStat(bestAo12)} />
                    <StatRow label="Ao50" value={showStat(ao50)} />
                    <StatRow label="Ao100" value={showStat(ao100)} />
                </div>
            </div>
        </div>
    )
}
