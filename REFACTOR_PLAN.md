# Rubik's Cube Web App - MVC Refactor Plan

## Summary
Transform the monolithic Pygame-based Rubik's Cube simulator into a modern web application with:
- **MVC Architecture** (separation of concerns)
- **React + TypeScript frontend** (replacing Pygame)
- **FastAPI backend** (Python REST API)
- **MongoDB database** (solve time tracking like cstimer)

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | React 18 + TypeScript + Vite | UI, cube visualization, timer |
| Backend | FastAPI (Python) | REST API, cube logic, solver |
| Database | MongoDB + Motor (async) | Solve records, statistics |
| Cube Rendering | CSS 3D Transforms | Lightweight 3D cube display |
| Solver | Kociemba (Python) | Optimal cube solving |

---

## Proposed Project Structure (Monorepo)

```
RubiksCubeProject/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── database.py                # MongoDB async connection
│   │   │
│   │   ├── models/                    # Pydantic models (M in MVC)
│   │   │   ├── __init__.py
│   │   │   ├── cube.py                # CubeState model
│   │   │   └── solve.py               # Solve record model
│   │   │
│   │   ├── services/                  # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── cube_service.py        # Cube moves, validation, scrambling
│   │   │   └── stats_service.py       # ao5, ao12, mean, std dev calculations
│   │   │
│   │   └── controllers/               # Route handlers (C in MVC)
│   │       ├── __init__.py
│   │       ├── cube_controller.py     # /api/cube/* endpoints
│   │       └── solve_controller.py    # /api/solves/* endpoints
│   │
│   ├── tests/
│   │   ├── test_cube_service.py
│   │   └── test_stats_service.py
│   │
│   ├── requirements.txt
│   └── pyproject.toml
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   │
│   ├── src/
│   │   ├── components/                # React components (V in MVC)
│   │   │   ├── Cube3D.tsx             # CSS 3D cube visualization
│   │   │   ├── CubeFace.tsx           # Single face (3x3 grid)
│   │   │   ├── Timer.tsx              # Competition timer with inspection
│   │   │   ├── Scramble.tsx           # Scramble display
│   │   │   ├── Statistics.tsx         # Stats panel (ao5, ao12, etc.)
│   │   │   ├── SolveHistory.tsx       # List of past solves
│   │   │   └── PenaltyButtons.tsx     # +2, DNF, OK buttons
│   │   │
│   │   ├── hooks/                     # Custom React hooks
│   │   │   ├── useTimer.ts            # Timer state and logic
│   │   │   ├── useCube.ts             # Cube state management
│   │   │   ├── useKeyboard.ts         # Keyboard event handling
│   │   │   └── useSolves.ts           # Solve history + stats fetching
│   │   │
│   │   ├── services/                  # API communication
│   │   │   └── api.ts                 # Fetch wrapper for backend calls
│   │   │
│   │   ├── types/                     # TypeScript type definitions
│   │   │   └── index.ts               # CubeState, Solve, Stats types
│   │   │
│   │   ├── App.tsx                    # Main app component
│   │   ├── App.css                    # Global styles
│   │   └── main.tsx                   # React entry point
│   │
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── REFACTOR_PLAN.md                   # This file
└── README.md
```

---

## Phase 1: Backend Core Setup

### 1.1 Create FastAPI Application
**File: `backend/app/main.py`**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Rubik's Cube API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from app.controllers import cube_controller, solve_controller
app.include_router(cube_controller.router, prefix="/api/cube", tags=["cube"])
app.include_router(solve_controller.router, prefix="/api/solves", tags=["solves"])
```

### 1.2 Cube State Model
**File: `backend/app/models/cube.py`**

```python
from pydantic import BaseModel, field_validator
from typing import List

class CubeState(BaseModel):
    """Represents a 3x3 Rubik's Cube state"""
    U: List[List[str]]  # Up face (3x3)
    D: List[List[str]]  # Down face
    L: List[List[str]]  # Left face
    R: List[List[str]]  # Right face
    F: List[List[str]]  # Front face
    B: List[List[str]]  # Back face

    @field_validator('U', 'D', 'L', 'R', 'F', 'B')
    @classmethod
    def validate_face(cls, v):
        if len(v) != 3 or any(len(row) != 3 for row in v):
            raise ValueError("Each face must be a 3x3 grid")
        valid_colors = {'U', 'D', 'L', 'R', 'F', 'B'}
        for row in v:
            for cell in row:
                if cell not in valid_colors:
                    raise ValueError(f"Invalid color: {cell}")
        return v

