"""Configuration settings for the application"""
import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Model configuration
MODEL_PATH = os.getenv("MODEL_PATH", str(PROJECT_ROOT / "models" / "potato_model.keras"))
MODEL_VERSION = "1.0"

# Image configuration
IMAGE_SIZE = (224, 224)
MAX_IMAGE_SIZE_MB = 10
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

# Disease classes
DISEASE_CLASSES = [
    "Early Blight",
    "Late Blight",
    "Healthy"
]

# Prediction threshold
CONFIDENCE_THRESHOLD = 0.5

# API configuration
API_PREFIX = "/api/v1"

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
