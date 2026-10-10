from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, Header, Response
import uuid
import datetime
from typing import Optional
from app.schemas import BatchJobRequest, BatchJobStatus, BatchJobResults, PredictResponse
from app.config import verify_api_key, MODEL_VERSION_TAG
from app.services.inference import predict_ticket_category

router = APIRouter(dependencies=[Depends(verify_api_key)])

# In-memory DB for MVP
JOBS_DB = {}

def process_job_in_background(job_id: str, tickets: list):
    JOBS_DB[job_id]["status"] = "running"
    JOBS_DB[job_id]["started_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    
    results = []
    for ticket in tickets:
        if JOBS_DB[job_id]["status"] == "cancelled":
            break # Stop processing if cancelled
            
        res = predict_ticket_category(ticket.ticket_id, ticket.text)
        results.append(PredictResponse(**res))
        JOBS_DB[job_id]["processed"] += 1
        
    if JOBS_DB[job_id]["status"] != "cancelled":
        JOBS_DB[job_id]["results"] = results
        JOBS_DB[job_id]["status"] = "succeeded"
        JOBS_DB[job_id]["finished_at"] = datetime.datetime.utcnow().isoformat() + "Z"
        # Expires in 6 hours
        expires = datetime.datetime.utcnow() + datetime.timedelta(hours=6)
        JOBS_DB[job_id]["expires_at"] = expires.isoformat() + "Z"

@router.post("/batch/jobs", status_code=202)
async def submit_job(
    request: BatchJobRequest, 
    background_tasks: BackgroundTasks, 
    response: Response,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key")
):
    ticket_ids = [t.ticket_id for t in request.tickets if t.ticket_id]
    if len(ticket_ids) != len(set(ticket_ids)):
        raise HTTPException(status_code=422, detail="Duplicate ticket_id found in batch")

    # Simple Idempotency handling
    if idempotency_key:
        for j_id, j_data in JOBS_DB.items():
            if j_data.get("idempotency_key") == idempotency_key:
                response.headers["Location"] = f"/batch/jobs/{j_id}"
                response.headers["Retry-After"] = "5"
                return BatchJobStatus(**j_data)

    job_id = str(uuid.uuid4())
    total = len(request.tickets)
    
    job_status = {
        "job_id": job_id,
        "status": "queued",
        "total": total,
        "processed": 0,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "started_at": None,
        "finished_at": None,
        "expires_at": None,
        "model_version": MODEL_VERSION_TAG,
        "error": None,
        "idempotency_key": idempotency_key
    }
    
    JOBS_DB[job_id] = job_status
    background_tasks.add_task(process_job_in_background, job_id, request.tickets)
    
    response.headers["Location"] = f"/batch/jobs/{job_id}"
    response.headers["Retry-After"] = "5"
    return BatchJobStatus(**job_status)

@router.get("/batch/jobs/{job_id}", response_model=BatchJobStatus)
async def get_job_status(job_id: str, response: Response):
    if job_id not in JOBS_DB:
        raise HTTPException(status_code=404, detail="Job not found")
        
    job = JOBS_DB[job_id]
    if job["status"] in ["queued", "running"]:
        response.headers["Retry-After"] = "5"
        
    return BatchJobStatus(**job)

@router.delete("/batch/jobs/{job_id}", status_code=204)
async def delete_job(job_id: str):
    if job_id not in JOBS_DB:
        raise HTTPException(status_code=404, detail="Job not found")
    
    JOBS_DB[job_id]["status"] = "cancelled"
    JOBS_DB[job_id]["finished_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    if "results" in JOBS_DB[job_id]:
        del JOBS_DB[job_id]["results"]
    return

@router.get("/batch/jobs/{job_id}/results", response_model=BatchJobResults)
async def get_job_results(job_id: str, offset: int = 0, limit: int = 5000):
    if job_id not in JOBS_DB:
        raise HTTPException(status_code=404, detail="Job not found")
        
    job = JOBS_DB[job_id]
    
    if job.get("expires_at") and datetime.datetime.utcnow().isoformat() + "Z" > job["expires_at"]:
        raise HTTPException(status_code=410, detail="Job expired")
        
    if job["status"] != "succeeded":
        raise HTTPException(status_code=409, detail="Job not ready")
        
    results = job.get("results", [])
    paginated = results[offset:offset+limit]
    next_offset = offset + limit if (offset + limit) < len(results) else None
    
    return BatchJobResults(
        job_id=job_id,
        status="succeeded",
        total=len(results),
        offset=offset,
        limit=limit,
        next_offset=next_offset,
        model_version=MODEL_VERSION_TAG,
        predictions=paginated
    )