class MoveRequest(BaseModel):
    state: CubeState
    moves: str  # e.g., "R U R' U'"

class SolveRequest(BaseModel):
    state: CubeState
```

### 1.3 Cube Service (Business Logic)
**File: `backend/app/services/cube_service.py`**

This file should contain all cube manipulation logic extracted from `RubiksCube.py`:

```python
import copy
import random
import kociemba

MOVES = ['U', 'U\'', 'U2', 'R', 'R\'', 'R2', 'F', 'F\'', 'F2',
         'D', 'D\'', 'D2', 'L', 'L\'', 'L2', 'B', 'B\'', 'B2']

def get_solved_state() -> dict:
    """Return a solved cube state"""
    return {
        'U': [['U']*3 for _ in range(3)],
        'D': [['D']*3 for _ in range(3)],
        'L': [['L']*3 for _ in range(3)],
        'R': [['R']*3 for _ in range(3)],
        'F': [['F']*3 for _ in range(3)],
        'B': [['B']*3 for _ in range(3)],
    }

def rotate_face_cw(face: list) -> list:
    """Rotate a face 90 degrees clockwise"""
    return [
        [face[2][0], face[1][0], face[0][0]],
        [face[2][1], face[1][1], face[0][1]],
        [face[2][2], face[1][2], face[0][2]],
    ]

def rotate_face_ccw(face: list) -> list:
    """Rotate a face 90 degrees counter-clockwise"""
    return [
        [face[0][2], face[1][2], face[2][2]],
        [face[0][1], face[1][1], face[2][1]],
        [face[0][0], face[1][0], face[2][0]],
    ]

def apply_move(state: dict, move: str) -> dict:
    """Apply a single move to the cube state"""
    state = copy.deepcopy(state)

    if move == 'U':
        state['U'] = rotate_face_cw(state['U'])
        temp = state['F'][0][:]
        state['F'][0] = state['R'][0][:]
        state['R'][0] = state['B'][0][:]
        state['B'][0] = state['L'][0][:]
        state['L'][0] = temp
    elif move == "U'":
        state['U'] = rotate_face_ccw(state['U'])
        temp = state['F'][0][:]
        state['F'][0] = state['L'][0][:]
        state['L'][0] = state['B'][0][:]
        state['B'][0] = state['R'][0][:]
        state['R'][0] = temp
    # ... implement all other moves (R, R', F, F', D, D', L, L', B, B')
    # ... implement slice moves (M, M', E, E', S, S')

    return state

def apply_moves(state: dict, moves: str) -> dict:
    """Apply a sequence of moves to the cube state"""
    move_list = parse_moves(moves)
    for move in move_list:
        state = apply_move(state, move)
    return state

def parse_moves(moves: str) -> list:
    """Parse a move string like 'R U R' U'' into individual moves"""
    result = []
    i = 0
    while i < len(moves):
        if moves[i].isspace():
            i += 1
            continue
        move = moves[i]
        i += 1
        if i < len(moves) and moves[i] == "'":
            move += "'"
            i += 1
        elif i < len(moves) and moves[i] == "2":
            result.append(move)  # Add move twice for double moves
            i += 1
        result.append(move)
    return result

def generate_scramble(length: int = 21) -> str:
    """Generate a random scramble sequence"""
    scramble = []
    last_move = None
    for _ in range(length):
        move = random.choice(MOVES)
        # Avoid consecutive moves on same face
        while last_move and move[0] == last_move[0]:
            move = random.choice(MOVES)
        scramble.append(move)
        last_move = move
    return ' '.join(scramble)

def state_to_kociemba_string(state: dict) -> str:
    """Convert cube state to Kociemba solver format (URFDLB order)"""
    # Kociemba expects: U1-U9, R1-R9, F1-F9, D1-D9, L1-L9, B1-B9
    face_order = ['U', 'R', 'F', 'D', 'L', 'B']
    result = ''
    for face_name in face_order:
        face = state[face_name]
        for row in face:
            for cell in row:
                result += cell
    return result

def get_solution(state: dict) -> str:
    """Get optimal solution using Kociemba algorithm"""
    cube_string = state_to_kociemba_string(state)
    try:
        solution = kociemba.solve(cube_string)
        return solution
    except ValueError as e:
        raise ValueError(f"Invalid cube state: {e}")

def validate_state(state: dict) -> bool:
    """Validate that cube state is solvable"""
    # Count colors - each should appear exactly 9 times
    counts = {'U': 0, 'D': 0, 'L': 0, 'R': 0, 'F': 0, 'B': 0}
    for face in state.values():
        for row in face:
            for cell in row:
                counts[cell] += 1

    for count in counts.values():
        if count != 9:
            return False

    # Try to solve - if it works, state is valid
    try:
        get_solution(state)
        return True
    except:
        return False
