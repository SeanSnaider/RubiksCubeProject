# Rubik's Cube Solver and Teaching Tool

A browser-based Rubik's cube simulator with a near-optimal solver, a competition-style
timer, and a 38-step guided tutorial that teaches CFOP by watching your cube state. The
solver returns a solution of 20 moves or fewer in well under a second.

## Website

<https://rubikscubeproject-frontend2.onrender.com/>

## Why I built it

I've been speedcubing for over a decade. I can solve a cube in a few seconds using CFOP,
which is a human method: pattern recognition, muscle memory, roughly 50-60 moves. A
computer doesn't need any of that, and the gap between how I solve a cube and how a
machine solves optimally is genuinely interesting.

I wanted to build the cube itself rather than drive someone else's. The move engine, the
state model, the solver integration, and the teaching tool are all mine; the two-phase
search is a library, because reimplementing a well-studied search was the least
interesting part of the problem. The first version was a Pygame capstone. This is the
rebuild: the same engine behind a real interface, built so other cubers could use it.

## How it works

### The cube engine

The core is a stateless move engine over a plain face model: six 3x3 grids, one per face,
each cell holding a color. Every move is a pure function from one state to the next, which
makes the whole thing easy to test against an exact oracle and easy to reason about.

It implements 48 moves — the 18 face turns, the M/E/S slices, the wide turns, and the
whole-cube x/y/z rotations — with the derived moves composed from the primitives rather
than hand-coded (`Rw` is `R` after `M'`, `x` is `R` after `M'` after `L'`). Primes are
three quarter turns. That composition is why the move table is a few hundred lines instead
of a few thousand, and why a bug in a slice move surfaces immediately in every wide turn
and rotation built on top of it.

The engine exists twice: [`cube_service.py`](backend/app/services/cube_service.py) drives
the API and the solver, and [`cubeMoves.ts`](frontend/src/utils/cubeMoves.ts) is a port
that runs in the browser so a keypress turns the cube in the same frame instead of waiting
on a round trip. The two are kept in sync by cross-checking the TypeScript port against
the Python engine over every move and a few hundred random sequences.

### The solver

Kociemba's two-phase algorithm, via [RubikTwoPhase](https://pypi.org/project/RubikTwoPhase/).
Rather than searching the full cube group directly, which is intractable, it splits the
problem:

- **Phase 1** reduces the cube to the subgroup G1 = ⟨U, D, L², R², F², B²⟩, meaning every
  edge and corner is correctly oriented and the four middle-slice edges sit in the middle
  slice. Getting to G1 is a much smaller search than solving outright.
- **Phase 2** solves the cube using only G1 moves, which can never break the orientation
  achieved in phase 1.

Neither phase alone is optimal, but iterating over phase-1 solutions of increasing length
and re-solving phase 2 converges on solutions under 20 moves fast. Across 150 random
sequences drawn from all 48 moves it returned a correct solution every time, never longer
than 20 moves, in at most half a second once the pruning tables are in memory.

The desktop version used the `kociemba` package, which needs a C toolchain to build.
Swapping in the pure-Python RubikTwoPhase was what made the backend deployable to Render
without a custom build image.

### The part that actually took the time

The solver kept rejecting cubes that were obviously solvable. A single `M'` from a solved
state — one slice turn, a cube anyone could fix by eye — came back as `Wrong edge and
corner parity`. That error sends you straight at piece orientation, so that's where I looked:
counting flipped edges, checking corner twist sums, convincing myself the move engine had
a bug it didn't have.

The move engine was fine. The problem is that Kociemba's facelet string has no way to
represent orientation. It identifies each face by its center sticker, which means it
requires the centers to read `URFDLB` in that exact order — the centers *are* the
coordinate system. Slice moves, wide moves and whole-cube rotations all move centers.
That's legal on a real cube and unrepresentable in the format, and the solver reports the
mismatch as a parity error pointing at the pieces rather than at the frame of reference.
None of the documentation mentions it.

The fix is to normalize orientation before serializing: rotate the cube until white is
back on top and green on the front, then prepend those rotations to the returned solution
so it still applies to the cube the user is actually holding. That's
[`normalize_orientation()`](backend/app/services/cube_service.py), which searches the 24
orientations rather than special-casing, and it's why the solver accepts a cube you've
been rotating freely while you turn it.

