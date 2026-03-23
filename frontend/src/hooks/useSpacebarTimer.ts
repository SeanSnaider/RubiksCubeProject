import { useState, useRef, useCallback, useEffect } from 'react'

export type SpaceTimerState = 'idle' | 'holding' | 'ready' | 'running' | 'stopped'

const HOLD_MS = 3000

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

    function setState(s: SpaceTimerState) {
        stateRef.current = s
        setSpaceStateRaw(s)
    }

    function holdTick() {
        setHoldMs(performance.now() - holdStartRef.current)
        holdRafRef.current = requestAnimationFrame(holdTick)
    }

    function runTick() {
        const elapsed = performance.now() - startTimeRef.current
        setTimeMs(elapsed)
        finalTimeRef.current = elapsed
        rafRef.current = requestAnimationFrame(runTick)
    }

    function cancelHold() {
        if (holdTimeoutRef.current) clearTimeout(holdTimeoutRef.current)
        cancelAnimationFrame(holdRafRef.current)
        setHoldMs(0)
    }

    const handleKeyDown = useCallback((e: KeyboardEvent) => {
        if (!enabled || e.code !== 'Space' || e.repeat) return
        e.preventDefault()

        const s = stateRef.current
        if (s === 'idle') {
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
            cancelHold()
            startTimeRef.current = performance.now()
            setTimeMs(0)
            finalTimeRef.current = 0
            rafRef.current = requestAnimationFrame(runTick)
            setState('running')
        }
    }, [enabled])

    useEffect(() => {
        window.addEventListener('keydown', handleKeyDown)
        window.addEventListener('keyup', handleKeyUp)
        return () => {
            window.removeEventListener('keydown', handleKeyDown)
            window.removeEventListener('keyup', handleKeyUp)
            cancelAnimationFrame(rafRef.current)
            cancelAnimationFrame(holdRafRef.current)
            if (holdTimeoutRef.current) clearTimeout(holdTimeoutRef.current)
        }
    }, [handleKeyDown, handleKeyUp])

    // Reset state when disabled (mode switch)
    useEffect(() => {
        if (!enabled) {
            cancelAnimationFrame(rafRef.current)
            cancelAnimationFrame(holdRafRef.current)
            if (holdTimeoutRef.current) clearTimeout(holdTimeoutRef.current)
            setState('idle')
            setTimeMs(0)
            setHoldMs(0)
        }
    }, [enabled])

    return {
        spaceState,
        timeMs,
        holdProgress: Math.min(holdMs / HOLD_MS, 1),
    }
}