```

### 1.4 Cube Controller (REST Endpoints)
**File: `backend/app/controllers/cube_controller.py`**

```python
from fastapi import APIRouter, HTTPException
from app.models.cube import CubeState, MoveRequest, SolveRequest
from app.services import cube_service

router = APIRouter()

@router.get("/reset")
def reset_cube():
    """Get a solved cube state"""
    return cube_service.get_solved_state()

@router.post("/move")
def apply_moves(request: MoveRequest):
    """Apply moves to cube and return new state"""
    try:
        new_state = cube_service.apply_moves(
            request.state.model_dump(),
            request.moves
        )
        return new_state
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/scramble")
def generate_scramble():
    """Generate a random scramble"""
    scramble = cube_service.generate_scramble()
    state = cube_service.apply_moves(
        cube_service.get_solved_state(),
        scramble
    )
    return {"scramble": scramble, "state": state}

@router.post("/solve")
def solve_cube(request: SolveRequest):
    """Get solution for current cube state"""
    try:
        solution = cube_service.get_solution(request.state.model_dump())
        return {"solution": solution}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/validate")
def validate_cube(request: SolveRequest):
    """Validate if cube state is solvable"""
    is_valid = cube_service.validate_state(request.state.model_dump())
    return {"valid": is_valid}
```

---

## Phase 2: Database Integration

### 2.1 MongoDB Connection
**File: `backend/app/database.py`**

```python
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

class Database:
    client: Optional[AsyncIOMotorClient] = None

db = Database()

async def get_database():
    return db.client.rubikscube

async def connect_to_mongo():
    db.client = AsyncIOMotorClient("mongodb://localhost:27017")

async def close_mongo_connection():
    db.client.close()
```

### 2.2 Solve Record Model
**File: `backend/app/models/solve.py`**

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class SolveRecord(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    time_ms: int                    # Solve time in milliseconds
    scramble: str                   # Scramble sequence used
    penalty: Optional[str] = None   # "+2", "DNF", or None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class CreateSolveRequest(BaseModel):
    time_ms: int
    scramble: str
    penalty: Optional[str] = None

class UpdatePenaltyRequest(BaseModel):
    penalty: Optional[str] = None  # "+2", "DNF", or None
```

### 2.3 Statistics Service
**File: `backend/app/services/stats_service.py`**

```python
from typing import List, Optional
import statistics

def calculate_ao(times: List[int], n: int) -> Optional[float]:
    """Calculate average of n, removing best and worst"""
    if len(times) < n:
        return None

    recent = times[-n:]
    sorted_times = sorted(recent)
    # Remove best and worst
    trimmed = sorted_times[1:-1]
    return statistics.mean(trimmed) if trimmed else None

def calculate_stats(solves: List[dict]) -> dict:
    """Calculate all statistics from solve list"""
    if not solves:
        return {
            "count": 0,
            "best": None,
            "worst": None,
            "current_ao5": None,
            "current_ao12": None,
            "current_ao100": None,
            "best_ao5": None,
            "best_ao12": None,
            "best_ao100": None,
            "mean": None,
            "std_dev": None,
        }

    # Filter out DNF solves for most calculations
    valid_solves = [s for s in solves if s.get('penalty') != 'DNF']

    # Apply +2 penalties
    times = []
    for s in valid_solves:
        t = s['time_ms']
        if s.get('penalty') == '+2':
            t += 2000
        times.append(t)

    if not times:
        return {"count": len(solves), "best": None, "worst": None}

    # Calculate all-time best averages
    best_ao5 = None
    best_ao12 = None
    best_ao100 = None

    for i in range(len(times)):
        if i >= 4:
            ao5 = calculate_ao(times[:i+1], 5)
            if ao5 and (best_ao5 is None or ao5 < best_ao5):
                best_ao5 = ao5
        if i >= 11:
            ao12 = calculate_ao(times[:i+1], 12)
            if ao12 and (best_ao12 is None or ao12 < best_ao12):
                best_ao12 = ao12
        if i >= 99:
            ao100 = calculate_ao(times[:i+1], 100)
            if ao100 and (best_ao100 is None or ao100 < best_ao100):
                best_ao100 = ao100

    return {
        "count": len(solves),
        "best": min(times),
        "worst": max(times),
        "current_ao5": calculate_ao(times, 5),
        "current_ao12": calculate_ao(times, 12),
        "current_ao100": calculate_ao(times, 100),
        "best_ao5": best_ao5,
        "best_ao12": best_ao12,
        "best_ao100": best_ao100,
        "mean": statistics.mean(times),
        "std_dev": statistics.stdev(times) if len(times) > 1 else None,
    }
```

