import React, { useState } from 'react'
import { KEY_MAP } from '../utils/keymap'
import styles from './KeyboardHelp.module.css'

// Group the keymap into sections for display
const SECTIONS: { title: string; keys: string[] }[] = [
    { title: 'Basic Moves', keys: ['j', 'f', 'i', 'k', 'h', 'g', 's', 'l', 'd', 'e', 'w', 'o'] },
    { title: 'Slice Moves', keys: ['x', '.', '5', '6', '2', '9', '1', '0'] },
    { title: 'Wide Moves', keys: ['u', 'm', 'r', 'v', ',', 'c', 'z', '/'] },
    { title: 'Rotations', keys: ['t', 'b', ';', 'a', 'p', 'q'] },
]

export function KeyboardHelp() {
    const [open, setOpen] = useState(false)

    return (
        <>
            <button className={styles.toggle} onClick={() => setOpen(o => !o)} title="Keyboard shortcuts">
                ?
            </button>
            {open && (
                <div className={styles.overlay}>
                    <div className={styles.heading}>Keyboard Controls</div>
                    {SECTIONS.map(section => (
                        <div key={section.title} className={styles.section}>
                            <div className={styles.sectionTitle}>{section.title}</div>
                            <div className={styles.bindings}>
                                {section.keys.map(key => (
                                    <React.Fragment key={key}>
                                        <span className={styles.key}>{key}</span>
                                        <span className={styles.move}>{KEY_MAP[key]}</span>
                                    </React.Fragment>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </>
    )
}
