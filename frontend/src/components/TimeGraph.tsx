import type { Solve } from '../types'
import { effectiveTime } from '../utils/stats'
import { formatTime } from '../utils/formatTime'
import styles from './TimeGraph.module.css'

interface TimeGraphProps {
    solves: Solve[]
    maxPoints?: number
}

const PAD_LEFT = 42
const PAD_RIGHT = 8
const PAD_TOP = 8
const PAD_BOTTOM = 8
const VIEW_W = 300
const VIEW_H = 90
const PLOT_W = VIEW_W - PAD_LEFT - PAD_RIGHT
const PLOT_H = VIEW_H - PAD_TOP - PAD_BOTTOM

export function TimeGraph({ solves, maxPoints = 50 }: TimeGraphProps) {
    // Take last N, reverse to oldest-first for display
    const display = solves.slice(0, maxPoints).reverse()
    const n = display.length

    if (n < 2) {
        return (
            <div className={styles.container}>
                <div className={styles.title}>Time Trend</div>
                <div className={styles.empty}>Need at least 2 solves</div>
            </div>
        )
    }

    const times = display.map(s => effectiveTime(s))
    const validTimes = times.filter(t => t !== Infinity)

    if (validTimes.length === 0) {
        return (
            <div className={styles.container}>
                <div className={styles.title}>Time Trend</div>
                <div className={styles.empty}>No valid times to plot</div>
            </div>
        )
    }

    const minT = Math.min(...validTimes)
    const maxT = Math.max(...validTimes)
    const rangeT = maxT - minT || 1000  // avoid division by zero

    function toX(i: number): number {
        return PAD_LEFT + (i / (n - 1)) * PLOT_W
    }

    function toY(t: number): number {
        return PAD_TOP + (1 - (t - minT) / rangeT) * PLOT_H
    }

    // Build SVG path segments (break on DNF)
    const segments: string[] = []
    let currentPath = ''
    for (let i = 0; i < n; i++) {
        if (times[i] === Infinity) {
            if (currentPath) segments.push(currentPath)
            currentPath = ''
        } else {
            const x = toX(i)
            const y = toY(times[i])
            currentPath += currentPath ? ` L ${x.toFixed(1)} ${y.toFixed(1)}` : `M ${x.toFixed(1)} ${y.toFixed(1)}`
        }
    }
    if (currentPath) segments.push(currentPath)

    // Y-axis labels: min and max
    const yLabelMin = formatTime(minT)
    const yLabelMax = formatTime(maxT)

    return (
        <div className={styles.container}>
            <div className={styles.title}>Time Trend (last {n})</div>
            <svg
                className={styles.svg}
                viewBox={`0 0 ${VIEW_W} ${VIEW_H}`}
                preserveAspectRatio="none"
            >
                {/* Grid line at mid-point */}
                <line
                    x1={PAD_LEFT} y1={PAD_TOP + PLOT_H / 2}
                    x2={VIEW_W - PAD_RIGHT} y2={PAD_TOP + PLOT_H / 2}
                    stroke="rgba(255,255,255,0.06)" strokeWidth="1"
                />

                {/* Y-axis labels */}
                <text x={PAD_LEFT - 3} y={PAD_TOP + 4} textAnchor="end"
                    fontSize="7" fill="rgba(255,255,255,0.4)">{yLabelMax}</text>
                <text x={PAD_LEFT - 3} y={PAD_TOP + PLOT_H} textAnchor="end"
                    fontSize="7" fill="rgba(255,255,255,0.4)">{yLabelMin}</text>

                {/* Time line segments */}
                {segments.map((d, i) => (
                    <path key={i} d={d} fill="none" stroke="var(--accent)" strokeWidth="1.5" />
                ))}

                {/* Data points */}
                {times.map((t, i) => {
                    if (t === Infinity) {
                        const x = toX(i)
                        const y = PAD_TOP + PLOT_H / 2
                        return (
                            <g key={i}>
                                <line x1={x - 3} y1={y - 3} x2={x + 3} y2={y + 3}
                                    stroke="var(--danger)" strokeWidth="1.5" />
                                <line x1={x + 3} y1={y - 3} x2={x - 3} y2={y + 3}
                                    stroke="var(--danger)" strokeWidth="1.5" />
                            </g>
                        )
                    }
                    return (
                        <circle key={i} cx={toX(i)} cy={toY(t)} r="2"
                            fill="var(--accent)" />
                    )
                })}
            </svg>
        </div>
    )
}
