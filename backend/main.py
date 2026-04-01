"""
Potato Disease Classification API
FastAPI Backend for deep learning predictions
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.routes import health, predict
from app.services.model_service import ModelService
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

# Initialize model service on startup
model_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - startup and shutdown"""
    global model_service
    # Startup
    logger.info("Application startup - Loading model...")
    model_service = ModelService()
    await model_service.load_model()
    logger.info("Model loaded successfully")
    
    yield
    
    # Shutdown
    logger.info("Application shutdown...")

# Create FastAPI app
app = FastAPI(
    title="Potato Disease Classification API",
    description="API for classifying potato plant diseases using deep learning",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(health.router, tags=["Health"])
app.include_router(predict.router, tags=["Prediction"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Potato Disease Classification API",
        "documentation": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