<!-- Two details here are reconstructed from the debug scripts in git history
     (test_face_orientation.py, analyze_invalid_state.py) rather than from your memory:
     that M' was the case you hit first, and that you spent real time down the
     edge-orientation path before finding it. Correct either if it went differently. -->

### Rendering

The cube renders as a single inline SVG: 54 stickers drawn as four-point polygons at
hardcoded isometric coordinates, filled from the current state and painted back-to-front
(`D, B, R, L, U, F`) so the near faces overlap the far ones correctly. The coordinates are
lifted directly from the `pygame.draw.polygon()` calls in the desktop version, which is
why the web cube looks pixel-for-pixel like the original.

There is no WebGL, no canvas, and no rendering dependency — the whole component is about
160 lines, most of it the coordinate table, and a turn is just a re-render with different
fills.

The tradeoff is that the projection is fixed and turns don't animate: the cube snaps to
its new state. For a keyboard-driven trainer where turns come faster than an animation
could play, that's the behavior I'd want anyway, but a real 3D representation is the
obvious next step if the view ever needs to rotate.

### Three modes

- **Cube** — Keyboard-driven cube manipulation using csTimer-compatible bindings. The
  timer starts on your first non-rotation move and stops the instant the state is solved,
  which then records the solve and deals a new scramble.
- **Timer** — A plain spacebar timer for solves on a physical cube. Hold to arm, with a
  hold-progress indicator, release to start.
- **Learn** — A 38-step CFOP tutorial covering notation, the cross, the first two layers,
  and OLL/PLL. Steps that teach an algorithm are gated: the tutorial reads your actual
  cube state through validators like `isCrossComplete` and `isOLLComplete` and won't
  advance until you've genuinely done it. Some steps scramble the cube on entry so you
  have to recognize the case rather than replay a memorized sequence.

### Timer and stats

Rolling ao5, ao12, ao50 and ao100 computed WCA-style (drop the best and worst, mean the
rest), plus session mean, standard deviation, personal best, and best ao5/ao12. Solves
carry editable +2 and DNF penalties that feed back into every average. History is kept in
localStorage, so the app works with the backend down and there's nothing to sign into.

A handful of people in my cubing circle use it as their daily timer, which has been the
best bug-reporting channel I could have asked for.

## Stack

| Layer | Tech |
|---|---|
| Cube engine | Python (backend), TypeScript port (browser) |
| Solver | RubikTwoPhase (Kociemba two-phase, pure Python) |
| API | FastAPI, Uvicorn |
| Frontend | React 19, TypeScript, Vite |
| Rendering | Inline SVG |
| Storage | localStorage; MongoDB (Motor) on the API |
| Deployment | Render (`render.yaml`) |

## Running it

Requires Python 3.10+ and Node 20+. MongoDB is optional — the API starts without it and
the frontend keeps its history locally regardless.

```bash
git clone https://github.com/SeanSnaider/RubiksCubeProject
cd RubiksCubeProject

# Backend — http://localhost:8000 (docs at /docs)
cd backend
python -m venv venv
source venv/Scripts/activate        # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                # defaults are fine for local dev
uvicorn app.main:app --reload

# Frontend — http://localhost:5173
cd ../frontend
npm install
cp .env.example .env
npm run dev
```

The first solve request loads the two-phase pruning tables from `backend/twophase/` and
takes a few seconds; every request after that is sub-second.

## What I'd do differently

- **The solve endpoint isn't wired into the UI.** `POST /api/cube/solve` works and returns
  a correct solution in standard notation, but nothing in the frontend calls it, so the
  headline feature is reachable only through the API. The cube renders as a static SVG,
  so showing a solution means either stepping through it move by move or building real
  animation first — which is the honest reason it isn't done yet.
- **MongoDB is connected but unused.** The solve-history endpoints and the Motor
  integration are all there, and `utils/api.ts` has typed clients for them, but no
  component calls them — localStorage does the real work. Either finish the sync or drop
  the dependency; carrying a database the app never reads is the worst of both.
- **The move engine still has no tests.** The solver boundary is covered, and the solves
  controller has a couple of tests that need a live MongoDB to pass, but the engine itself
  doesn't — despite being the easiest thing in the project to test. It's pure functions
  with an exact oracle, and there are now two implementations that have to agree. `pytest`
  also isn't in `requirements.txt`, so running any of it means installing it by hand.
