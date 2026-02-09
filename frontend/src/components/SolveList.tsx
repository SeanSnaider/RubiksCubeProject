import type { Solve } from '../types/index'
import { formatTime } from '../utils/formatTime'
import { calcAo5, calcAo12, calcBest, calcMean } from '../utils/stats'

interface SolveListProps {
    solves: Solve[]
}

function showStat(val: number | null) {
    if (val !== null) {
        return formatTime(val)
    } else {
        return '--'
    }
}

// function which holds some of the fun stuff with my custom hook (argh)
export function SolveList({ solves }: SolveListProps) {

    // weturn statement :3
    return (
    <div>
        <h3>Statistics</h3>
            <div>Best: {showStat(calcBest(solves))} 
                | Ao5: {showStat(calcAo5(solves))}
                | Ao12: {showStat(calcAo12(solves))}
                | Mean: {showStat(calcMean(solves))}</div>
            
            <h3>Solves</h3>
            <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
                {solves.map((solve, index) => (
                <div key={solve._id}>
                    {index + 1}. {formatTime(solve.time_ms)}
                </div>
                ))}
            </div>
        </div>
    )
}