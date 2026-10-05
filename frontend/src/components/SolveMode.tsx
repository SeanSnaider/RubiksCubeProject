/**
 * Solve mode: enter the colors of a physical cube, get a Kociemba two-phase
 * solution, and follow it one move at a time.
 *
 * Owns the entered cube and the current solution, and switches between the
 * two halves of the mode: `CubeEntry` (painting the cube) and
 * `SolutionStepper` (following the solution). Solving runs in a Web Worker
 * through `solverClient`, so the page stays responsive throughout.
 *
 * Props:
 * - `active` — whether Solve mode is the visible tab. The parent keeps this
 *   component mounted while hidden so the entered cube isn't lost when the
 *   user switches tabs; `active` gates the keyboard shortcuts and triggers
 *   loading the solver the first time the tab is opened.
 *
 * Side effects: starts the solver worker on first activation.
 */
import { useEffect, useRef, useState } from 'react'
import type { CubeState, EditableCube } from '../types'
import { CubeEntry, type SolverStatus } from './CubeEntry'
import { SolutionStepper } from './SolutionStepper'
import { createBlankCube, isComplete } from '../utils/editableCube'
import { findCubeProblems } from '../utils/cubeValidation'
import { CubeProblemsError, prepareSolver, solveCube } from '../solver/solverClient'
import styles from './SolveMode.module.css'

/** Props for {@link SolveMode}. */
export interface SolveModeProps {
    active: boolean
}

/** A solution together with the cube it solves. */
interface Solution {
    start: CubeState
    moves: string[]
    /** Distinguishes successive solutions, so the stepper resets for each. */
    id: number
}

/**
 * Render Solve mode.
 *
 * @param props - See {@link SolveModeProps}.
 * @returns The entry panel, or the solution stepper once a solution exists.
 */
export function SolveMode({ active }: SolveModeProps) {
    const [cube, setCube] = useState<EditableCube>(createBlankCube)
    const [solution, setSolution] = useState<Solution | null>(null)
    const [problems, setProblems] = useState<string[]>([])
    const [solving, setSolving] = useState(false)
    const [solverStatus, setSolverStatus] = useState<SolverStatus>('loading')
    const solverRequested = useRef(false)
    const nextSolutionId = useRef(1)

    // Warm the solver up the first time the tab is opened, not on page load,
    // so people who only use the timer never pay for it.
    useEffect(() => {
        if (!active || solverRequested.current) return
        solverRequested.current = true
        prepareSolver()
            .then(() => setSolverStatus('ready'))
            .catch((error: unknown) => {
                console.error('Failed to prepare the solver', error)
                setSolverStatus('error')
            })
    }, [active])

    /**
     * Replace the entered cube, clearing problems that may no longer apply.
     *
     * @param next - The updated cube.
     */
    function handleCubeChange(next: EditableCube) {
        setCube(next)
        setProblems([])
    }

    /** Validate the entered cube and, if it is solvable, solve it in the worker. */
    async function handleSolve() {
        const found = findCubeProblems(cube)
        if (found.length > 0 || !isComplete(cube)) {
            setProblems(found)
            return
        }
        setSolving(true)
        setProblems([])
        try {
            const moves = await solveCube(cube)
            setSolution({ start: cube, moves, id: nextSolutionId.current++ })
        } catch (error) {
            if (error instanceof CubeProblemsError) {
                setProblems(error.problems)
            } else {
                console.error('Solver failed', error)
                setProblems([`The solver failed unexpectedly: ${error instanceof Error ? error.message : String(error)}`])
            }
        } finally {
            setSolving(false)
        }
    }

    /** Discard the solution and the entered cube, and start from a blank cube. */
    function startNewCube() {
        setSolution(null)
        setCube(createBlankCube())
        setProblems([])
    }

    return (
        <div className={styles.container}>
            {solution ? (
                <SolutionStepper
                    key={solution.id}
                    start={solution.start}
                    moves={solution.moves}
                    onEdit={() => setSolution(null)}
                    onNewCube={startNewCube}
                    active={active}
                />
            ) : (
                <CubeEntry
                    cube={cube}
                    onChange={handleCubeChange}
                    onSolve={handleSolve}
                    solving={solving}
                    solverStatus={solverStatus}
                    problems={problems}
                    active={active}
                />
            )}
        </div>
    )
}
