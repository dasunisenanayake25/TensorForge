from fastapi import APIRouter, Depends, HTTPException
from app.schemas import TicketRequest, PredictResponse, BatchRequest, BatchResponse
from app.config import verify_api_key, MODEL_VERSION_TAG
from app.services.inference import predict_ticket_category

router = APIRouter(dependencies=[Depends(verify_api_key)])

@router.post("/predict", response_model=PredictResponse)
async def predict_single(request: TicketRequest):
    res = predict_ticket_category(request.ticket_id, request.text)
    return PredictResponse(**res)

@router.post("/predict/batch", response_model=BatchResponse)
async def predict_batch(request: BatchRequest):
    # Check for duplicate ticket IDs
    ticket_ids = [t.ticket_id for t in request.tickets if t.ticket_id]
    if len(ticket_ids) != len(set(ticket_ids)):
        raise HTTPException(status_code=422, detail="Duplicate ticket_id found in batch")

    results_list = []
    for ticket in request.tickets:
        res = predict_ticket_category(ticket.ticket_id, ticket.text)
        results_list.append(PredictResponse(**res))
        
    meta = {
        "count": len(results_list),
        "model_version": MODEL_VERSION_TAG,
        "processing_time_ms": 100
    }
    return BatchResponse(predictions=results_list, meta=meta)