### 2.4 Solve Controller
**File: `backend/app/controllers/solve_controller.py`**

```python
from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from app.database import get_database
from app.models.solve import SolveRecord, CreateSolveRequest, UpdatePenaltyRequest
from app.services.stats_service import calculate_stats

router = APIRouter()

@router.get("/")
async def list_solves(limit: int = 100, offset: int = 0):
    """Get list of solve records"""
    db = await get_database()
    cursor = db.solves.find().sort("created_at", -1).skip(offset).limit(limit)
    solves = await cursor.to_list(length=limit)
    # Convert ObjectId to string
    for solve in solves:
        solve["_id"] = str(solve["_id"])
    return solves

@router.post("/")
async def create_solve(solve: CreateSolveRequest):
    """Create a new solve record"""
    if solve.time_ms < 500:  # Reject impossibly fast times
        raise HTTPException(status_code=400, detail="Time too fast to be valid")
    if solve.penalty and solve.penalty not in ["+2", "DNF"]:
        raise HTTPException(status_code=400, detail="Invalid penalty type")

    db = await get_database()
    record = SolveRecord(**solve.model_dump())
    result = await db.solves.insert_one(record.model_dump(by_alias=True, exclude={'id'}))
    return {"id": str(result.inserted_id)}

@router.delete("/{solve_id}")
async def delete_solve(solve_id: str):
    """Delete a solve record"""
    db = await get_database()
    result = await db.solves.delete_one({"_id": ObjectId(solve_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Solve not found")
    return {"deleted": True}

@router.patch("/{solve_id}")
async def update_penalty(solve_id: str, request: UpdatePenaltyRequest):
    """Update penalty for a solve"""
    if request.penalty and request.penalty not in ["+2", "DNF"]:
        raise HTTPException(status_code=400, detail="Invalid penalty type")

    db = await get_database()
    result = await db.solves.update_one(
        {"_id": ObjectId(solve_id)},
        {"$set": {"penalty": request.penalty}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Solve not found")
    return {"updated": True}

@router.get("/stats")
async def get_stats():
    """Get calculated statistics"""
    db = await get_database()
    cursor = db.solves.find().sort("created_at", 1)  # Oldest first
    solves = await cursor.to_list(length=10000)
    return calculate_stats(solves)
```

---

## Phase 3: React Frontend

### 3.1 Package Dependencies
**File: `frontend/package.json`**

```json
{
  "name": "rubikscube-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0"
  }
}
```

### 3.2 TypeScript Types
**File: `frontend/src/types/index.ts`**

```typescript
export type Color = 'U' | 'D' | 'L' | 'R' | 'F' | 'B';
export type Face = Color[][];

export interface CubeState {
  U: Face;
  D: Face;
  L: Face;
  R: Face;
  F: Face;
  B: Face;
}

export interface Solve {
  _id: string;
  time_ms: number;
  scramble: string;
  penalty: '+2' | 'DNF' | null;
  created_at: string;
}

export interface Stats {
  count: number;
  best: number | null;
  worst: number | null;
  current_ao5: number | null;
  current_ao12: number | null;
  current_ao100: number | null;
  best_ao5: number | null;
  best_ao12: number | null;
  best_ao100: number | null;
  mean: number | null;
  std_dev: number | null;
}

export type TimerPhase = 'idle' | 'inspection' | 'ready' | 'running' | 'stopped';
```

### 3.3 API Service
**File: `frontend/src/services/api.ts`**

