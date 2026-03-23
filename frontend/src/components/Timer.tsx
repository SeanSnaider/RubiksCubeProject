import { formatTime } from '../utils/formatTime'
import type { Solve } from '../types'
import styles from './Timer.module.css'

interface TimerProps {
    time_ms: number
    timerState: string
    lastSolve?: Solve | null
}

export function Timer({ time_ms, timerState, lastSolve }: TimerProps) {
    const isRunning = timerState === 'running'

    return (
        <div className={styles.container}>
            <div className={`${styles.time} ${isRunning ? styles.running : ''}`}>
                {formatTime(time_ms)}
            </div>
            {lastSolve?.penalty === '+2' && (
                <div className={`${styles.penalty} ${styles.penaltyPlus2}`}>+2</div>
            )}
            {lastSolve?.penalty === 'DNF' && (
                <div className={`${styles.penalty} ${styles.penaltyDnf}`}>DNF</div>
            )}
            {timerState === 'idle' && (
                <div className={styles.hint}>Press a move key to start</div>
            )}
        </div>
    )
}
