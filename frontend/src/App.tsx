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
import { fetchScramble, applyMove } from './utils/api'
import {
    getTimerSolves, addTimerSolve, removeTimerSolve, setTimerPenalty,
    getCubeSolves, addCubeSolve, removeCubeSolve, setCubePenalty,
} from './utils/timerStorage'
import { KEY_MAP } from './utils/keymap'
import { useTimer } from './hooks/useTimer'
import { useSpacebarTimer } from './hooks/useSpacebarTimer'
import { isSolved } from './utils/isSolved'

const solvedCube: CubeState = {
    U: [['U','U','U'], ['U','U','U'], ['U','U','U']],
    D: [['D','D','D'], ['D','D','D'], ['D','D','D']],
    L: [['L','L','L'], ['L','L','L'], ['L','L','L']],
    R: [['R','R','R'], ['R','R','R'], ['R','R','R']],
    F: [['F','F','F'], ['F','F','F'], ['F','F','F']],
    B: [['B','B','B'], ['B','B','B'], ['B','B','B']],
}

// Whole-cube rotations — should not start the timer
const ROTATION_MOVES = new Set(['x', "x'", 'x2', 'y', "y'", 'y2', 'z', "z'", 'z2'])

function App() {
    const [mode, setMode] = useState<'cube' | 'timer' | 'learn'>('cube')

    // ── Learn mode ───────────────────────────────────────────────────────
    const [learnCubeState, setLearnCubeState] = useState<CubeState>(solvedCube)

    // ── Cube mode ──────────────────────────────────────────────────────────
    const { timeMs, timerState, start, stop, reset } = useTimer()
    const [scramble, setScramble] = useState<string>(generateScramble())
    const [cubeState, setCubeState] = useState<CubeState>(solvedCube)
    const [cubeSolves, setCubeSolves] = useState<Solve[]>(() => getCubeSolves())

    // Ref so the keydown closure always sees the latest timerState without re-registering
    const timerStateRef = useRef(timerState)
    useEffect(() => { timerStateRef.current = timerState }, [timerState])

    const timeMsRef = useRef(timeMs)
    useEffect(() => { timeMsRef.current = timeMs }, [timeMs])

    const scrambleRef = useRef(scramble)
    useEffect(() => { scrambleRef.current = scramble }, [scramble])

    function refreshCubeSolves() {
        setCubeSolves(getCubeSolves())
    }

    async function newScramble() {
        const data = await fetchScramble()
        setScramble(data.scramble)
        setCubeState(data.state)
    }

    // ── Timer mode ─────────────────────────────────────────────────────────
    const [timerSolves, setTimerSolves] = useState<Solve[]>(() => getTimerSolves())

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
    function handleDelete(id: string) {
        if (mode === 'cube') {
            removeCubeSolve(id)
            refreshCubeSolves()
        } else {
            removeTimerSolve(id)
            refreshTimerSolves()
        }
    }

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
        if (mode !== 'cube') return
        if (!(event.key in KEY_MAP)) return

        event.preventDefault()
        const move = KEY_MAP[event.key]
        const isRotation = ROTATION_MOVES.has(move)

        if (!isRotation) {
            if (timerStateRef.current === 'idle') start()
            if (timerStateRef.current === 'stopped') reset()
        }

        applyMove(cubeState, move).then(newState => {
            setCubeState(newState)
            if (!isRotation && isSolved(newState)) {
                stop()
                addCubeSolve(timeMsRef.current, scrambleRef.current)
                refreshCubeSolves()
                newScramble()
            }
        })
    }, [mode, cubeState, start, stop, reset])

    useEffect(() => {
        window.addEventListener('keydown', handleKeyDown)
        return () => window.removeEventListener('keydown', handleKeyDown)
    }, [handleKeyDown])

    // ── Render ─────────────────────────────────────────────────────────────
    const solves = mode === 'cube' ? cubeSolves : timerSolves
    const lastSolve = cubeSolves[0] ?? null

    return (
        <div className="app-layout">
            <div className="sidebar" style={{ backgroundColor: 'var(--bg-sidebar)' }}>
                <ModeToggle mode={mode} onChange={setMode} />
                {mode !== 'learn' && (
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
                    <div style={{ padding: 'var(--space-3)', color: 'var(--text-muted)', fontSize: '0.85em', lineHeight: 1.6 }}>
                        <h3 style={{ color: 'var(--accent)', margin: '0 0 var(--space-2)' }}>Keyboard Controls</h3>
                        <div><b>R / R'</b> — i / k</div>
                        <div><b>L / L'</b> — d / e</div>
                        <div><b>U / U'</b> — j / f</div>
                        <div><b>F / F'</b> — h / g</div>
                        <div><b>D / D'</b> — s / l</div>
                        <div><b>B / B'</b> — w / o</div>
                        <div style={{ marginTop: 'var(--space-2)' }}><b>x / x'</b> — t / b</div>
                        <div><b>y / y'</b> — ; / a</div>
                        <div><b>z / z'</b> — p / q</div>
                    </div>
                )}
            </div>

            <div className="main-content">
                {mode === 'cube' ? (
                    <>
                        <ScrambleBar scramble={scramble} onNewScramble={newScramble} />
                        <div style={{ padding: '20px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                            <Cube3D state={cubeState} />
                            <Timer time_ms={timeMs} timerState={timerState} lastSolve={lastSolve} />
                        </div>
                    </>
                ) : mode === 'timer' ? (
                    <SpacebarTimer
                        spaceState={spaceState}
                        timeMs={spaceTimeMs}
                        holdProgress={holdProgress}
                    />
                ) : (
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
