/**
 * Root component: the sidebar (mode tabs, stats, solve history) and the main
 * area for whichever mode is active.
 *
 * Modes:
 * - Cube  — solve a scrambled virtual cube with the keyboard; the timer starts
 *           on the first turn and stops when the cube is solved.
 * - Timer — spacebar timer for solves on a physical cube.
 * - Learn — guided beginner tutorial (`LearnMode`).
 *
 * Cube mode's state lives here. Learn mode's cube is lifted here too, so
 * switching tabs never loses work.
 *
 * Side effects: listens on `window` for Cube mode's move keys; reads and
 * writes solve history in localStorage (via `timerStorage`).
 */
import './App.css'
import { Cube3D } from './components/Cube3D'
import type { CubeState, Solve } from './types'
import { Timer } from './components/Timer'
import { ScrambleBar } from './components/ScrambleBar'
import { StatsPanel } from './components/StatsPanel'
import { SolveList } from './components/SolveList'
import { TimeGraph } from './components/TimeGraph'
import { KeyboardHelp } from './components/KeyboardHelp'
import { ModeToggle } from './components/ModeToggle'
import { SpacebarTimer } from './components/SpacebarTimer'
import { LearnMode } from './components/LearnMode'
import { generateScramble } from './utils/scramble'
import { useState, useCallback, useEffect, useRef } from 'react'
import { applyMove, applyMoves, getSolvedState } from './utils/cubeMoves'
import {
    getTimerSolves, addTimerSolve, removeTimerSolve, setTimerPenalty,
    getCubeSolves, addCubeSolve, removeCubeSolve, setCubePenalty,
} from './utils/timerStorage'
import { KEY_MAP } from './utils/keymap'
import { shouldIgnoreShortcut } from './utils/keyboard'
import { useTimer } from './hooks/useTimer'
import { useSpacebarTimer } from './hooks/useSpacebarTimer'
import { isSolved } from './utils/isSolved'

const solvedCube: CubeState = getSolvedState()

// Whole-cube rotations — should not start the timer
const ROTATION_MOVES = new Set(['x', "x'", 'x2', 'y', "y'", 'y2', 'z', "z'", 'z2'])

// How long the finished cube stays on screen after a solve before the next
// scramble replaces it. Moves used to be applied server-side, so the round trip
// left the solved cube visible for a moment; now that they are instant, that
// pause has to be deliberate or the solve would never be seen.
const SOLVED_PAUSE_MS = 800

/**
 * Render the whole app.
 *
 * @returns The sidebar, the active mode's main view, and the keyboard help button.
 */
