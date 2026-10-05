"""
Solve history models.

Request bodies for the /api/solves endpoints and the record stored in MongoDB.
`Literal` types make Pydantic reject an unknown penalty or mode with a 422
before any handler runs.
"""
from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime, timezone

# Penalties a solve can carry, matching the frontend's Solve type.
Penalty = Optional[Literal["+2", "DNF"]]

# Which mode recorded the solve.
SolveMode = Literal["cube", "timer"]

# Fastest time accepted. Anything quicker is a misfire, not a solve.
MIN_SOLVE_TIME_MS = 500


def utc_now() -> datetime:
    """Return the current time as a timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


class SolveRecord(BaseModel):
    """A single solve attempt stored in MongoDB"""
    time_ms: int                    # Time in milliseconds (12345 = 12.345s)
    scramble: str                   # The scramble used (empty string for timer mode)
    penalty: Penalty = None         # "+2", "DNF", or None
    mode: SolveMode = "cube"        # "cube" or "timer"
    created_at: datetime = Field(default_factory=utc_now)


class CreateSolveRequest(BaseModel):
    """POST request body - what the client sends to create a solve"""
    time_ms: int = Field(ge=MIN_SOLVE_TIME_MS)
    scramble: str
    penalty: Penalty = None
    mode: SolveMode = "cube"


class UpdatePenaltyRequest(BaseModel):
    """PATCH request body - for updating just the penalty"""
    penalty: Penalty = None
