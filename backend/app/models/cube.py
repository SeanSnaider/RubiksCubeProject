"""
Cube State Models

Pydantic models define the shape of your data and automatically validate
incoming requests. If someone sends invalid data (like a 2x2 face instead
of 3x3), Pydantic will reject it with a clear error message.

The cube state uses face-based representation:
- U (Up/White), D (Down/Yellow)
- L (Left/Orange), R (Right/Red)
- F (Front/Green), B (Back/Blue)

Each face is a 3x3 grid represented as a list of 3 rows.
"""
from pydantic import BaseModel, field_validator
from typing import List


class CubeState(BaseModel):
    """
    Represents a 3x3 Rubik's Cube state.

    Each face is a 3x3 grid stored as a list of lists:
    [
        [corner, edge, corner],   # top row
        [edge,   center, edge],   # middle row
        [corner, edge, corner]    # bottom row
    ]

    Colors are represented by the face they belong to on a solved cube:
    'U' = White, 'D' = Yellow, 'L' = Orange, 'R' = Red, 'F' = Green, 'B' = Blue
    """
    U: List[List[str]]  # Up face (3x3)
    D: List[List[str]]  # Down face
    L: List[List[str]]  # Left face
    R: List[List[str]]  # Right face
    F: List[List[str]]  # Front face
    B: List[List[str]]  # Back face

    @field_validator('U', 'D', 'L', 'R', 'F', 'B')
    @classmethod
    def validate_face(cls, v):
        """
        Validates that each face is exactly 3x3 with valid colors.

        This decorator (@field_validator) tells Pydantic to run this
        function on each face field before accepting the data.
        """
        # Check dimensions
        if len(v) != 3:
            raise ValueError("Each face must have exactly 3 rows")
        for row in v:
            if len(row) != 3:
                raise ValueError("Each row must have exactly 3 cells")

        # Check colors
        valid_colors = {'U', 'D', 'L', 'R', 'F', 'B'}
        for row in v:
            for cell in row:
                if cell not in valid_colors:
                    raise ValueError(f"Invalid color: {cell}. Must be one of {valid_colors}")
        return v


class MoveRequest(BaseModel):
    """
    Request model for applying moves to a cube.

    Example:
    {
        "state": { ... cube state ... },
        "moves": "R U R' U'"
    }
    """
    state: CubeState
    moves: str  # Move notation like "R U R' U'" or "F2 D' B"


class SolveRequest(BaseModel):
    """
    Request model for getting a solution for a cube state.
    Contains just the current cube state to solve.
    """
    state: CubeState