```typescript
import { CubeState, Solve, Stats } from '../types';

const API_BASE = 'http://localhost:8000/api';

export const api = {
  // Cube endpoints
  async resetCube(): Promise<CubeState> {
    const res = await fetch(`${API_BASE}/cube/reset`);
    return res.json();
  },

  async applyMoves(state: CubeState, moves: string): Promise<CubeState> {
    const res = await fetch(`${API_BASE}/cube/move`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ state, moves }),
    });
    return res.json();
  },

  async getScramble(): Promise<{ scramble: string; state: CubeState }> {
    const res = await fetch(`${API_BASE}/cube/scramble`);
    return res.json();
  },

  async solve(state: CubeState): Promise<{ solution: string }> {
    const res = await fetch(`${API_BASE}/cube/solve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ state }),
    });
    if (!res.ok) throw new Error('Invalid cube state');
    return res.json();
  },

  // Solve endpoints
  async listSolves(limit = 100): Promise<Solve[]> {
    const res = await fetch(`${API_BASE}/solves?limit=${limit}`);
    return res.json();
  },

  async createSolve(time_ms: number, scramble: string, penalty?: string): Promise<{ id: string }> {
    const res = await fetch(`${API_BASE}/solves`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ time_ms, scramble, penalty }),
    });
    return res.json();
  },

  async deleteSolve(id: string): Promise<void> {
    await fetch(`${API_BASE}/solves/${id}`, { method: 'DELETE' });
  },

  async updatePenalty(id: string, penalty: string | null): Promise<void> {
    await fetch(`${API_BASE}/solves/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ penalty }),
    });
  },

  async getStats(): Promise<Stats> {
    const res = await fetch(`${API_BASE}/solves/stats`);
    return res.json();
  },
};
```

---

## Phase 4: CSS 3D Cube Component

### 4.1 Cube Visualization
**File: `frontend/src/components/Cube3D.tsx`**

```tsx
import React from 'react';
import { CubeState, Color } from '../types';
import './Cube3D.css';

const COLOR_MAP: Record<Color, string> = {
  U: '#FFFFFF', // White
  D: '#FFFF00', // Yellow
  L: '#FFA500', // Orange
  R: '#FF0000', // Red
  F: '#00FF00', // Green
  B: '#0000FF', // Blue
};

interface Cube3DProps {
  state: CubeState;
}

const CubeFace: React.FC<{ face: Color[][]; className: string }> = ({ face, className }) => (
  <div className={`face ${className}`}>
    {face.flat().map((color, i) => (
      <div
        key={i}
        className="sticker"
        style={{ backgroundColor: COLOR_MAP[color] }}
      />
    ))}
  </div>
);

export const Cube3D: React.FC<Cube3DProps> = ({ state }) => {
  return (
    <div className="cube-container">
      <div className="cube">
        <CubeFace face={state.U} className="face-U" />
        <CubeFace face={state.D} className="face-D" />
        <CubeFace face={state.L} className="face-L" />
        <CubeFace face={state.R} className="face-R" />
        <CubeFace face={state.F} className="face-F" />
        <CubeFace face={state.B} className="face-B" />
      </div>
    </div>
  );
};
```

### 4.2 Cube CSS
**File: `frontend/src/components/Cube3D.css`**

```css
.cube-container {
  perspective: 800px;
  width: 200px;
  height: 200px;
  margin: 50px auto;
}

.cube {
  width: 150px;
  height: 150px;
  position: relative;
  transform-style: preserve-3d;
  transform: rotateX(-30deg) rotateY(-45deg);
}

.face {
  position: absolute;
  width: 150px;
  height: 150px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(3, 1fr);
  gap: 2px;
  padding: 2px;
  background: #333;
}

.sticker {
  border-radius: 4px;
  border: 1px solid #222;
}

.face-U {
  transform: rotateX(90deg) translateZ(75px);
}

.face-D {
  transform: rotateX(-90deg) translateZ(75px);
}

.face-F {
  transform: translateZ(75px);
}

.face-B {
  transform: rotateY(180deg) translateZ(75px);
}

.face-L {
  transform: rotateY(-90deg) translateZ(75px);
}

.face-R {
  transform: rotateY(90deg) translateZ(75px);
}
```

---

## Phase 5: Timer Component

### 5.1 Timer Hook
**File: `frontend/src/hooks/useTimer.ts`**

```typescript
import { useState, useRef, useCallback } from 'react';
import { TimerPhase } from '../types';

const INSPECTION_TIME = 15000; // 15 seconds

export function useTimer() {
  const [phase, setPhase] = useState<TimerPhase>('idle');
  const [displayTime, setDisplayTime] = useState(0);
  const [inspectionTime, setInspectionTime] = useState(INSPECTION_TIME);
  const [penalty, setPenalty] = useState<'+2' | 'DNF' | null>(null);

  const startTimeRef = useRef(0);
  const inspectionStartRef = useRef(0);
  const animationFrameRef = useRef<number>();
  const inspectionIntervalRef = useRef<number>();

  const startInspection = useCallback(() => {
    setPhase('inspection');
    setInspectionTime(INSPECTION_TIME);
    setPenalty(null);
    inspectionStartRef.current = performance.now();

    inspectionIntervalRef.current = window.setInterval(() => {
      const elapsed = performance.now() - inspectionStartRef.current;
      const remaining = INSPECTION_TIME - elapsed;

      if (remaining <= 0) {
        if (remaining <= -2000) {
          // DNF after 17 seconds
          setPenalty('DNF');
          setPhase('idle');
          clearInterval(inspectionIntervalRef.current);
        } else {
          // +2 after 15 seconds
          setPenalty('+2');
        }
        setInspectionTime(0);
      } else {
        setInspectionTime(remaining);
      }
    }, 100);
  }, []);

  const startSolve = useCallback(() => {
    if (inspectionIntervalRef.current) {
      clearInterval(inspectionIntervalRef.current);
    }

    setPhase('running');
    startTimeRef.current = performance.now();

    const updateTimer = () => {
      setDisplayTime(performance.now() - startTimeRef.current);
      animationFrameRef.current = requestAnimationFrame(updateTimer);
    };
    animationFrameRef.current = requestAnimationFrame(updateTimer);
  }, []);

  const stopSolve = useCallback(() => {
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
    }
    setPhase('stopped');
    const finalTime = performance.now() - startTimeRef.current;
    setDisplayTime(finalTime);
    return { time: finalTime, penalty };
  }, [penalty]);

  const reset = useCallback(() => {
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
    }
    if (inspectionIntervalRef.current) {
      clearInterval(inspectionIntervalRef.current);
    }
    setPhase('idle');
    setDisplayTime(0);
    setInspectionTime(INSPECTION_TIME);
    setPenalty(null);
  }, []);

  return {
    phase,
    displayTime,
    inspectionTime,
    penalty,
    setPenalty,
    startInspection,
    startSolve,
    stopSolve,
    reset,
  };
}
```

### 5.2 Timer Component
**File: `frontend/src/components/Timer.tsx`**

```tsx
import React from 'react';
import { TimerPhase } from '../types';
import './Timer.css';

interface TimerProps {
  phase: TimerPhase;
  displayTime: number;
  inspectionTime: number;
  penalty: '+2' | 'DNF' | null;
}

function formatTime(ms: number): string {
  if (ms < 0) return '0.00';
  const totalSeconds = ms / 1000;
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;

  if (minutes > 0) {
    return `${minutes}:${seconds.toFixed(2).padStart(5, '0')}`;
  }
  return seconds.toFixed(2);
}

export const Timer: React.FC<TimerProps> = ({
  phase,
  displayTime,
  inspectionTime,
  penalty,
}) => {
  const getDisplay = () => {
    if (phase === 'inspection') {
      const seconds = Math.ceil(inspectionTime / 1000);
      if (seconds <= 0) return penalty === 'DNF' ? 'DNF' : '+2';
      return seconds.toString();
    }
    return formatTime(displayTime);
  };

  return (
    <div className={`timer timer-${phase}`}>
      <div className="timer-display">
        {getDisplay()}
        {phase === 'stopped' && penalty && (
          <span className="penalty">{penalty}</span>
        )}
      </div>
      <div className="timer-hint">
        {phase === 'idle' && 'Press SPACE to start inspection'}
        {phase === 'inspection' && 'Hold SPACE, release to start'}
        {phase === 'running' && 'Press any key to stop'}
      </div>
    </div>
  );
};
```

---

## Phase 6: Keyboard Controls

### 6.1 Keyboard Hook
**File: `frontend/src/hooks/useKeyboard.ts`**

```typescript
import { useEffect, useCallback } from 'react';
import { CubeState } from '../types';
import { api } from '../services/api';

// Standard cubing keybindings
const MOVE_KEYS: Record<string, string> = {
  'i': 'R',   'k': "R'",
  'j': 'U',   'f': "U'",
  'd': 'L',   'e': "L'",
  'h': 'F',   'g': "F'",
  's': 'D',   'l': "D'",
  'w': 'B',   'o': "B'",
  'u': 'r',   'm': "r'",  // Wide moves
  ';': 'y',   'a': "y'",  // Y rotation
  'v': 'x',   'n': "x'",  // X rotation
  'p': 'z',   'q': "z'",  // Z rotation
};

interface UseKeyboardProps {
  cubeState: CubeState;
  setCubeState: (state: CubeState) => void;
  timerPhase: string;
  onSpaceDown: () => void;
  onSpaceUp: () => void;
  onAnyKey: () => void;
}

export function useKeyboard({
  cubeState,
  setCubeState,
  timerPhase,
  onSpaceDown,
  onSpaceUp,
  onAnyKey,
}: UseKeyboardProps) {

  const handleKeyDown = useCallback(async (e: KeyboardEvent) => {
    // Timer controls take priority
    if (e.code === 'Space') {
      e.preventDefault();
      onSpaceDown();
      return;
    }

    if (timerPhase === 'running') {
      onAnyKey();
      return;
    }

    // Cube moves only when timer is idle or stopped
    if (timerPhase !== 'idle' && timerPhase !== 'stopped') return;

    const move = MOVE_KEYS[e.key.toLowerCase()];
    if (move) {
      e.preventDefault();
      try {
        const newState = await api.applyMoves(cubeState, move);
        setCubeState(newState);
      } catch (err) {
        console.error('Failed to apply move:', err);
      }
    }
  }, [cubeState, setCubeState, timerPhase, onSpaceDown, onAnyKey]);

  const handleKeyUp = useCallback((e: KeyboardEvent) => {
    if (e.code === 'Space') {
      e.preventDefault();
      onSpaceUp();
    }
  }, [onSpaceUp]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [handleKeyDown, handleKeyUp]);
}
```

---

## Phase 7: Statistics & History

### 7.1 Statistics Component
**File: `frontend/src/components/Statistics.tsx`**

```tsx
import React from 'react';
import { Stats } from '../types';
import './Statistics.css';

interface StatisticsProps {
  stats: Stats;
}

function formatTime(ms: number | null): string {
  if (ms === null) return '-';
  const seconds = ms / 1000;
  if (seconds >= 60) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toFixed(2).padStart(5, '0')}`;
  }
  return seconds.toFixed(2);
}

