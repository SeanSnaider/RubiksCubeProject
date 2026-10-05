/**
 * The "follow the solution" half of Solve mode: shows the cube after each move
 * and lets the user step through the solution one move at a time.
 *
 * Props:
 * - `start` — the cube as entered, before any solution move.
 * - `moves` — the solution, in standard notation.
 * - `onEdit` — go back to editing the entered cube.
 * - `onNewCube` — discard this cube and start entering a fresh one.
 * - `active` — whether Solve mode is the visible tab; keyboard shortcuts only
 *   apply while it is.
 *
 * The step position is local state. Give the component a new `key` when the
 * solution changes so the position resets to the start.
 *
 * Side effects: while active, listens on `window` for ←/→/Home/End.
 */
import { useCallback, useEffect, useMemo, useState } from 'react'
import type { CubeState } from '../types'
import { Cube3D } from './Cube3D'
import { CubeNet } from './CubeNet'
import { applyMove } from '../utils/cubeMoves'
import { describeMove } from '../utils/moveDescriptions'
import { shouldIgnoreShortcut } from '../utils/keyboard'
import styles from './SolveMode.module.css'

/** Props for {@link SolutionStepper}. */
export interface SolutionStepperProps {
    start: CubeState
    moves: string[]
    onEdit: () => void
    onNewCube: () => void
    active: boolean
}

/**
 * Compute the cube after each prefix of the solution.
 *
 * @param start - The cube before any move.
 * @param moves - The solution.
 * @returns `moves.length + 1` states; entry `i` is the cube after `i` moves.
 */
function statesAlong(start: CubeState, moves: string[]): CubeState[] {
    const states = [start]
    for (const move of moves) states.push(applyMove(states[states.length - 1], move))
    return states
}

/**
 * Render the solution view.
 *
 * @param props - See {@link SolutionStepperProps}.
 * @returns The cube views, the move list and the step controls.
 */
export function SolutionStepper({ start, moves, onEdit, onNewCube, active }: SolutionStepperProps) {
    // How many moves have been applied: 0 (entered cube) to moves.length (solved).
    const [step, setStep] = useState(0)
    const states = useMemo(() => statesAlong(start, moves), [start, moves])
    const total = moves.length
    const done = step === total

    const goTo = useCallback((target: number) => {
        setStep(Math.max(0, Math.min(total, target)))
    }, [total])

    const handleKeyDown = useCallback((event: KeyboardEvent) => {
        if (!active || shouldIgnoreShortcut(event)) return
        const targets: Record<string, number> = {
            ArrowRight: step + 1,
            ArrowLeft: step - 1,
            Home: 0,
            End: total,
        }
        if (event.key in targets) {
            event.preventDefault()
            goTo(targets[event.key])
        }
    }, [active, step, total, goTo])

    useEffect(() => {
        window.addEventListener('keydown', handleKeyDown)
        return () => window.removeEventListener('keydown', handleKeyDown)
    }, [handleKeyDown])

    return (
        <div className={styles.panel}>
            <div className={styles.instructions}>
                <h2 className={styles.heading}>
                    {total === 0 ? 'Already solved' : `Solution: ${total} moves`}
                </h2>
                <p>
                    Keep the <b>white center on top</b> and the <b>green center facing you</b> the whole
                    time, and do each move on your cube before pressing Next.
                </p>
            </div>

            <div className={styles.current} aria-live="polite">
                {done ? (
                    <span className={styles.currentDone}>
                        {total === 0 ? 'This cube is already solved.' : '✓ Solved! Every move is done.'}
                    </span>
                ) : (
                    <>
                        <span className={styles.currentLabel}>Move {step + 1} of {total}</span>
                        <span className={styles.currentMove}>{moves[step]}</span>
                        <span className={styles.currentText}>{describeMove(moves[step])}</span>
                    </>
                )}
            </div>

            {total > 0 && (
                <ol className={styles.moveList} aria-label="Solution moves">
                    {moves.map((move, index) => {
                        const state = index < step ? styles.moveDone : index === step ? styles.moveNext : ''
                        return (
                            <li key={index}>
                                <button
                                    type="button"
                                    className={`${styles.moveChip} ${state}`}
                                    onClick={() => goTo(index)}
                                    title={`Jump to move ${index + 1}`}
                                    aria-current={index === step ? 'step' : undefined}
                                >
                                    {move}
                                </button>
                            </li>
                        )
                    })}
                </ol>
            )}

            <div className={styles.controls}>
                <button type="button" className={`${styles.btn} ${styles.btnSecondary}`} onClick={() => goTo(0)} disabled={step === 0}>
                    ⏮ Start
                </button>
                <button type="button" className={`${styles.btn} ${styles.btnSecondary}`} onClick={() => goTo(step - 1)} disabled={step === 0}>
                    ← Previous
                </button>
                <button type="button" className={`${styles.btn} ${styles.btnPrimary}`} onClick={() => goTo(step + 1)} disabled={done}>
                    Next →
                </button>
                <button type="button" className={`${styles.btn} ${styles.btnSecondary}`} onClick={() => goTo(total)} disabled={done}>
                    End ⏭
                </button>
            </div>
            <div className={styles.status}>Keyboard: ← / → to step, Home / End to jump.</div>

            <div className={styles.views}>
                <Cube3D state={states[step]} />
                <CubeNet cube={states[step]} label={`Cube after ${step} of ${total} moves`} />
            </div>

            <div className={styles.controls}>
                <button type="button" className={`${styles.btn} ${styles.btnSecondary}`} onClick={onEdit}>
                    Edit entered cube
                </button>
                <button type="button" className={`${styles.btn} ${styles.btnSecondary}`} onClick={onNewCube}>
                    Enter a new cube
                </button>
            </div>
        </div>
    )
}
