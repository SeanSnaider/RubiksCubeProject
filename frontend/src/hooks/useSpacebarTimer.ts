/**
 * Hold-to-arm spacebar timer for Timer mode (solves on a physical cube).
 *
 * Holding Space for `HOLD_MS` arms the timer; releasing starts it; pressing
 * Space again stops it and saves the time; one more press resets the display.
 * Releasing early cancels the hold.
 */
import { useState, useRef, useCallback, useEffect } from 'react'

export type SpaceTimerState = 'idle' | 'holding' | 'ready' | 'running' | 'stopped'

const HOLD_MS = 3000

/**
 * Drive the spacebar timer.
 *
 * @param enabled - Whether Timer mode is active. Key events are ignored and the
 *   timer resets while false.
 * @param onSave - Called with the final time in milliseconds when a solve stops.
 * @returns `spaceState`, the elapsed `timeMs`, and `holdProgress` (0–1) for the
 *   arming ring.
 */
export function useSpacebarTimer(enabled: boolean, onSave: (timeMs: number) => void) {
    const [spaceState, setSpaceStateRaw] = useState<SpaceTimerState>('idle')
    const [timeMs, setTimeMs] = useState(0)
    const [holdMs, setHoldMs] = useState(0)

    // Refs so event handlers always see current values without re-registering
    const stateRef = useRef<SpaceTimerState>('idle')
    const startTimeRef = useRef(0)
    const holdStartRef = useRef(0)
    const rafRef = useRef(0)
    const holdRafRef = useRef(0)
    const holdTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null)
    const finalTimeRef = useRef(0)
    const onSaveRef = useRef(onSave)
    useEffect(() => { onSaveRef.current = onSave }, [onSave])

    /** Update the state and its synchronous ref together. */
    function setState(s: SpaceTimerState) {
        stateRef.current = s
        setSpaceStateRaw(s)
    }

    /** Abort an in-progress hold and clear the arming ring. */
    function cancelHold() {
        if (holdTimeoutRef.current) clearTimeout(holdTimeoutRef.current)
        cancelAnimationFrame(holdRafRef.current)
        setHoldMs(0)
    }

    const handleKeyDown = useCallback((e: KeyboardEvent) => {
        if (!enabled || e.code !== 'Space' || e.repeat) return
        e.preventDefault()

        // Space would otherwise also "click" whichever button was last clicked
        // (a penalty toggle or Delete in the solve list) when the key is released.
        if (document.activeElement instanceof HTMLElement) document.activeElement.blur()

        const s = stateRef.current
        if (s === 'idle') {
            const holdTick = () => {
                setHoldMs(performance.now() - holdStartRef.current)
                holdRafRef.current = requestAnimationFrame(holdTick)
            }
            holdStartRef.current = performance.now()
            holdRafRef.current = requestAnimationFrame(holdTick)
            holdTimeoutRef.current = setTimeout(() => {
                cancelAnimationFrame(holdRafRef.current)
                setHoldMs(HOLD_MS)
                setState('ready')
            }, HOLD_MS)
            setState('holding')
        } else if (s === 'running') {
            cancelAnimationFrame(rafRef.current)
            onSaveRef.current(finalTimeRef.current)
            setState('stopped')
        } else if (s === 'stopped') {
            setTimeMs(0)
            setState('idle')
        }
    }, [enabled])

    const handleKeyUp = useCallback((e: KeyboardEvent) => {
        if (!enabled || e.code !== 'Space') return
        e.preventDefault()

        const s = stateRef.current
        if (s === 'holding') {
            cancelHold()
            setState('idle')
        } else if (s === 'ready') {
            const runTick = () => {
                const elapsed = performance.now() - startTimeRef.current
                setTimeMs(elapsed)
                finalTimeRef.current = elapsed
                rafRef.current = requestAnimationFrame(runTick)
            }
            cancelHold()
            startTimeRef.current = performance.now()
            setTimeMs(0)
            finalTimeRef.current = 0
            rafRef.current = requestAnimationFrame(runTick)
            setState('running')
        }
    }, [enabled])

    // Listen only while enabled. Leaving Timer mode runs the cleanup, which
    // also abandons any hold or run in progress so the timer comes back idle.
    useEffect(() => {
        if (!enabled) return
        window.addEventListener('keydown', handleKeyDown)
        window.addEventListener('keyup', handleKeyUp)
        return () => {
            window.removeEventListener('keydown', handleKeyDown)
            window.removeEventListener('keyup', handleKeyUp)
            cancelAnimationFrame(rafRef.current)
            cancelAnimationFrame(holdRafRef.current)
            if (holdTimeoutRef.current) clearTimeout(holdTimeoutRef.current)
            setState('idle')
            setTimeMs(0)
            setHoldMs(0)
        }
    }, [enabled, handleKeyDown, handleKeyUp])

    return {
        spaceState,
        timeMs,
        holdProgress: Math.min(holdMs / HOLD_MS, 1),
    }
}