export const Statistics: React.FC<StatisticsProps> = ({ stats }) => {
  return (
    <div className="statistics">
      <div className="stat-row">
        <span className="stat-label">Solves:</span>
        <span className="stat-value">{stats.count}</span>
      </div>
      <div className="stat-row">
        <span className="stat-label">Best:</span>
        <span className="stat-value best">{formatTime(stats.best)}</span>
      </div>
      <div className="stat-row">
        <span className="stat-label">Worst:</span>
        <span className="stat-value">{formatTime(stats.worst)}</span>
      </div>
      <div className="stat-divider" />
      <div className="stat-row">
        <span className="stat-label">ao5:</span>
        <span className="stat-value">{formatTime(stats.current_ao5)}</span>
      </div>
      <div className="stat-row">
        <span className="stat-label">ao12:</span>
        <span className="stat-value">{formatTime(stats.current_ao12)}</span>
      </div>
      <div className="stat-row">
        <span className="stat-label">ao100:</span>
        <span className="stat-value">{formatTime(stats.current_ao100)}</span>
      </div>
      <div className="stat-divider" />
      <div className="stat-row">
        <span className="stat-label">Mean:</span>
        <span className="stat-value">{formatTime(stats.mean)}</span>
      </div>
      <div className="stat-row">
        <span className="stat-label">σ:</span>
        <span className="stat-value">
          {stats.std_dev !== null ? (stats.std_dev / 1000).toFixed(2) : '-'}
        </span>
      </div>
    </div>
  );
};
```

### 7.2 Solve History Component
**File: `frontend/src/components/SolveHistory.tsx`**

```tsx
import React from 'react';
import { Solve } from '../types';
import './SolveHistory.css';

