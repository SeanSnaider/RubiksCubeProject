/**
 * Stopwatch hook used by Cube mode, driven by `requestAnimationFrame`.
 *
 * The timer is started and stopped imperatively (by the first move and by the
 * solving move), and `timeMs` re-renders the display every frame while running.
 */
import { useState, useRef, useCallback, useEffect } from 'react'

/** Lifecycle of the stopwatch. */
export type TimerState = 'idle' | 'running' | 'stopped'

/**
 * Provide a start/stop/reset stopwatch.
 *
 * @returns `timeMs` (elapsed time to display), `timerState`, and the
 *   `start`, `stop` and `reset` controls. `stop()` returns the exact final time,
 *   which is what should be recorded: `timeMs` may lag it by up to one frame.
 */
export function useTimer() {
    const [timeMs, setTimeMs] = useState<number>(0)
    const [timerState, setTimerState] = useState<TimerState>('idle')

    const startTimeRef = useRef<number>(0)
    const animationFrameRef = useRef<number>(0)

    /** Start (or restart) timing from zero. */
    const start = useCallback(() => {
        cancelAnimationFrame(animationFrameRef.current)
        startTimeRef.current = performance.now()
        setTimerState('running')
        setTimeMs(0)

        const tick = () => {
            setTimeMs(performance.now() - startTimeRef.current)
            animationFrameRef.current = requestAnimationFrame(tick)
        }
        animationFrameRef.current = requestAnimationFrame(tick)
    }, [])

    /**
     * Stop timing and freeze the display on the final time.
     *
     * @returns The elapsed time in milliseconds.
     */
    const stop = useCallback((): number => {
        cancelAnimationFrame(animationFrameRef.current)
        const elapsed = performance.now() - startTimeRef.current
        setTimeMs(elapsed)
        setTimerState('stopped')
        return elapsed
    }, [])

    /** Stop timing and clear the display back to zero. */
    const reset = useCallback(() => {
        cancelAnimationFrame(animationFrameRef.current)
        setTimerState('idle')
        setTimeMs(0)
    }, [])

    // Don't leave an animation loop running after unmount.
    useEffect(() => () => cancelAnimationFrame(animationFrameRef.current), [])

    return { timeMs, timerState, start, stop, reset }
}
