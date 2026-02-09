from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database import get_database
from app.models.solve import SolveRecord, CreateSolveRequest, UpdatePenaltyRequest

router = APIRouter()


@router.get("/")
async def list_solves(limit: int = 100, offset: int = 0):
    """
    GET /api/solves?limit=100&offset=0
    """
    db = await get_database()
    cursor = db.solves.find().sort("created_at", -1).skip(offset).limit(limit)
    solves = await cursor.to_list(length=limit)
    for solve in solves:
        solve["_id"] = str(solve["_id"])
    return solves


@router.post("/")
async def create_solve(solve: CreateSolveRequest):
    """
    POST /api/solves
    Body: {"time_ms": 12345, "scramble": "R U R'...", "penalty": null}
    """
    db = await get_database()
    record = SolveRecord(
        time_ms=solve.time_ms,
        scramble=solve.scramble,
        penalty=solve.penalty
    )
    if (solve.time_ms < 500):
        raise HTTPException(status_code=400, detail="impossible time twin")
    result = await db.solves.insert_one(record.model_dump())
    return {"id": str(result.inserted_id)}


@router.delete("/{solve_id}")
async def delete_solve(solve_id: str):
    """
    DELETE /api/solves/{solve_id}
    """
    db = await get_database()
    result = await db.solves.delete_one({"_id": ObjectId(solve_id)})
    if (result.deleted_count == 0):
        raise HTTPException(status_code=404, detail="Solve not found")
    return {"deleted": True}


@router.patch("/{solve_id}")
async def update_penalty(solve_id: str, request: UpdatePenaltyRequest):
    """
    PATCH /api/solves/{solve_id}
    Body: {"penalty": "+2"} or {"penalty": null}
    """
    penalty = request.penalty
    if (not (penalty == "+2" or penalty is None or penalty == "DNF")):
        raise HTTPException(status_code=400, detail="invalid penalty")
    db = await get_database()
    result = await db.solves.update_one(
        {"_id": ObjectId(solve_id)},
        {"$set": {"penalty": penalty}}
    )
    if (result.matched_count == 0):
        raise HTTPException(status_code=404, detail="unable to delete, invalid sovle id")
    return {"updated": True}
