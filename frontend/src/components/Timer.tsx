import { formatTime } from '../utils/formatTime'

interface TimerProps {
    time_ms: number
    timerState: string
}

// function which holds some of the fun stuff with my custom hook (argh)
export function Timer({ time_ms, timerState }: TimerProps) {

    const color = timerState === 'running' ? 'lime' : 'white'

    // weturn statement :3
    return (
    <div>
        <div style={{ color, fontSize: '48px' }}>
            <div>
                {formatTime(time_ms)}
            </div>
        </div>
    </div>
    )
}