import type { SpaceTimerState } from '../hooks/useSpacebarTimer'
import { formatTime } from '../utils/formatTime'
import styles from './SpacebarTimer.module.css'

interface SpacebarTimerProps {
    spaceState: SpaceTimerState
    timeMs: number
    holdProgress: number  // 0–1
}

const RADIUS = 68
const CIRCUMFERENCE = 2 * Math.PI * RADIUS

const HINTS: Record<SpaceTimerState, string> = {
    idle: 'Hold Space for 3 seconds to arm',
    holding: 'Keep holding...',
    ready: 'Release to start!',
    running: 'Press Space to stop',
    stopped: 'Press Space to reset',
}

export function SpacebarTimer({ spaceState, timeMs, holdProgress }: SpacebarTimerProps) {
    const dashOffset = CIRCUMFERENCE * (1 - holdProgress)

    const timeClass = [
        styles.time,
        spaceState === 'running' ? styles.running : '',
        spaceState === 'ready' ? styles.ready : '',
        spaceState === 'holding' ? styles.holding : '',
    ].filter(Boolean).join(' ')

    const ringClass = [
        styles.ringFill,
        spaceState === 'ready' ? styles.ready : '',
        spaceState === 'holding' ? styles.holding : '',
    ].filter(Boolean).join(' ')

    const showRing = spaceState === 'holding' || spaceState === 'ready'

    return (
        <div className={styles.container}>
            {showRing ? (
                <div className={styles.ring}>
                    <svg width="160" height="160" viewBox="0 0 160 160">
                        <circle
                            className={styles.ringTrack}
                            cx="80" cy="80" r={RADIUS}
                            fill="none" strokeWidth="6"
                        />
                        <circle
                            className={ringClass}
                            cx="80" cy="80" r={RADIUS}
                            fill="none" strokeWidth="6"
                            strokeDasharray={CIRCUMFERENCE}
                            strokeDashoffset={dashOffset}
                        />
                    </svg>
                    <div className={styles.ringLabel}>
                        <span className={timeClass}>
                            {spaceState === 'ready' ? '✓' : `${Math.ceil(3 - holdProgress * 3)}s`}
                        </span>
                    </div>
                </div>
            ) : (
                <div className={timeClass}>
                    {formatTime(timeMs)}
                </div>
            )}

            <div className={spaceState === 'ready' ? styles.hintReady : styles.hint}>
                {HINTS[spaceState]}
            </div>
        </div>
    )
}
