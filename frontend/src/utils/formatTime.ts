export function formatTime(timeMs: number): string {
    if (timeMs === Infinity) return 'DNF'

    let seconds: number = timeMs / 1000
    let minutes: number = Math.floor(seconds / 60)
    seconds = seconds % 60
    let result: string = seconds.toFixed(2)

    if (seconds < 10) {
        result = result.padStart(5, '0')
    }

    if (minutes > 0) {
        result = minutes + ':' + result
    }

    return result
}
