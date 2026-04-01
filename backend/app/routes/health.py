"""Health check routes"""
from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/health")

@router.get("")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Potato Disease Classification API"
    }

@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    try:
        return {
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service not ready")
