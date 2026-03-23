import type { Solve } from '../types'
import { SolveRow } from './SolveRow'
import styles from './SolveList.module.css'

interface SolveListProps {
    solves: Solve[]
    onDelete: (id: string) => void
    onPenalty: (id: string, penalty: '+2' | 'DNF' | null) => void
}

export function SolveList({ solves, onDelete, onPenalty }: SolveListProps) {
    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <span className={styles.title}>Solves</span>
                <span className={styles.count}>{solves.length} total</span>
            </div>
            <div className={styles.list}>
                {solves.length === 0 ? (
                    <div className={styles.empty}>No solves yet</div>
                ) : (
                    solves.map((solve, i) => (
                        <SolveRow
                            key={solve._id}
                            solve={solve}
                            index={i + 1}
                            onDelete={onDelete}
                            onPenalty={onPenalty}
                        />
                    ))
                )}
            </div>
        </div>
    )
}
