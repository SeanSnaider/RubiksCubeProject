/**
 * Bar above the Cube mode cube showing the current scramble, with buttons to
 * copy it and to deal a new one.
 *
 * Props: `scramble` (the text to show) and `onNewScramble` (deal another).
 */
import { useState } from 'react'
import styles from './ScrambleBar.module.css'

interface ScrambleBarProps {
    scramble: string
    onNewScramble: () => void
}

export function ScrambleBar({ scramble, onNewScramble }: ScrambleBarProps) {
    const [copied, setCopied] = useState(false)

    /** Copy the scramble to the clipboard and briefly confirm it. */
    function handleCopy() {
        if (!navigator.clipboard) {
            // Clipboard API needs a secure context (https or localhost).
            window.prompt('Copy the scramble:', scramble)
            return
        }
        navigator.clipboard.writeText(scramble)
            .then(() => {
                setCopied(true)
                setTimeout(() => setCopied(false), 1500)
            })
            .catch((error: unknown) => {
                console.error('Could not copy the scramble', error)
                window.prompt('Copy the scramble:', scramble)
            })
    }

    return (
        <div className={styles.bar}>
            <span className={styles.scramble}>{scramble}</span>
            <div className={styles.actions}>
                <button
                    className={`${styles.iconBtn} ${copied ? styles.copied : ''}`}
                    onClick={handleCopy}
                    title="Copy scramble"
                >
                    {copied ? '✓ Copied' : 'Copy'}
                </button>
                <button
                    className={styles.iconBtn}
                    onClick={onNewScramble}
                    title="Generate new scramble"
                >
                    New
                </button>
            </div>
        </div>
    )
}
