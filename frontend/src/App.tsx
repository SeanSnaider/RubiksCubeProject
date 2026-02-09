import { Cube3D } from './components/Cube3D';
import type { CubeState, Solve } from './types';
import { Timer } from './components/Timer';
import { generateScramble } from './utils/scramble'
import { useState, useCallback, useEffect } from 'react';
import { fetchScramble, applyMove, fetchSolves } from './utils/api';
import { SolveList } from './components/SolveList';
import { KEY_MAP } from './utils/keymap'
import { useTimer } from './hooks/useTimer';
import { isSolved } from './utils/isSolved';
import { saveSolve } from './utils/api'

// A solved cube for testing
const solvedCube: CubeState = {
  U: [['U','U','U'], ['U','U','U'], ['U','U','U']],
  D: [['D','D','D'], ['D','D','D'], ['D','D','D']],
  L: [['L','L','L'], ['L','L','L'], ['L','L','L']],
  R: [['R','R','R'], ['R','R','R'], ['R','R','R']],
  F: [['F','F','F'], ['F','F','F'], ['F','F','F']],
  B: [['B','B','B'], ['B','B','B'], ['B','B','B']],
};


function App() {

  const { timeMs, timerState, start, stop, reset } = useTimer();
  

  // general useState for generating a scramble and storing its state
  const [scramble, setScramble] = useState<string>(generateScramble())
  const [cubeState, setCubeState] = useState<CubeState>(solvedCube)
  const [solves, setSolves] = useState<Solve[]>([])

  // basic react callback to set the scramble using the function that i made
  async function newScramble() {
    const data = await fetchScramble()
    setScramble(data.scramble)
    setCubeState(data.state)
  }

  //basic call to fetch the solves
  async function loadSolves() {
    const data = await fetchSolves()
    setSolves(data)
  }

  useEffect(() => {loadSolves() }, [])

  const handleKeyDown = useCallback((event: KeyboardEvent) => {
    if (event.key in KEY_MAP) {
        event.preventDefault()
        if (timerState === 'idle') {
          start()
        }
        if (timerState === 'stopped') {
          reset()
        }
        applyMove(cubeState, KEY_MAP[event.key]).then(newState => {
          setCubeState(newState)
        if (isSolved(newState)) {
          stop()
          saveSolve(timeMs, scramble)
          loadSolves()
          newScramble()
        }})

    }}, [cubeState, timerState, start, stop, reset, timeMs, scramble])

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown)
    return () => {
        window.removeEventListener('keydown', handleKeyDown)
    }
  }, [handleKeyDown])

  return (
    <div style={{ display: 'flex', height: '100vh' }}>

      {/* Left sidebar - solve list */}
      <div style={{ width: '280px', padding: '10px', overflowY: 'auto',
            borderRight: '1px solid rgba(255,255,255,0.1)' }}>
        <SolveList solves={solves} />
      </div>

      {/* Main content - centered */}
      <div style={{ flex: 1, textAlign: 'center' }}>
        <div style={{ fontSize: '18px',
              backgroundColor: 'rgba(0, 0, 0, 0.7)',
              padding: '10px' }}>
          {scramble}
        </div>
        <div style={{ padding: '20px' }}>
          <Cube3D state={cubeState} />
          <Timer time_ms={timeMs} timerState={timerState} />
        </div>
      </div>

    </div>
  );
}

export default App;
