import { useState, useRef, useCallback } from 'react'

type TimerState = 'idle' | 'running' | 'stopped'

// the hook for this wubiks cubix
export function useTimer() {

    const [timeMs, setTimeMs] = useState<number>(0);
    const [timerState, setTimerState] = useState<TimerState>('idle'); 

    // starting constant values
    const startTimeRef = useRef<number>(0);
    const animationFrameRef = useRef<number>(0);

    // tick function (useCallback)
    const tick = useCallback(() => {
        let elapsed: number = performance.now() - startTimeRef.current
        setTimeMs(elapsed)

        // continue looping through the project
        animationFrameRef.current = requestAnimationFrame(tick)
    }, []);

    // start function (useCallback)
    const start = useCallback(() => {
        startTimeRef.current = performance.now()
        setTimerState('running')
        setTimeMs(0)

        // start the loop
        animationFrameRef.current = requestAnimationFrame(tick)
    }, [tick])

    // stop function (useCallback)
    const stop = useCallback(() => {
        cancelAnimationFrame(animationFrameRef.current)
        setTimerState('stopped')
    }, [])

    // reset function (useCallback)
    const reset = useCallback(() => {
        cancelAnimationFrame(animationFrameRef.current)
        setTimerState('idle')
        setTimeMs(0)
    }, [])

    // return statement
    return { timeMs, timerState, start, stop, reset };
}