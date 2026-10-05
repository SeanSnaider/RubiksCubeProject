/**
 * Color picker for painting stickers in Solve mode.
 *
 * Shows one swatch per color plus an eraser, each with its keyboard shortcut,
 * and how many stickers of that color have been placed out of the nine a real
 * cube has, so a miscount is visible before the user asks for a solve.
 *
 * Props:
 * - `selected` — the current brush: a color, or null for the eraser.
 * - `onSelect` — called with the brush the user picked.
 * - `counts` — stickers placed per color, centers included.
 *
 * Renders only; the keyboard shortcuts themselves are handled by `SolveMode`.
 */
import type { Color, Sticker } from '../types'
import { ALL_COLORS, BLANK_FILL, COLOR_NAME, STICKER_FILL } from '../utils/colors'
import styles from './ColorPalette.module.css'

/** Number of stickers of each color on a real cube. */
const STICKERS_PER_COLOR = 9

/** Props for {@link ColorPalette}. */
export interface ColorPaletteProps {
    /** The active brush; null means the eraser. */
    selected: Sticker
    /** Called when the user picks a brush. */
    onSelect: (brush: Sticker) => void
    /** Stickers placed so far, per color. */
    counts: Record<Color, number>
}

/**
 * Keyboard shortcut for each brush, in display order: 1–6 for the colors and
 * 0 for the eraser.
 *
 * @param index - Position of the swatch in `ALL_COLORS`, or -1 for the eraser.
 * @returns The key to show on the swatch.
 */
function paletteShortcut(index: number): string {
    return index === -1 ? '0' : String(index + 1)
}

/**
 * Render the palette.
 *
 * @param props - See {@link ColorPaletteProps}.
 * @returns A row of swatch buttons.
 */
export function ColorPalette({ selected, onSelect, counts }: ColorPaletteProps) {
    return (
        <div className={styles.palette} role="radiogroup" aria-label="Sticker color">
            {ALL_COLORS.map((color, index) => {
                const count = counts[color]
                const countClass = count > STICKERS_PER_COLOR
                    ? styles.countOver
                    : count === STICKERS_PER_COLOR ? styles.countDone : ''
                return (
                    <button
                        key={color}
                        type="button"
                        role="radio"
                        aria-checked={selected === color}
                        className={`${styles.swatch} ${selected === color ? styles.selected : ''}`}
                        onClick={() => onSelect(color)}
                        title={`${COLOR_NAME[color]} (key ${paletteShortcut(index)})`}
                    >
                        <span className={styles.chip} style={{ backgroundColor: STICKER_FILL[color] }} />
                        <span className={styles.name}>{COLOR_NAME[color]}</span>
                        <span className={`${styles.count} ${countClass}`}>{count}/{STICKERS_PER_COLOR}</span>
                        <kbd className={styles.key}>{paletteShortcut(index)}</kbd>
                    </button>
                )
            })}
            <button
                type="button"
                role="radio"
                aria-checked={selected === null}
                className={`${styles.swatch} ${selected === null ? styles.selected : ''}`}
                onClick={() => onSelect(null)}
                title={`Eraser (key ${paletteShortcut(-1)})`}
            >
                <span className={`${styles.chip} ${styles.eraserChip}`} style={{ backgroundColor: BLANK_FILL }} />
                <span className={styles.name}>Eraser</span>
                <span className={styles.count} />
                <kbd className={styles.key}>{paletteShortcut(-1)}</kbd>
            </button>
        </div>
    )
}
