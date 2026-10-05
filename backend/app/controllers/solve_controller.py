"""
Solve Controller - REST API endpoints for solve history.

CRUD over the `solves` MongoDB collection. Every endpoint returns 503 if the
server couldn't reach MongoDB at startup (see `get_database()`), and 404 for an
id that is malformed or doesn't match a solve.
"""
from typing import Literal, Optional

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException

from app.database import get_database
from app.models.solve import SolveRecord, CreateSolveRequest, UpdatePenaltyRequest

router = APIRouter()


def parse_solve_id(solve_id: str) -> ObjectId:
    """Convert a path id to a MongoDB ObjectId.

    Args:
        solve_id: The id from the URL.

    Returns:
        The matching ObjectId.

    Raises:
        HTTPException: 404 if the id isn't a valid ObjectId, since no solve
            can have it. Without this, bson raises and the client gets a 500.
    """
    try:
        return ObjectId(solve_id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=404, detail=f"Solve not found: {solve_id}")


@router.get("/")
async def list_solves(
    limit: int = 100,
    offset: int = 0,
    mode: Optional[Literal["cube", "timer"]] = None,
):
    """
    GET /api/solves?limit=100&offset=0&mode=cube
    mode filter: "cube" includes legacy records with no mode field.
    """
    db = await get_database()
    if mode == "cube":
        query = {"$or": [{"mode": "cube"}, {"mode": {"$exists": False}}]}
    elif mode == "timer":
        query = {"mode": "timer"}
    else:
        query = {}
    cursor = db.solves.find(query).sort("created_at", -1).skip(offset).limit(limit)
    solves = await cursor.to_list(length=limit)
    for solve in solves:
        solve["_id"] = str(solve["_id"])
    return solves


@router.post("/")
async def create_solve(solve: CreateSolveRequest):
    """
    POST /api/solves
    Body: {"time_ms": 12345, "scramble": "R U R'...", "penalty": null, "mode": "cube"}

    Times under 500 ms are rejected with 422 as misfires.
    """
    db = await get_database()
    record = SolveRecord(
        time_ms=solve.time_ms,
        scramble=solve.scramble,
        penalty=solve.penalty,
        mode=solve.mode,
    )
    result = await db.solves.insert_one(record.model_dump())
    return {"id": str(result.inserted_id)}


@router.delete("/{solve_id}")
async def delete_solve(solve_id: str):
    """
    DELETE /api/solves/{solve_id}
    """
    object_id = parse_solve_id(solve_id)
    db = await get_database()
    result = await db.solves.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Solve not found: {solve_id}")
    return {"deleted": True}


@router.patch("/{solve_id}")
async def update_penalty(solve_id: str, request: UpdatePenaltyRequest):
    """
    PATCH /api/solves/{solve_id}
    Body: {"penalty": "+2"}, {"penalty": "DNF"} or {"penalty": null}

    An unknown penalty is rejected with 422 by the request model.
    """
    object_id = parse_solve_id(solve_id)
    db = await get_database()
    result = await db.solves.update_one(
        {"_id": object_id},
        {"$set": {"penalty": request.penalty}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Solve not found: {solve_id}")
    return {"updated": True}