interface SolveHistoryProps {
  solves: Solve[];
  onDelete: (id: string) => void;
  onPenaltyChange: (id: string, penalty: '+2' | 'DNF' | null) => void;
}

function formatTime(ms: number, penalty: string | null): string {
  let time = ms;
  if (penalty === '+2') time += 2000;

  const seconds = time / 1000;
  if (seconds >= 60) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toFixed(2).padStart(5, '0')}`;
  }
  return seconds.toFixed(2);
}

export const SolveHistory: React.FC<SolveHistoryProps> = ({
  solves,
  onDelete,
  onPenaltyChange,
}) => {
  return (
    <div className="solve-history">
      <h3>Solve History</h3>
      <div className="solve-list">
        {solves.map((solve, index) => (
          <div key={solve._id} className="solve-item">
            <span className="solve-number">{solves.length - index}.</span>
            <span className={`solve-time ${solve.penalty === 'DNF' ? 'dnf' : ''}`}>
              {solve.penalty === 'DNF' ? 'DNF' : formatTime(solve.time_ms, solve.penalty)}
              {solve.penalty === '+2' && <sup>+2</sup>}
            </span>
            <div className="solve-actions">
              <button
                className={solve.penalty === '+2' ? 'active' : ''}
                onClick={() => onPenaltyChange(solve._id, solve.penalty === '+2' ? null : '+2')}
              >
                +2
              </button>
              <button
                className={solve.penalty === 'DNF' ? 'active' : ''}
                onClick={() => onPenaltyChange(solve._id, solve.penalty === 'DNF' ? null : 'DNF')}
              >
                DNF
              </button>
              <button className="delete" onClick={() => onDelete(solve._id)}>
                ×
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
```

