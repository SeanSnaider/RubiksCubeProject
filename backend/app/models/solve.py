from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SolveRecord(BaseModel):
    """A single solve attempt stored in MongoDB"""
    time_ms: int                    # Time in milliseconds (12345 = 12.345s)
    scramble: str                   # The scramble used
    penalty: Optional[str] = None   # "+2", "DNF", or None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CreateSolveRequest(BaseModel):
    """POST request body - what the client sends to create a solve"""
    time_ms: int
    scramble: str
    penalty: Optional[str] = None


class UpdatePenaltyRequest(BaseModel):
    """PATCH request body - for updating just the penalty"""
    penalty: Optional[str] = None
