import { useState, useCallback, useEffect, useRef } from 'react'
import { Cube3D } from './Cube3D'
import type { CubeState } from '../types'
import { applyMove } from '../utils/api'
import { KEY_MAP } from '../utils/keymap'
import {
    isFlowerComplete,
    isCrossComplete,
    isFirstLayerComplete,
    isSecondLayerComplete,
    isYellowCrossComplete,
    isOLLComplete,
    isCPLLComplete,
    isCubeSolved,
} from '../utils/cubeChecks'
import { fetchScramble } from '../utils/api'
import styles from './LearnMode.module.css'

const TOTAL_STEPS = 42

interface Step {
    phase: string
    text: string[]
    algorithm?: string
    tip?: string[]
    /** If set, user must achieve this check before advancing */
    gateCheck?: (s: CubeState) => boolean
    /** Auto-scramble when entering this step */
    scrambleOnEnter?: boolean
}

const STEPS: Step[] = [
    // Step 0 — welcome
    {
        phase: 'Introduction',
        text: [
            "Welcome to the Rubik's Cube learning tool! This guided tutorial will teach you how to solve a Rubik's Cube step by step using the layer-by-layer (beginner's) method.",
            "You'll start by learning the basic notation and moves, then work through each phase of the solve. Use the same keyboard controls as Cube mode to manipulate the cube.",
            "Click \"Next\" to begin!",
        ],
    },
    // Step 1 — notation intro
    {
        phase: 'Notation',
        text: [
            "The first step to solving a Rubik's cube is to learn the notation. The moves I will teach you are the most basic ones: R, L, F, U, D, and B. I will also teach you rotations (x, y, z) that help you reorient the cube.",
            "Although this seems like a lot right now, we'll go through each one individually.",
        ],
    },
    // Step 2 — R move
    {
        phase: 'Notation',
        text: [
            "The first move is R — a clockwise rotation of the right layer (upward). Press 'i' on your keyboard to do an R move.",
            "The inverse, R', is a counterclockwise rotation (downward). Press 'k' for R'.",
            "Try both moves until you're comfortable, then click Next.",
        ],
    },
    // Step 3 — L move
    {
        phase: 'Notation',
        text: [
            "Next is L — a downward movement of the left layer. Press 'd' to do an L move.",
            "The inverse L' moves the left layer upward. Press 'e' for L'.",
            "Practice these, then click Next.",
        ],
    },
    // Step 4 — U move
    {
        phase: 'Notation',
        text: [
            "U moves the top layer clockwise. Press 'j' for U.",
            "U' moves the top layer counterclockwise. Press 'f' for U'.",
            "Practice these, then click Next.",
        ],
    },
    // Step 5 — F move
    {
        phase: 'Notation',
        text: [
            "F rotates the front face clockwise. Press 'h' for F.",
            "F' rotates the front face counterclockwise. Press 'g' for F'.",
            "Practice these, then click Next.",
        ],
    },
    // Step 6 — rotations intro
    {
        phase: 'Notation',
        text: [
            "Now let's learn cube rotations. These rotate the entire cube without changing the relative positions of the stickers.",
            "There are three axes: x, y, and z — each with a normal and inverse (prime) version.",
        ],
    },
    // Step 7 — x rotation
    {
        phase: 'Notation',
        text: [
            "An x rotation tilts the cube forward (like an R move but the whole cube). Press 't' or 'y' for x.",
            "x' tilts the cube backward. Press 'b' or 'n' for x'.",
            "Practice, then click Next.",
        ],
    },
    // Step 8 — y rotation
    {
        phase: 'Notation',
        text: [
            "A y rotation spins the cube clockwise (looking from above, like a U move of the whole cube). Press ';' for y.",
            "y' spins counterclockwise. Press 'a' for y'.",
            "Practice, then click Next.",
        ],
    },
    // Step 9 — z rotation
    {
        phase: 'Notation',
        text: [
            "A z rotation tilts the cube sideways clockwise (like an F move of the whole cube). Press 'p' for z.",
            "z' tilts counterclockwise. Press 'q' for z'.",
            "Now you know all the basic moves and rotations! Let's start solving.",
        ],
    },
    // Step 10 — Flower intro
    {
        phase: 'Step 1 — The Flower',
        text: [
            "The first solving step is creating a 'flower'. This means placing four white edge pieces around the yellow center on the top face.",
            "An edge piece is one with exactly two colored stickers. You want white edges surrounding the yellow center.",
            "There's no single algorithm for this — just experiment! Try to get all four white edges onto the yellow (top) face.",
        ],
        scrambleOnEnter: true,
    },
    // Step 11 — Flower explanation
    {
        phase: 'Step 1 — The Flower',
        text: [
            "The flower should look like a plus/cross shape of white edges on the yellow face. The center stays yellow, and each of the four edge positions (top, bottom, left, right of center) should be white.",
            "Tip: Do an x2 rotation to put the yellow side on top if it isn't already!",
            "Try to create the flower on your scrambled cube, then click Next when you're done.",
        ],
        tip: [
            "Do x2 to put yellow on top",
            "Focus on getting white edges to the top without displacing ones already there",
        ],
        gateCheck: isFlowerComplete,
    },
    // Step 12 — Cross intro
    {
        phase: 'Step 2 — The Cross',
        text: [
            "Great job! Now convert the flower into a white cross on the bottom face.",
            "Look at the center color on each of the four side faces. Rotate the top layer (U moves) until a white edge's second color matches the center below it, then do two F moves (F F or F2) to send it down.",
            "Repeat for all four edges. Click Next when the white cross is on the bottom.",
        ],
        gateCheck: isCrossComplete,
    },
    // Step 13 — First layer corners intro
    {
        phase: 'Step 3 — First Layer Corners',
        text: [
            "Awesome! Now finish the first layer by inserting the four white corners.",
            "Rotate the cube so white is on the bottom (do x2 if needed). Find a white corner piece in the top layer and position it above where it belongs.",
            "There are three cases depending on which way the white sticker faces. Click Next to learn the algorithms.",
        ],
    },
    // Step 14 — Corner case 1: white facing left
    {
        phase: 'Step 3 — First Layer Corners',
        text: [
            "Case 1: The white sticker of the corner is facing you on the LEFT side.",
            "Position the corner above its target slot, then do:",
        ],
        algorithm: "U L' U' L",
        tip: ["This inserts the corner from the left side into the bottom-left slot."],
    },
    // Step 15 — Corner case 2: white facing right
    {
        phase: 'Step 3 — First Layer Corners',
        text: [
            "Case 2: The white sticker of the corner is facing you on the RIGHT side.",
            "Position the corner above its target slot, then do:",
        ],
        algorithm: "U R U' R'",
        tip: ["This inserts the corner from the right side into the bottom-right slot."],
    },
    // Step 16 — Corner case 3: white facing up
    {
        phase: 'Step 3 — First Layer Corners',
        text: [
            "Case 3: The white sticker is facing UP (on the top face).",
            "Place the corner directly above where it needs to go, then repeat this algorithm three times:",
        ],
        algorithm: "(R U R' U') × 3",
        tip: [
            "This is just R U R' U' repeated three times",
            "It rotates the corner in place until white faces down",
        ],
    },
    // Step 17 — First layer practice
    {
        phase: 'Step 3 — First Layer Corners',
        text: [
            "Now solve all four corners to complete the first layer! Use the three algorithms you just learned.",
            "Remember: first position each corner above its slot, check which way white faces, then apply the right algorithm.",
        ],
        tip: [
            "White on left: U L' U' L",
            "White on right: U R U' R'",
            "White on top: (R U R' U') × 3",
        ],
        gateCheck: isFirstLayerComplete,
    },
    // Step 18 — Second layer intro
    {
        phase: 'Step 4 — Second Layer',
        text: [
            "Great work! Now solve the second (middle) layer edges.",
            "Find an edge in the top layer that does NOT have yellow on it. Rotate U until its front color matches the center below it.",
            "Then check: does the top color of that edge match the center to the RIGHT or to the LEFT? Click Next to see both algorithms.",
        ],
    },
    // Step 19 — Edge to the right
    {
        phase: 'Step 4 — Second Layer',
        text: [
            "If the edge needs to go to the RIGHT slot (the top color matches the right-side center):",
        ],
        algorithm: "(U R U' R') (F R' F' R)",
        tip: ["This moves the edge from the top layer into the right slot of the second layer."],
    },
    // Step 20 — Edge to the left
    {
        phase: 'Step 4 — Second Layer',
        text: [
            "If the edge needs to go to the LEFT slot (the top color matches the left-side center):",
        ],
        algorithm: "(U' L' U L) (F' L F L')",
        tip: ["This moves the edge from the top layer into the left slot of the second layer."],
    },
    // Step 21 — Second layer practice
    {
        phase: 'Step 4 — Second Layer',
        text: [
            "Now insert all four second-layer edges! Find each non-yellow edge in the top layer, align it, and use the correct algorithm.",
        ],
        tip: [
            "Edge into right slot: (U R U' R') (F R' F' R)",
            "Edge into left slot: (U' L' U L) (F' L F L')",
        ],
        gateCheck: isSecondLayerComplete,
    },
    // Step 22 — Yellow cross intro
    {
        phase: 'Step 5 — Yellow Cross',
        text: [
            "Amazing! Now for the last layer. First, make all four edges on top yellow to form a yellow cross.",
            "There are three possible cases: no yellow edges, an L-shape (two adjacent), or a line (two opposite). Click Next to see the algorithms.",
        ],
    },
    // Step 23 — Yellow cross: no edges
    {
        phase: 'Step 5 — Yellow Cross',
        text: [
            "Case 1 — No yellow edges (dot): Orient the cube any way and do:",
        ],
        algorithm: "F (U R U' R') F' U' F (R U R' U') F'",
        tip: [
            "This is actually the L-shape algorithm followed immediately by the line algorithm",
            "It converts dot → L → cross in one go",
        ],
    },
    // Step 24 — Yellow cross: L shape
    {
        phase: 'Step 5 — Yellow Cross',
        text: [
            "Case 2 — L-shape (two adjacent yellow edges): Orient the L so the two yellow edges point to the BACK and LEFT, then do:",
        ],
        algorithm: "F (U R U' R') F'",
    },
    // Step 25 — Yellow cross: line
    {
        phase: 'Step 5 — Yellow Cross',
        text: [
            "Case 3 — Line (two opposite yellow edges): Orient the line so it goes LEFT to RIGHT (horizontal), then do:",
        ],
        algorithm: "F (R U R' U') F'",
    },
    // Step 26 — Yellow cross practice
    {
        phase: 'Step 5 — Yellow Cross',
        text: [
            "Now make the yellow cross! Identify which case you have and apply the correct algorithm. Sometimes you'll need to do it in stages (dot → L → cross).",
        ],
        tip: [
            "L-shape: F (U R U' R') F'",
            "Line: F (R U R' U') F'",
            "No edges: F (U R U' R') F' U' F (R U R' U') F'",
        ],
        gateCheck: isYellowCrossComplete,
    },
    // Step 27 — OLL intro (corner orientation)
    {
        phase: 'Step 6 — Orient Last Layer',
        text: [
            "Great job! Now orient the yellow corners so the entire top face is yellow.",
            "You only need two algorithms: the Sune and Anti-Sune. When applying them, make sure one solved corner (yellow on top) is in the front-left, and the front-right corner has yellow facing toward you.",
        ],
    },
    // Step 28 — Sune
    {
        phase: 'Step 6 — Orient Last Layer',
        text: [
            "The Sune: With the solved corner front-left and the front-right corner's yellow facing you, do:",
        ],
        algorithm: "R U R' U R U2 R'",
    },
    // Step 29 — Anti-Sune
    {
        phase: 'Step 6 — Orient Last Layer',
        text: [
            "The Anti-Sune: With the solved corner front-right and the front-left corner's yellow facing you, do:",
        ],
        algorithm: "L' U' L U' L' U2 L",
    },
    // Step 30 — OLL practice
    {
        phase: 'Step 6 — Orient Last Layer',
        text: [
            "Now orient all four yellow corners! Keep applying Sune or Anti-Sune until the entire top face is yellow.",
            "If you don't see a clear Sune/Anti-Sune case, do either one to change the case, then try again.",
        ],
        tip: [
            "Sune: R U R' U R U2 R'",
            "Anti-Sune: L' U' L U' L' U2 L",
        ],
        gateCheck: isOLLComplete,
    },
    // Step 31 — CPLL intro (corner permutation)
    {
        phase: 'Step 7 — Permute Corners',
        text: [
            "Great! Now position the corners correctly. Look for 'headlights' — two corners on the same side that share the same color.",
            "Place the headlights on your LEFT and do the T-perm algorithm. If no headlights exist, do the algorithm from any angle to create them, then repeat.",
        ],
    },
    // Step 32 — T-perm
    {
        phase: 'Step 7 — Permute Corners',
        text: [
            "The corner swap algorithm (place headlights on your left):",
        ],
        algorithm: "(R U R' U') (R' F R2 U') (R' U' R U) (R' F')",
        tip: [
            "If there are no headlights, do this algorithm from any angle first",
            "Then find the headlights and repeat with them on the left",
        ],
    },
    // Step 33 — CPLL practice
    {
        phase: 'Step 7 — Permute Corners',
        text: [
            "Now permute the corners! Find headlights, put them on the left, and apply the algorithm.",
        ],
        tip: [
            "Corner swap: (R U R' U') (R' F R2 U') (R' U' R U) (R' F')",
        ],
        gateCheck: isCPLLComplete,
    },
    // Step 34 — EPLL intro (edge permutation)
    {
        phase: 'Step 8 — Permute Edges',
        text: [
            "Phenomenal! Last step — permute the final layer edges.",
            "Find a side where the edge is already solved (matches the center). Place that solved edge in FRONT of you, then apply the U-perm.",
            "If no edge is solved, do the algorithm from any angle — this will create a solved edge.",
        ],
    },
    // Step 35 — U-perm
    {
        phase: 'Step 8 — Permute Edges',
        text: [
            "The edge cycle algorithm (solved edge in front):",
        ],
        algorithm: "(R' U R' U') (R' U' R' U) (R U R2)",
        tip: [
            "If no edge is solved, do this from any angle first, then find the solved edge and repeat",
        ],
    },
    // Step 36 — Final solve
    {
        phase: 'Step 8 — Permute Edges',
        text: [
            "Now finish the cube! Find a solved edge, place it in front, and apply the algorithm. You may need to repeat it.",
        ],
        tip: [
            "Edge cycle: (R' U R' U') (R' U' R' U) (R U R2)",
        ],
        gateCheck: isCubeSolved,
    },
    // Step 37 — Congratulations
    {
        phase: 'Complete!',
        text: [
            "CONGRATULATIONS! You've just solved a Rubik's Cube!",
            "You now know the complete beginner's layer-by-layer method. With practice, you'll get faster and eventually be able to solve it from memory.",
            "Feel free to switch to Cube mode to time yourself, or click \"Restart\" to go through the tutorial again!",
        ],
    },
]

