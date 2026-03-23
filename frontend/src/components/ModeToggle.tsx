import styles from './ModeToggle.module.css'

interface ModeToggleProps {
    mode: 'cube' | 'timer' | 'learn'
    onChange: (mode: 'cube' | 'timer' | 'learn') => void
}

export function ModeToggle({ mode, onChange }: ModeToggleProps) {
    return (
        <div className={styles.container}>
            <button
                className={`${styles.tab} ${mode === 'cube' ? styles.active : ''}`}
                onClick={() => onChange('cube')}
            >
                Cube
            </button>
            <button
                className={`${styles.tab} ${mode === 'timer' ? styles.active : ''}`}
                onClick={() => onChange('timer')}
            >
                Timer
            </button>
            <button
                className={`${styles.tab} ${mode === 'learn' ? styles.active : ''}`}
                onClick={() => onChange('learn')}
            >
                Learn
            </button>
        </div>
    )
}
