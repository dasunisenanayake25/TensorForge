from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class TicketRequest(BaseModel):
    ticket_id: Optional[str] = Field(None, max_length=64)
    channel: Literal["email", "chat", "call_transcript"]
    subject: Optional[str] = Field("", max_length=500)
    text: str = Field(..., min_length=1, max_length=10000)

class PredictResponse(BaseModel):
    ticket_id: Optional[str] = None
    category: str
    secondary_category: Optional[str] = None
    team: str
    is_urgent: bool
    confidence: float
    model_version: str
    needs_human_review: Optional[bool] = None

class BatchRequest(BaseModel):
    tickets: List[TicketRequest] = Field(..., min_length=1, max_length=100)

class BatchResponse(BaseModel):
    predictions: List[PredictResponse]
    meta: Optional[dict] = None

class BatchJobRequest(BaseModel):
    tickets: List[TicketRequest] = Field(..., min_length=1, max_length=5000)

class BatchJobStatus(BaseModel):
    job_id: str
    status: Literal["queued", "running", "succeeded", "failed", "cancelled"]
    total: int
    processed: int
    created_at: str
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    expires_at: Optional[str] = None
    model_version: str
    error: Optional[dict] = None

class BatchJobResults(BaseModel):
    job_id: str
    status: Literal["succeeded"]
    total: int
    offset: int
    limit: int
    next_offset: Optional[int]
    model_version: str
    predictions: List[PredictResponse]