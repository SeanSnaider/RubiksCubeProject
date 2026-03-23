import { useState } from 'react'
import type { Solve } from '../types'
import { formatTime } from '../utils/formatTime'
import { effectiveTime } from '../utils/stats'
import styles from './SolveRow.module.css'

interface SolveRowProps {
    solve: Solve
    index: number
    onDelete: (id: string) => void
    onPenalty: (id: string, penalty: '+2' | 'DNF' | null) => void
}

export function SolveRow({ solve, index, onDelete, onPenalty }: SolveRowProps) {
    const [open, setOpen] = useState(false)

    const displayTime = formatTime(effectiveTime(solve))
    const date = new Date(solve.created_at).toLocaleString()

    function togglePenalty(p: '+2' | 'DNF') {
        onPenalty(solve._id, solve.penalty === p ? null : p)
    }

    function handleDelete() {
        if (window.confirm('Delete this solve?')) {
            onDelete(solve._id)
        }
    }

    return (
        <div className={styles.row}>
            <div className={styles.header} onClick={() => setOpen(o => !o)}>
                <span className={styles.index}>{index}.</span>
                <span className={styles.time}>{displayTime}</span>
                {solve.penalty === '+2' && (
                    <span className={`${styles.badge} ${styles.badgePlus2}`}>+2</span>
                )}
                {solve.penalty === 'DNF' && (
                    <span className={`${styles.badge} ${styles.badgeDnf}`}>DNF</span>
                )}
                <span className={`${styles.chevron} ${open ? styles.chevronOpen : ''}`}>▶</span>
            </div>

            {open && (
                <div className={styles.details}>
                    <div className={styles.scramble}>{solve.scramble}</div>
                    <div className={styles.date}>{date}</div>
                    <div className={styles.actions}>
                        <button
                            className={`${styles.penaltyBtn} ${solve.penalty === '+2' ? styles.penaltyBtnActive : ''}`}
                            onClick={() => togglePenalty('+2')}
                        >
                            +2
                        </button>
                        <button
                            className={`${styles.penaltyBtn} ${solve.penalty === 'DNF' ? styles.penaltyBtnActive : ''}`}
                            onClick={() => togglePenalty('DNF')}
                        >
                            DNF
                        </button>
                        <button className={styles.deleteBtn} onClick={handleDelete}>
                            Delete
                        </button>
                    </div>
                </div>
            )}
        </div>
    )
}
