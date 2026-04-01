"""Logging configuration"""
import logging
import sys
from app.config import LOG_LEVEL, LOG_FORMAT

def setup_logger(name: str) -> logging.Logger:
    """
    Setup logger with consistent configuration
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger
