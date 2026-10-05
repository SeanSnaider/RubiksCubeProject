/**
 * The "enter your cube" half of Solve mode: a color palette and an editable
 * net the user paints to match their physical cube.
 *
 * Props:
 * - `cube` / `onChange` — the cube being entered; the parent owns it so it
 *   survives switching to the solution view and back.
 * - `onSolve` — called when the user asks for a solution.
 * - `solving` — a solve is in flight; the Solve button is disabled.
 * - `solverStatus` — whether the background solver is still warming up.
 * - `problems` — messages from the last failed solve attempt, shown under the net.
 * - `active` — whether Solve mode is the visible tab; keyboard shortcuts only
 *   apply while it is.
 *
 * Side effects: while active, listens on `window` for the 0–6 palette shortcuts.
 */
import { useCallback, useEffect, useState } from 'react'
import type { EditableCube, FaceName, Sticker } from '../types'
import { CubeNet } from './CubeNet'
import { ColorPalette } from './ColorPalette'
import { ALL_COLORS } from '../utils/colors'
import { countBlankStickers, countColors, createBlankCube, setSticker, toEditable } from '../utils/editableCube'
import { applyMoves, getSolvedState } from '../utils/cubeMoves'
import { generateScramble } from '../utils/scramble'
import { shouldIgnoreShortcut } from '../utils/keyboard'
import styles from './SolveMode.module.css'

/** State of the background solver, as shown to the user. */
export type SolverStatus = 'loading' | 'ready' | 'error'

/** Props for {@link CubeEntry}. */
export interface CubeEntryProps {
    cube: EditableCube
    onChange: (cube: EditableCube) => void
    onSolve: () => void
    solving: boolean
    solverStatus: SolverStatus
    problems: string[]
    active: boolean
}

/** Stickers the user can paint: 54 minus the six fixed centers. */
const PAINTABLE_STICKERS = 48

/** Status line text for each solver state. */
const SOLVER_STATUS_TEXT: Record<SolverStatus, string> = {
    loading: 'Preparing the solver (takes a second the first time)…',
    ready: 'Solver ready.',
    error: 'The solver failed to load. Try reloading the page.',
}

/**
 * Render the palette, the editable net, and the entry actions.
 *
 * @param props - See {@link CubeEntryProps}.
 * @returns The cube entry panel.
 */
export function CubeEntry({ cube, onChange, onSolve, solving, solverStatus, problems, active }: CubeEntryProps) {
    const [brush, setBrush] = useState<Sticker>(ALL_COLORS[0])

    const blanks = countBlankStickers(cube)

    /**
     * Paint the clicked sticker with the current brush.
     *
     * @param face - Face of the clicked sticker.
     * @param row - Its row, 0–2.
     * @param col - Its column, 0–2.
     */
    function handleStickerClick(face: FaceName, row: number, col: number) {
        onChange(setSticker(cube, face, row, col, brush))
    }

    /** Fill the net with a random, solvable cube, for trying the solver out. */
    function fillRandom() {
        onChange(toEditable(applyMoves(getSolvedState(), generateScramble())))
    }

    /** Clear every sticker except the fixed centers, after confirming. */
    function clearAll() {
        if (blanks === PAINTABLE_STICKERS || window.confirm('Clear every sticker you have entered?')) {
            onChange(createBlankCube())
        }
    }

    // 1–6 pick a color, 0 picks the eraser.
    const handleKeyDown = useCallback((event: KeyboardEvent) => {
        if (!active || shouldIgnoreShortcut(event)) return
        if (event.key === '0') {
            setBrush(null)
        } else if (/^[1-6]$/.test(event.key)) {
            setBrush(ALL_COLORS[Number(event.key) - 1])
        }
    }, [active])

    useEffect(() => {
        window.addEventListener('keydown', handleKeyDown)
        return () => window.removeEventListener('keydown', handleKeyDown)
    }, [handleKeyDown])

    return (
        <div className={styles.panel}>
            <div className={styles.instructions}>
                <h2 className={styles.heading}>Enter your cube</h2>
                <p>
                    Hold your cube with the <b>white center on top</b> and the <b>green center facing you</b>.
                    Pick a color, then click stickers to paint them. Turn the cube to see the left, right and
                    back faces, keeping white on top; tip it toward you to see the bottom.
                </p>
            </div>

            <ColorPalette selected={brush} onSelect={setBrush} counts={countColors(cube)} />

            <CubeNet cube={cube} onStickerClick={handleStickerClick} label="Cube to solve (editable)" />

            {problems.length > 0 && (
                <div className={styles.problems} role="alert">
                    <div className={styles.problemsTitle}>This cube can't be solved as entered:</div>
                    <ul>
                        {problems.map(problem => <li key={problem}>{problem}</li>)}
                    </ul>
                </div>
            )}

            <div className={styles.controls}>
                <button
                    type="button"
                    className={`${styles.btn} ${styles.btnPrimary}`}
                    onClick={onSolve}
                    disabled={solving || solverStatus === 'error'}
                >
                    {solving ? 'Solving…' : blanks > 0 ? `Solve (${blanks} blank)` : 'Solve'}
                </button>
                <button type="button" className={`${styles.btn} ${styles.btnSecondary}`} onClick={fillRandom}>
                    Random cube
                </button>
                <button type="button" className={`${styles.btn} ${styles.btnSecondary}`} onClick={clearAll}>
                    Clear
                </button>
            </div>

            <div className={`${styles.status} ${solverStatus === 'error' ? styles.statusError : ''}`}>
                {SOLVER_STATUS_TEXT[solverStatus]}
            </div>
        </div>
    )
}