---

## Bug Fixes Required

### M' Move Bug (Critical)

**Current Issue:**
The M' (middle prime) move in `RubiksCube.py` creates invalid cube states that the Kociemba solver rejects. After M' from a solved state, the cube string fails validation.

**Location:** `RubiksCube_project/RubiksCube/RubiksCube.py` lines 296-310

**Root Cause:**
The M slice should rotate the middle layer (between L and R faces) in the same direction as L'. The current implementation likely:
1. Incorrectly cycles edge pieces
2. Does not properly handle the face orientation

**Fix Approach:**
```python
def move_m_prime(state: dict) -> dict:
    """M' moves the middle slice in the same direction as R"""
    state = copy.deepcopy(state)

    # M' cycle: U center column -> F center column -> D center column -> B center column (reversed)
    # Save U center column
    temp = [state['U'][0][1], state['U'][1][1], state['U'][2][1]]

    # U <- B (reversed)
    state['U'][0][1] = state['B'][2][1]
    state['U'][1][1] = state['B'][1][1]
    state['U'][2][1] = state['B'][0][1]

    # B <- D (reversed)
    state['B'][0][1] = state['D'][2][1]
    state['B'][1][1] = state['D'][1][1]
    state['B'][2][1] = state['D'][0][1]

    # D <- F
    state['D'][0][1] = state['F'][0][1]
    state['D'][1][1] = state['F'][1][1]
    state['D'][2][1] = state['F'][2][1]

    # F <- temp (U)
    state['F'][0][1] = temp[0]
    state['F'][1][1] = temp[1]
    state['F'][2][1] = temp[2]

    return state
```

**Verification:**
After implementing, test with:
1. M' from solved state should produce valid Kociemba string
2. M M' should return to solved state
3. M' M' M' M' (4x) should return to solved state

---

## Security Considerations

### 1. Input Validation (Backend)

**Move strings:**
```python
import re

VALID_MOVE_PATTERN = re.compile(r"^[URFDLBMES]'?2?$")

def validate_move(move: str) -> bool:
    return bool(VALID_MOVE_PATTERN.match(move))
```

**Solve times:**
```python
def validate_solve_time(time_ms: int) -> bool:
    return 500 <= time_ms <= 3600000  # 0.5s to 1 hour
```

### 2. Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/solve")
@limiter.limit("10/minute")  # Solver is computationally expensive
async def solve_cube(request: Request, data: SolveRequest):
    ...
```

### 3. CORS Configuration

```python
# Development
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

# Production (update with actual domain)
# origins = ["https://yourdomain.com"]
```

### 4. MongoDB Security
- Use parameterized queries (Motor handles this automatically)
- Never interpolate user input directly into queries
- Validate ObjectId format before querying

---

## Verification Checklist

### Backend
- [ ] FastAPI server starts without errors
- [ ] `/api/cube/reset` returns valid solved state
- [ ] `/api/cube/move` applies moves correctly
- [ ] `/api/cube/scramble` generates valid scrambles
- [ ] `/api/cube/solve` returns valid solutions
- [ ] MongoDB connection works
- [ ] CRUD operations on solves work
- [ ] Statistics calculation is accurate

### Frontend
- [ ] React app builds and runs
- [ ] 3D cube displays all 6 faces correctly
- [ ] Colors update when moves are applied
- [ ] Timer starts with spacebar hold
- [ ] Inspection countdown works
- [ ] Timer stops with any key press
- [ ] Penalties (+2, DNF) apply correctly
- [ ] Solves are saved to database
- [ ] Statistics update after each solve
- [ ] Solve history displays correctly

### Integration
- [ ] Frontend communicates with backend
- [ ] Scramble → solve → verify solved works end-to-end
- [ ] Timer flow: inspection → solve → save → stats update

---

## Files to Remove (Pygame Cleanup)

After migration is complete, these can be removed:
- Pygame import and initialization
- `screen`, `clock` variables
- All `draw*Face()` methods
- `handleKeyPress()` method (replaced by React hooks)
- `run()` game loop method
- PIL/Pillow image creation code

---

## Backend Requirements
**File: `backend/requirements.txt`**

```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
motor>=3.3.0
pydantic>=2.5.0
kociemba>=1.2.0
python-multipart>=0.0.6
slowapi>=0.1.9
```

---

## Running the Application

### Start MongoDB
```bash
# Using Docker (recommended)
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Or install MongoDB locally
```

### Start Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Start Frontend
```bash
cd frontend
npm install
npm run dev
```

### Access Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
