"""Prediction response schemas"""
from pydantic import BaseModel, Field
from typing import Dict, List
from datetime import datetime

class PredictionResponse(BaseModel):
    """Prediction response model"""
    predicted_class: str = Field(..., description="Predicted disease class")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    confidence_percentage: float = Field(..., ge=0.0, le=100.0, description="Confidence as percentage")
    all_predictions: Dict[str, float] = Field(..., description="All class predictions with scores")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "predicted_class": "Early Blight",
                "confidence": 0.95,
                "confidence_percentage": 95.0,
                "all_predictions": {
                    "Early Blight": 0.95,
                    "Late Blight": 0.03,
                    "Healthy": 0.02
                },
                "timestamp": "2024-01-01T12:00:00"
            }
        }

class HealthCheckResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: datetime
    service: str
