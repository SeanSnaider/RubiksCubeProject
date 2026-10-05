/**
 * Tab bar at the top of the sidebar for switching between the app's modes.
 *
 * Props:
 * - `mode` — the active mode, shown highlighted.
 * - `onChange` — called with the mode the user clicked.
 *
 * Renders only; no state or side effects.
 */
import type { AppMode } from '../types'
import styles from './ModeToggle.module.css'

/** Props for {@link ModeToggle}. */
interface ModeToggleProps {
    mode: AppMode
    onChange: (mode: AppMode) => void
}

/** Tabs in display order, with their labels and tooltips. */
const TABS: { mode: AppMode; label: string; description: string }[] = [
    { mode: 'cube', label: 'Cube', description: 'Solve a virtual cube with the keyboard' },
    { mode: 'timer', label: 'Timer', description: 'Time solves on a physical cube' },
    { mode: 'learn', label: 'Learn', description: 'Step-by-step beginner tutorial' },
    { mode: 'solve', label: 'Solve', description: 'Enter your cube\'s colors and follow a solution' },
]

/**
 * Render the mode tabs.
 *
 * @param props - See {@link ModeToggleProps}.
 * @returns A row of tab buttons.
 */
export function ModeToggle({ mode, onChange }: ModeToggleProps) {
    return (
        <div className={styles.container} role="tablist">
            {TABS.map(tab => (
                <button
                    key={tab.mode}
                    type="button"
                    role="tab"
                    aria-selected={mode === tab.mode}
                    className={`${styles.tab} ${mode === tab.mode ? styles.active : ''}`}
                    onClick={() => onChange(tab.mode)}
                    title={tab.description}
                >
                    {tab.label}
                </button>
            ))}
        </div>
    )
}
