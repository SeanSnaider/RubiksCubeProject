import { useState } from 'react'
import styles from './ScrambleBar.module.css'

interface ScrambleBarProps {
    scramble: string
    onNewScramble: () => void
}

export function ScrambleBar({ scramble, onNewScramble }: ScrambleBarProps) {
    const [copied, setCopied] = useState(false)

    function handleCopy() {
        navigator.clipboard.writeText(scramble).then(() => {
            setCopied(true)
            setTimeout(() => setCopied(false), 1500)
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
