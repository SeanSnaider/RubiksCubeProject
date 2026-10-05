/**
 * Flat, unfolded view of all 54 stickers, laid out as the standard cross:
 *
 *            Top
 *     Left  Front  Right  Back
 *           Bottom
 *
 * Unlike `Cube3D`, every sticker is visible, which makes it the view for
 * entering a cube by hand and for checking the whole state at a glance.
 *
 * Each face is drawn as you would see it by turning the cube to face it with
 * white kept on top; the top face is seen from above with the front edge
 * nearest the front face, and the bottom face from below with the front edge
 * nearest the front face. This matches the face layout of `CubeState`.
 *
 * Props:
 * - `cube` — the stickers to show; blank (null) stickers are drawn gray.
 * - `onStickerClick` — if given, every non-center sticker becomes a button
 *   that calls it. Omit it for a read-only view.
 * - `label` — accessible name for the whole net.
 *
 * Renders only; holds no state and has no side effects.
 */
import type { EditableCube, FaceName } from '../types'
import { BLANK_FILL, COLOR_NAME, FACE_POSITION_NAME, STICKER_FILL, STICKER_TEXT } from '../utils/colors'
import { isCenter } from '../utils/editableCube'
import styles from './CubeNet.module.css'

/** Grid cell (column, row) of each face in the cross layout, 1-based. */
const FACE_GRID_POSITION: Record<FaceName, { column: number; row: number }> = {
    U: { column: 2, row: 1 },
    L: { column: 1, row: 2 },
    F: { column: 2, row: 2 },
    R: { column: 3, row: 2 },
    B: { column: 4, row: 2 },
    D: { column: 2, row: 3 },
}

/** Props for {@link CubeNet}. */
export interface CubeNetProps {
    /** The stickers to display. */
    cube: EditableCube
    /** Called with a sticker's position when it is clicked. Omit for read-only. */
    onStickerClick?: (face: FaceName, row: number, col: number) => void
    /** Accessible name for the net. */
    label: string
}

/**
 * Render the unfolded cube.
 *
 * @param props - See {@link CubeNetProps}.
 * @returns The net as a grid of six 3x3 faces.
 */
export function CubeNet({ cube, onStickerClick, label }: CubeNetProps) {
    return (
        <div className={styles.net} role="group" aria-label={label}>
            {(Object.keys(FACE_GRID_POSITION) as FaceName[]).map(face => (
                <div
                    key={face}
                    className={styles.face}
                    style={{
                        gridColumn: FACE_GRID_POSITION[face].column,
                        gridRow: FACE_GRID_POSITION[face].row,
                    }}
                >
                    {cube[face].map((rowStickers, row) =>
                        rowStickers.map((sticker, col) => {
                            const fill = sticker === null ? BLANK_FILL : STICKER_FILL[sticker]
                            const colorName = sticker === null ? 'blank' : COLOR_NAME[sticker]
                            const position = `${FACE_POSITION_NAME[face]} face, row ${row + 1}, column ${col + 1}`

                            if (isCenter(row, col)) {
                                return (
                                    <div
                                        key={`${row}-${col}`}
                                        className={`${styles.sticker} ${styles.center}`}
                                        style={{ backgroundColor: fill, color: sticker ? STICKER_TEXT[sticker] : undefined }}
                                        title={`${FACE_POSITION_NAME[face]} center (${colorName}, fixed)`}
                                    >
                                        {FACE_POSITION_NAME[face]}
                                    </div>
                                )
                            }
                            if (onStickerClick) {
                                return (
                                    <button
                                        key={`${row}-${col}`}
                                        type="button"
                                        className={`${styles.sticker} ${styles.editable} ${sticker === null ? styles.blank : ''}`}
                                        style={{ backgroundColor: fill }}
                                        aria-label={`${position}: ${colorName}`}
                                        onClick={() => onStickerClick(face, row, col)}
                                    />
                                )
                            }
                            return (
                                <div
                                    key={`${row}-${col}`}
                                    className={`${styles.sticker} ${sticker === null ? styles.blank : ''}`}
                                    style={{ backgroundColor: fill }}
                                    title={`${position}: ${colorName}`}
                                />
                            )
                        }),
                    )}
                </div>
            ))}
        </div>
    )
}
