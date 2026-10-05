/**
 * Formatting of solve times for display.
 */

/** Milliseconds per hundredth of a second, the precision times are shown at. */
const MS_PER_CENTISECOND = 10
const CENTISECONDS_PER_SECOND = 100
const SECONDS_PER_MINUTE = 60

/**
 * Format a time the way cubing timers do: `9.87`, `12.34`, `1:05.43`.
 *
 * Times are truncated to hundredths rather than rounded, as WCA timing is, so
 * 59.999s shows as `59.99`, never `60.00`.
 *
 * @param timeMs - The time in milliseconds, or `Infinity` for a DNF.
 * @returns The formatted time, or `"DNF"`.
 */
export function formatTime(timeMs: number): string {
    if (timeMs === Infinity) return 'DNF'

    const totalCentiseconds = Math.floor(Math.max(0, timeMs) / MS_PER_CENTISECOND)
    const centiseconds = totalCentiseconds % CENTISECONDS_PER_SECOND
    const totalSeconds = Math.floor(totalCentiseconds / CENTISECONDS_PER_SECOND)
    const seconds = totalSeconds % SECONDS_PER_MINUTE
    const minutes = Math.floor(totalSeconds / SECONDS_PER_MINUTE)

    const fraction = String(centiseconds).padStart(2, '0')
    if (minutes === 0) return `${seconds}.${fraction}`
    return `${minutes}:${String(seconds).padStart(2, '0')}.${fraction}`
}