const STORAGE_KEY = 'rubiks_learn_step'

function loadStep(): number {
    try {
        const v = localStorage.getItem(STORAGE_KEY)
        if (v !== null) return Math.min(Number(v), TOTAL_STEPS - 1)
    } catch { /* ignore */ }
    return 0
}

interface LearnModeProps {
    cubeState: CubeState
    setCubeState: (s: CubeState) => void
    active: boolean
}

export function LearnMode({ cubeState, setCubeState, active }: LearnModeProps) {
    const [step, setStep] = useState(loadStep)
    const [moveLog, setMoveLog] = useState('')
    const cubeRef = useRef(cubeState)
    cubeRef.current = cubeState

    // Persist step
    useEffect(() => {
        localStorage.setItem(STORAGE_KEY, String(step))
    }, [step])

    const currentStep = STEPS[Math.min(step, STEPS.length - 1)]
    const gateCheck = currentStep.gateCheck
    const gatePass = gateCheck ? gateCheck(cubeState) : true

    // Auto-scramble on entering a step that requests it
    const prevStepRef = useRef(step)
    useEffect(() => {
        if (step !== prevStepRef.current && STEPS[step]?.scrambleOnEnter) {
            fetchScramble().then(data => {
                setCubeState(data.state)
                setMoveLog('')
            })
        }
        prevStepRef.current = step
    }, [step, setCubeState])

    // Keyboard handler
    const handleKeyDown = useCallback((e: KeyboardEvent) => {
        if (!active) return
        if (!(e.key in KEY_MAP)) return
        e.preventDefault()

        const move = KEY_MAP[e.key]
        applyMove(cubeRef.current, move).then(newState => {
            setCubeState(newState)
            setMoveLog(prev => prev + (prev ? ' ' : '') + move)
        })
    }, [active, setCubeState])

    useEffect(() => {
        window.addEventListener('keydown', handleKeyDown)
        return () => window.removeEventListener('keydown', handleKeyDown)
    }, [handleKeyDown])

    function advance() {
        if (step < STEPS.length - 1) setStep(s => s + 1)
    }

    function goBack() {
        if (step > 0) setStep(s => s - 1)
    }

    function restart() {
        setStep(0)
        setMoveLog('')
    }

    function resetCube() {
        const solved: CubeState = {
            U: [['U','U','U'],['U','U','U'],['U','U','U']],
            D: [['D','D','D'],['D','D','D'],['D','D','D']],
            L: [['L','L','L'],['L','L','L'],['L','L','L']],
            R: [['R','R','R'],['R','R','R'],['R','R','R']],
            F: [['F','F','F'],['F','F','F'],['F','F','F']],
            B: [['B','B','B'],['B','B','B'],['B','B','B']],
        }
        setCubeState(solved)
        setMoveLog('')
    }

    function scramble() {
        fetchScramble().then(data => {
            setCubeState(data.state)
            setMoveLog('')
        })
    }

    const progress = Math.round((step / (STEPS.length - 1)) * 100)

    return (
        <div className={styles.container}>
            {/* Progress */}
            <div className={styles.progressBar}>
                <div className={styles.progressLabel}>
                    <span>{currentStep.phase}</span>
                    <span>Step {step + 1} / {STEPS.length}</span>
                </div>
                <div className={styles.progressTrack}>
                    <div className={styles.progressFill} style={{ width: `${progress}%` }} />
                </div>
            </div>

            {/* Cube */}
            <Cube3D state={cubeState} />

            {/* Gate check indicator */}
            {gateCheck && (
                <div className={`${styles.stepCheck} ${gatePass ? styles.checkDone : styles.checkPending}`}>
                    {gatePass ? '✓ Complete!' : '⟳ Waiting for you to complete this step on the cube...'}
                </div>
            )}

            {/* Tutorial card */}
            <div className={styles.tutorialCard}>
                {currentStep.text.map((line, i) => (
                    <p key={i} className={styles.tutorialText}>{line}</p>
                ))}

                {currentStep.algorithm && (
                    <div className={styles.algorithm}>{currentStep.algorithm}</div>
                )}

                {currentStep.tip && (
                    <div className={styles.tip}>
                        <div className={styles.tipLabel}>Tip</div>
                        {currentStep.tip.map((t, i) => (
                            <div key={i}>{t}</div>
                        ))}
                    </div>
                )}
            </div>

            {/* Move log */}
            {moveLog && (
                <div className={styles.moveLog}>Moves: {moveLog}</div>
            )}

            {/* Controls */}
            <div className={styles.controls}>
                <button className={`${styles.btn} ${styles.btnSecondary}`} onClick={goBack} disabled={step === 0}>
                    Back
                </button>

                {step < STEPS.length - 1 ? (
                    <button
                        className={`${styles.btn} ${styles.btnPrimary}`}
                        onClick={advance}
                        disabled={!!gateCheck && !gatePass}
                    >
                        {gateCheck && !gatePass ? 'Complete the step to continue' : 'Next'}
                    </button>
                ) : (
                    <button className={`${styles.btn} ${styles.btnPrimary}`} onClick={restart}>
                        Restart Tutorial
                    </button>
                )}

                <button className={`${styles.btn} ${styles.btnSecondary}`} onClick={resetCube}>
                    Reset Cube
                </button>
                <button className={`${styles.btn} ${styles.btnSecondary}`} onClick={scramble}>
                    Scramble
                </button>
                <button className={`${styles.btn} ${styles.btnSecondary}`} onClick={() => setMoveLog('')}>
                    Clear Moves
                </button>
            </div>
        </div>
    )
}