function App() {
    const [mode, setMode] = useState<'cube' | 'timer' | 'learn'>('cube')

    // ── Learn mode ───────────────────────────────────────────────────────
    const [learnCubeState, setLearnCubeState] = useState<CubeState>(solvedCube)

    // ── Cube mode ──────────────────────────────────────────────────────────
    const { timeMs, timerState, start, stop, reset } = useTimer()
    // The first scramble and the cube it produces are created together, so the
    // cube on screen always matches the scramble shown above it.
    const [initialScramble] = useState(generateScramble)
    const [scramble, setScramble] = useState<string>(initialScramble)
    const [cubeState, setCubeState] = useState<CubeState>(() => applyMoves(solvedCube, initialScramble))
    const [cubeSolves, setCubeSolves] = useState<Solve[]>(() => getCubeSolves())

    // Ref so the keydown closure always sees the latest timerState without
    // re-registering. Also written synchronously on start, so two keypresses in
    // the same frame don't both try to start the timer.
    const timerStateRef = useRef(timerState)
    useEffect(() => { timerStateRef.current = timerState }, [timerState])

    const scrambleRef = useRef(scramble)
    useEffect(() => { scrambleRef.current = scramble }, [scramble])

    // Mirrors cubeState, but updated synchronously on every change. React batches
    // state updates until the next render, so several keypresses within one frame
    // would otherwise all read the same stale cube and lose all but the last move.
    const cubeStateRef = useRef(cubeState)

    /**
     * Set the cube to a new state, keeping the synchronous mirror in step.
     *
     * @param next - The state to display. Always a fresh object, never mutated.
     */
    const commitCubeState = useCallback((next: CubeState) => {
        cubeStateRef.current = next
        setCubeState(next)
    }, [])

    /** Reload Cube mode's history from storage after it changes. */
    function refreshCubeSolves() {
        setCubeSolves(getCubeSolves())
    }

    // Pending post-solve scramble. While it is set the solved cube is on show
    // and move keys are ignored, so a stray keypress can't unsolve it.
    const nextScrambleTimeoutRef = useRef<number | null>(null)

    /**
     * Deal a new scramble. Abandons an attempt in progress, so its time isn't
     * carried over into the next solve.
     */
    const newScramble = useCallback(() => {
        if (nextScrambleTimeoutRef.current !== null) {
            clearTimeout(nextScrambleTimeoutRef.current)
            nextScrambleTimeoutRef.current = null
        }
        if (timerStateRef.current === 'running') reset()
        const next = generateScramble()
        setScramble(next)
        commitCubeState(applyMoves(solvedCube, next))
    }, [commitCubeState, reset])

    // ── Timer mode ─────────────────────────────────────────────────────────
    const [timerSolves, setTimerSolves] = useState<Solve[]>(() => getTimerSolves())

    /** Reload Timer mode's history from storage after it changes. */
    function refreshTimerSolves() {
        setTimerSolves(getTimerSolves())
    }

    const handleTimerSave = useCallback((ms: number) => {
        addTimerSolve(Math.round(ms))
        refreshTimerSolves()
    }, [])

    const { spaceState, timeMs: spaceTimeMs, holdProgress } = useSpacebarTimer(
        mode === 'timer',
        handleTimerSave
    )

    // ── Shared delete / penalty ────────────────────────────────────────────
    /**
     * Delete a solve from the active mode's history.
     *
     * @param id - The solve's id.
     */
    function handleDelete(id: string) {
        if (mode === 'cube') {
            removeCubeSolve(id)
            refreshCubeSolves()
        } else {
            removeTimerSolve(id)
            refreshTimerSolves()
        }
    }

    /**
     * Set or clear a penalty on a solve in the active mode's history.
     *
     * @param id - The solve's id.
     * @param penalty - The new penalty, or null to clear it.
     */
    function handlePenalty(id: string, penalty: '+2' | 'DNF' | null) {
        if (mode === 'cube') {
            setCubePenalty(id, penalty)
            refreshCubeSolves()
        } else {
            setTimerPenalty(id, penalty)
            refreshTimerSolves()
        }
    }

    // ── Cube keyboard handler ──────────────────────────────────────────────
    const handleKeyDown = useCallback((event: KeyboardEvent) => {
        if (mode !== 'cube' || shouldIgnoreShortcut(event)) return
        if (!(event.key in KEY_MAP)) return

        event.preventDefault()
        // Showing off a just-solved cube; the next scramble is on its way.
        if (nextScrambleTimeoutRef.current !== null) return

        const move = KEY_MAP[event.key]
        const isRotation = ROTATION_MOVES.has(move)

        // Any turn starts a fresh attempt unless one is already being timed,
        // including the first turn after a finished solve.
        if (!isRotation && timerStateRef.current !== 'running') {
            start()
            timerStateRef.current = 'running'
        }

        // Applied locally and synchronously so the cube turns in the same frame
        // as the keypress, with no network round trip in between.
        const newState = applyMove(cubeStateRef.current, move)
        commitCubeState(newState)

        if (!isRotation && isSolved(newState)) {
            const finalMs = stop()
            timerStateRef.current = 'stopped'
            addCubeSolve(Math.round(finalMs), scrambleRef.current)
            refreshCubeSolves()
            // Leave the solved cube up briefly before scrambling it again.
            nextScrambleTimeoutRef.current = window.setTimeout(newScramble, SOLVED_PAUSE_MS)
        }
    }, [mode, start, stop, commitCubeState, newScramble])

    // Don't scramble a cube that is no longer mounted
    useEffect(() => () => {
        if (nextScrambleTimeoutRef.current !== null) {
            clearTimeout(nextScrambleTimeoutRef.current)
        }
    }, [])

    useEffect(() => {
        window.addEventListener('keydown', handleKeyDown)
        return () => window.removeEventListener('keydown', handleKeyDown)
    }, [handleKeyDown])

    // ── Render ─────────────────────────────────────────────────────────────
    const solves = mode === 'cube' ? cubeSolves : timerSolves
    const lastSolve = cubeSolves[0] ?? null
    const showsHistory = mode === 'cube' || mode === 'timer'

    return (
        <div className="app-layout">
            <div className="sidebar" style={{ backgroundColor: 'var(--bg-sidebar)' }}>
                <ModeToggle mode={mode} onChange={setMode} />
                {showsHistory && (
                    <>
                        <StatsPanel solves={solves} />
                        <TimeGraph solves={solves} />
                        <SolveList
                            solves={solves}
                            onDelete={handleDelete}
                            onPenalty={handlePenalty}
                        />
                    </>
                )}
                {mode === 'learn' && (
                    <div className="sidebar-help">
                        <h3>Keyboard Controls</h3>
                        <div><b>R / R'</b> — i / k</div>
                        <div><b>L / L'</b> — d / e</div>
                        <div><b>U / U'</b> — j / f</div>
                        <div><b>F / F'</b> — h / g</div>
                        <div><b>D / D'</b> — s / l</div>
                        <div><b>B / B'</b> — w / o</div>
                        <div className="sidebar-help-gap"><b>x / x'</b> — t / b</div>
                        <div><b>y / y'</b> — ; / a</div>
                        <div><b>z / z'</b> — p / q</div>
                        <div className="sidebar-help-gap">Press <b>?</b> (bottom right) for every key.</div>
                    </div>
                )}
            </div>

            <div className="main-content">
                {mode === 'cube' && (
                    <>
                        <ScrambleBar scramble={scramble} onNewScramble={newScramble} />
                        <div style={{ padding: '20px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                            <Cube3D state={cubeState} />
                            <Timer time_ms={timeMs} timerState={timerState} lastSolve={lastSolve} />
                        </div>
                    </>
                )}
                {mode === 'timer' && (
                    <SpacebarTimer
                        spaceState={spaceState}
                        timeMs={spaceTimeMs}
                        holdProgress={holdProgress}
                    />
                )}
                {mode === 'learn' && (
                    <LearnMode
                        cubeState={learnCubeState}
                        setCubeState={setLearnCubeState}
                        active={mode === 'learn'}
                    />
                )}
            </div>

            <KeyboardHelp />
        </div>
    )
}

export default App
