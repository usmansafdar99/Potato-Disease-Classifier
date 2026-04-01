"""Image preprocessing utilities for model prediction."""
from io import BytesIO
from typing import Tuple, Union

import numpy as np
from PIL import Image

from app.config import IMAGE_SIZE


def preprocess_image(image_input: Union[BytesIO, bytes, Image.Image]) -> np.ndarray:
    """Preprocess image for model input.

    Supports TensorFlow/PyTorch formats as Numpy arrays.

    Steps:
    - Load image from bytes/BytesIO/PIL
    - Convert to RGB
    - Resize to IMAGE_SIZE
    - Normalize pixel values to [0, 1]
    - Add batch dimension (1, H, W, C)

    Returns:
        np.ndarray: preprocessed input.
    """
    # Load PIL image from bytes-like input
    if isinstance(image_input, (bytes, bytearray)):
        image = Image.open(BytesIO(image_input))
    elif isinstance(image_input, BytesIO):
        image = Image.open(image_input)
    elif isinstance(image_input, Image.Image):
        image = image_input
    else:
        raise TypeError("Unsupported image input type")

    image = image.convert("RGB")
    image = image.resize(IMAGE_SIZE, Image.LANCZOS)

    array = np.asarray(image).astype(np.float32) / 255.0

    # Batch dimension
    array = np.expand_dims(array, axis=0)

    # Ensure C order
    array = np.ascontiguousarray(array)

    return array
