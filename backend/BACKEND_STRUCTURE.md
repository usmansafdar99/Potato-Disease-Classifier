# Potato Disease Classification System
# Backend Project Structure and Guidelines

This directory contains all backend application code.

## Directory Structure

```
backend/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration settings
│   ├── routes/              # API endpoints
│   │   ├── __init__.py
│   │   ├── health.py        # Health check endpoints
│   │   └── predict.py       # Prediction endpoints
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── model_service.py # ML model service
│   ├── schemas/             # Pydantic models
│   │   ├── __init__.py
│   │   └── prediction.py    # Request/response schemas
│   └── utils/               # Utilities
│       ├── __init__.py
│       ├── logger.py        # Logging setup
│       ├── validators.py    # Input validation
│       └── exceptions.py    # Custom exceptions
├── main.py                  # FastAPI application entry point
└── requirements.txt         # Python dependencies
```

## Module Descriptions

### `config.py`
Central configuration management. Contains all application settings like:
- Model paths and versions
- Image processing parameters
- API settings
- Disease class definitions

### `routes/`
API endpoint definitions:
- `health.py`: Health check and readiness probes
- `predict.py`: Image upload and prediction endpoint

### `services/`
Business logic layer:
- `model_service.py`: Handles model loading, preprocessing, and inference

### `schemas/`
Pydantic models for request/response validation:
- `prediction.py`: Structured data for predictions

### `utils/`
Helper functions:
- `logger.py`: Centralized logging setup
- `validators.py`: Input validation functions
- `exceptions.py`: Custom exception classes

## Best Practices

1. **Separation of Concerns**: Routes handle HTTP, services handle business logic
2. **Dependency Injection**: Use FastAPI dependencies for model service
3. **Validation**: Use Pydantic schemas for all I/O
4. **Logging**: Use centralized logger for debugging
5. **Error Handling**: Use custom exceptions and HTTP exceptions
