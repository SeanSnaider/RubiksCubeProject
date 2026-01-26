# Rubik's Cube Solver and Teaching Tool

A 3D Rubik's Cube simulator with a near-optimal solving algorithm and step-by-step tutorial mode. Built by someone who's been speedcubing for 10+ years (sub-7 seconds).

![Python](https://img.shields.io/badge/Python-3.x-blue)
![PyGame](https://img.shields.io/badge/PyGame-2.x-green)

## Features

**Solver**
- Implements Kociemba's two-phase algorithm
- Computes near-optimal solutions (≤20 moves) in under 1 second
- Real-time 3D rendering with PyGame

**Teaching Mode**
- Step-by-step tutorial for learning to solve the cube
- State validation at each stage—cross, corners, second layer, top face
- Blocks progression until each stage is completed correctly
- Designed to teach the CFOP method fundamentals

**Controls**
- Intuitive keyboard-based controls for cube manipulation
- Demonstrated to 20+ peers who preferred it over existing online platforms

## Installation

```bash
git clone https://github.com/SeanSnaider/RubiksCubeProject.git
cd RubiksCubeProject
pip install pygame
python RubiksCube_project/main.py
```

## Controls

Keybinds follow a speedcuber-friendly layout (similar to csTimer).

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

### Utility

| Key | Action |
|-----|--------|
| [ | Scramble cube |
| ] | Reset cube |
| \ | Solve (Kociemba algorithm) |
| = | Clear move history |

*(Adjust keybindings based on your actual implementation)*

## How the Solver Works

The Kociemba algorithm solves the cube in two phases:

1. **Phase 1**: Reduce the cube to a state where only certain moves are needed (the "G1" group)
2. **Phase 2**: Solve from the reduced state to completion

This approach finds solutions averaging 18-19 moves, with a maximum of 20.

## Why I Built This

I've been cubing since I was a kid and wanted to create a tool that actually teaches the solving process rather than just showing a solution. Most online solvers dump a move sequence on you—this one makes you learn each stage.

## Tech Stack

- **Python** — Core logic
- **PyGame** — 3D rendering and UI

## Author

Sean Snaider — [seansnaider.vercel.app](https://seansnaider.vercel.app) · [LinkedIn](https://linkedin.com/in/seansnaider)
