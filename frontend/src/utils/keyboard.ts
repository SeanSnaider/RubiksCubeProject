/**
 * Shared filtering for the app's global keyboard shortcuts.
 *
 * Cube and Learn mode listen for single letter keys on `window`. Without a
 * filter they would swallow browser shortcuts (Ctrl+R, Ctrl+C, Cmd+L), keys
 * typed into a text field, and the flood of repeats a held key produces.
 */

/**
 * Decide whether a keydown should be left alone by a global move shortcut.
 *
 * @param event - The keydown event.
 * @returns True if the key has a modifier (other than Shift), is an
 *   auto-repeat from a held key, or was typed into an editable element.
 */
export function shouldIgnoreShortcut(event: KeyboardEvent): boolean {
    if (event.ctrlKey || event.metaKey || event.altKey) return true
    if (event.repeat) return true
    const target = event.target
    if (target instanceof HTMLElement) {
        if (target.isContentEditable) return true
        const tag = target.tagName
        if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return true
    }
    return false
}
