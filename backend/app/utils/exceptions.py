"""Custom exceptions"""

class ModelNotLoadedError(Exception):
    """Raised when model is not loaded"""
    pass

class InvalidImageError(Exception):
    """Raised when image is invalid"""
    pass

class PredictionError(Exception):
    """Raised during prediction"""
    pass
