"""Prediction routes"""
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from typing import List
import io

from app.schemas.prediction import PredictionResponse, HealthCheckResponse
from app.services.model_service import ModelService
from app.utils.logger import setup_logger
from app.utils.validators import validate_image

logger = setup_logger(__name__)
router = APIRouter(prefix="/api/v1")

def get_model_service() -> ModelService:
    """Dependency injection for model service"""
    from main import model_service
    if model_service is None:
        raise HTTPException(status_code=503, detail="Model service not initialized")
    return model_service

@router.post("/predict", response_model=PredictionResponse)
async def predict(
    file: UploadFile = File(...),
    model_service: ModelService = Depends(get_model_service)
):
    """
    Predict disease from uploaded image
    
    - **file**: Image file (jpg, png, webp)
    - Returns: Prediction results with confidence scores
    """
    try:
        # Read file
        contents = await file.read()
        
        # Validate image
        is_valid, error_msg = validate_image(contents, file.filename)
        if not is_valid:
            logger.warning(f"Invalid image: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Make prediction
        logger.info(f"Processing prediction for file: {file.filename}")
        prediction = await model_service.predict(io.BytesIO(contents))
        
        logger.info(f"Prediction completed: {prediction}")
        return prediction
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during prediction")

@router.get("/model/info", response_model=dict)
async def model_info(model_service: ModelService = Depends(get_model_service)):
    """Get model information"""
    try:
        return {
            "model_version": "1.0",
            "classes": model_service.class_names,
            "input_size": (224, 224),
            "framework": "TensorFlow",
        }
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving model information")
