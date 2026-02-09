export function formatTime(timeMs: number) {

    let seconds: number = timeMs / 1000
    let minutes: number = Math.floor(seconds / 60)
    seconds = seconds % 60
    let result: string = seconds.toFixed(2)

    // seconds logic where i check to make sure its not just a single digit and ugly ui
    if (seconds < 10) {
        result = result.padStart(5, '0')
    }

    // logic for when the time is above a minute (would never be me right?)
    if (minutes > 0) {
        result = minutes + ":" + result
    }

    return result
}