# Rubik's Cube Solver and Teaching Tool

A full-stack 3D Rubik's Cube simulator with a near-optimal solving algorithm, competition-style timer, and step-by-step tutorial mode. Built by someone who's been speedcubing for 10+ years (sub-7 seconds).

Originally a Pygame desktop app built as a high school capstone in collaboration with [TheCubicle.com](https://www.thecubicle.com/), now fully refactored into a modern web application with MVC architecture, CSS 3D rendering, and solve tracking inspired by [csTimer](https://cstimer.net/).

![React](https://img.shields.io/badge/React-18-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![MongoDB](https://img.shields.io/badge/MongoDB-7-green)
![Python](https://img.shields.io/badge/Python-3.10+-yellow)

<!-- ![App Screenshot](docs/screenshot.png) -->

## Features

**Solver**
- Implements Kociemba's two-phase algorithm
- Computes near-optimal solutions (≤20 moves) in under 1 second
- Real-time 3D rendering with CSS 3D transforms

**Teaching Mode**
- Step-by-step tutorial for learning to solve the cube
- State validation at each stage — cross, corners, second layer, top face
- Blocks progression until each stage is completed correctly
- Designed to teach the CFOP method fundamentals

**Competition Timer**
- Spacebar-driven timer with 15-second WCA-style inspection countdown
- Automatic +2 and DNF penalty detection
- Every solve persisted to MongoDB with scramble, time, and penalty data

**Live Statistics**
- Current and best ao5, ao12, ao100
- Mean, standard deviation, personal bests
- Scrollable solve history with inline penalty editing and deletion

**Controls**
- Keyboard-based cube manipulation following standard cubing keybindings (csTimer layout)
- Full move support — all face moves, primes, doubles, slice moves (M, E, S), and wide moves

## Tech Stack

| Layer | Technology | Role |
|---|---|---|
| Frontend | React 18, TypeScript, Vite | UI, cube rendering, timer |
| Backend | FastAPI (Python) | REST API, cube logic, solver |
| Database | MongoDB + Motor (async) | Solve records, statistics |
| Cube Rendering | CSS 3D Transforms | Lightweight 3D display |
| Solver | Kociemba (Python) | Two-phase optimal solving |

## Project Structure

```
RubiksCubeProject/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI entry point + CORS
│   │   ├── database.py             # Async MongoDB connection
│   │   ├── models/                 # Pydantic models
│   │   │   ├── cube.py             # CubeState, MoveRequest, SolveRequest
│   │   │   └── solve.py            # SolveRecord, CreateSolveRequest
│   │   ├── services/               # Business logic
│   │   │   ├── cube_service.py     # Moves, scrambling, solving, validation
│   │   │   └── stats_service.py    # ao5/ao12/ao100, mean, std dev
│   │   └── controllers/            # Route handlers
│   │       ├── cube_controller.py  # /api/cube/* endpoints
│   │       └── solve_controller.py # /api/solves/* endpoints
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/             # React components
│   │   │   ├── Cube3D.tsx          # 3D cube visualization
│   │   │   ├── Timer.tsx           # Competition timer
│   │   │   ├── Statistics.tsx      # Stats panel
│   │   │   ├── SolveHistory.tsx    # Past solves list
│   │   │   └── ...
│   │   ├── hooks/                  # Custom React hooks
│   │   │   ├── useTimer.ts         # Timer state machine
│   │   │   ├── useCube.ts          # Cube state management
│   │   │   └── useKeyboard.ts      # Keybinding handler
│   │   ├── services/
│   │   │   └── api.ts              # Backend API client
│   │   └── types/
│   │       └── index.ts            # TypeScript type definitions
│   ├── package.json
│   └── vite.config.ts
│
└── README.md
```

## Getting Started

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** and npm
- **MongoDB** — locally installed or via Docker

### 1. Start MongoDB

Using Docker:

```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

Or make sure your local `mongod` service is running.

### 2. Start the Backend

```bash
cd backend
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000` with interactive docs at `http://localhost:8000/docs`.

### 3. Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

The app will open at `http://localhost:5173`.

## API Endpoints

### Cube

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/cube/reset` | Returns a solved cube state |
| `POST` | `/api/cube/move` | Applies move(s) to a given cube state |
| `GET` | `/api/cube/scramble` | Generates a random 21-move scramble and resulting state |
| `POST` | `/api/cube/solve` | Returns a near-optimal solution via Kociemba |
| `POST` | `/api/cube/validate` | Checks whether a cube state is solvable |

### Solves

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/solves` | List solve records (supports `limit` and `offset`) |
| `POST` | `/api/solves` | Save a new solve |
| `DELETE` | `/api/solves/:id` | Delete a solve |
| `PATCH` | `/api/solves/:id` | Update penalty (+2, DNF, or clear) |
| `GET` | `/api/solves/stats` | Get calculated statistics (ao5, ao12, ao100, mean, etc.) |

## Controls

Keybinds follow a speedcuber-friendly layout (same as csTimer).

### Face Moves

| Key | Move | | Key | Move |
|-----|------|-|-----|------|
| I | R | | K | R' |
| D | L | | E | L' |
| J | U | | F | U' |
| S | D | | L | D' |
| H | F | | G | F' |
| W | B | | O | B' |

### Slice Moves

| Key | Move | | Key | Move |
|-----|------|-|-----|------|
| 5, 6 | M | | X, . | M' |
| 2 | E | | 9 | E' |
| 0 | S | | 1 | S' |

### Wide Moves

| Key | Move | | Key | Move |
|-----|------|-|-----|------|
| U | Rw | | M | Rw' |
| V | Lw | | R | Lw' |
| , | Uw | | C | Uw' |
| Z | Dw | | / | Dw' |

### Cube Rotations

| Key | Move | | Key | Move |
|-----|------|-|-----|------|
| T, Y | x | | B, N | x' |
| ; | y | | A | y' |
| P | z | | Q | z' |

### Timer

| Key | Action |
|-----|--------|
| Space (hold) | Start inspection → release to start timer |
| Any key | Stop timer during solve |

## How the Solver Works

The Kociemba algorithm solves the cube in two phases:

1. **Phase 1** — Reduce the cube to the G1 subgroup, where only half-turn moves on certain faces are needed
2. **Phase 2** — Solve from the reduced state to completion

This approach finds solutions averaging 18–19 moves, with a maximum of 20.

## Why I Built This

I've been cubing since I was a kid and wanted to create a tool that actually teaches the solving process rather than just showing a solution. Most online solvers dump a move sequence on you — this one makes you learn each stage.

The original Pygame version was my high school senior capstone, built in collaboration with TheCubicle.com. Rebuilding it as a full-stack web app let me apply everything I've learned about software architecture — separating concerns with MVC, building a proper REST API, adding persistent data with MongoDB, and rendering the cube in the browser with CSS 3D transforms instead of a game engine.

## Author

Sean Snaider — [seansnaider.vercel.app](https://seansnaider.vercel.app) · [LinkedIn](https://linkedin.com/in/seansnaider)
