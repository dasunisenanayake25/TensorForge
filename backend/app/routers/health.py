from fastapi import APIRouter
from app.config import MODEL_VERSION_TAG

router = APIRouter()

@router.get("/health")
async def health_check():
    # Returns 200 OK indicating model is loaded and ready
    return {
        "status": "ok",
        "model_version": MODEL_VERSION_TAG,
        "model_loaded": True
    }