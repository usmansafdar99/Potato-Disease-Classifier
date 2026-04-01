"""Validation utilities"""
from pathlib import Path
from app.config import ALLOWED_EXTENSIONS, MAX_IMAGE_SIZE_MB

def validate_image(file_content: bytes, filename: str) -> tuple[bool, str]:
    """
    Validate uploaded image
    
    Args:
        file_content: Image file content
        filename: Original filename
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check file size
    file_size_mb = len(file_content) / (1024 * 1024)
    if file_size_mb > MAX_IMAGE_SIZE_MB:
        return False, f"File size exceeds {MAX_IMAGE_SIZE_MB}MB limit"
    
    # Check file extension
    file_ext = Path(filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(ALLOWED_EXTENSIONS)
        return False, f"Invalid file type. Allowed types: {allowed}"
    
    # Check if file is a valid image
    try:
        from PIL import Image
        from io import BytesIO
        image = Image.open(BytesIO(file_content))
        image.verify()
        return True, ""
    except Exception as e:
        return False, f"Invalid image file: {str(e)}"
