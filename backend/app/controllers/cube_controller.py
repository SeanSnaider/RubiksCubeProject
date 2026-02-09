"""
Cube Controller - REST API Endpoints

This is the "C" in MVC - it handles HTTP requests, delegates to services,
and returns HTTP responses. Controllers should be thin - they just:
1. Parse the request
2. Call the appropriate service function
3. Return the response

FastAPI's APIRouter groups related endpoints together.
The @router.get/post decorators define the HTTP method and path.
"""
from fastapi import APIRouter, HTTPException
from app.models.cube import CubeState, MoveRequest, SolveRequest
from app.services import cube_service

# Create a router instance - this will be registered in main.py
router = APIRouter()


@router.get("/reset")
def reset_cube():
    """
    GET /api/cube/reset

    Returns a solved cube state. Use this to initialize or reset the cube.

    Response: CubeState with all faces in solved position
    """
    return cube_service.get_solved_state()


@router.post("/move")
def apply_moves(request: MoveRequest):
    """
    POST /api/cube/move

    Apply one or more moves to the cube and return the new state.

    Request body:
    {
        "state": { ... current cube state ... },
        "moves": "R U R' U'"
    }

    Response: New CubeState after applying moves
    """
    try:
        new_state = cube_service.apply_moves(
            request.state.model_dump(),  # Convert Pydantic model to dict
            request.moves
        )
        return new_state
    except ValueError as e:
        # Return 400 Bad Request for invalid moves
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/scramble")
def generate_scramble():
    """
    GET /api/cube/scramble

    Generate a random scramble and return both the scramble string
    and the resulting cube state.

    Response:
    {
        "scramble": "R U R' U' F' ...",
        "state": { ... scrambled cube state ... }
    }
    """
    scramble = cube_service.generate_scramble()
    state = cube_service.apply_moves(
        cube_service.get_solved_state(),
        scramble
    )
    return {"scramble": scramble, "state": state}


@router.post("/solve")
def solve_cube(request: SolveRequest):
    """
    POST /api/cube/solve

    Get the optimal solution for the current cube state using
    the Kociemba two-phase algorithm.

    Request body:
    {
        "state": { ... current cube state ... }
    }

    Response:
    {
        "solution": "U R2 F' ..."
    }

    Errors:
    - 400: Invalid/unsolvable cube state
    """
    try:
        solution = cube_service.get_solution(request.state.model_dump())
        return {"solution": solution}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/validate")
def validate_cube(request: SolveRequest):
    """
    POST /api/cube/validate

    Check if a cube state is valid and solvable.

    Request body:
    {
        "state": { ... cube state to validate ... }
    }

    Response:
    {
        "valid": true/false
    }
    """
    is_valid = cube_service.validate_state(request.state.model_dump())
    return {"valid": is_valid}
