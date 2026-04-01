"""Model service for predictions"""
import tensorflow as tf
import numpy as np
from io import BytesIO
from pathlib import Path
from PIL import Image
from typing import Optional
import logging

from app.config import MODEL_PATH, IMAGE_SIZE, DISEASE_CLASSES
from app.schemas.prediction import PredictionResponse
from app.utils.image_preprocessing import preprocess_image
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class ModelService:
    """Service for loading and using the model for predictions"""
    
    def __init__(self):
        self.model = None
        self.class_names = DISEASE_CLASSES
        
    async def load_model(self):
        """Load the pre-trained model"""
        logger.info(f"Loading model from {MODEL_PATH}")
        model_path = Path(MODEL_PATH)

        if model_path.is_file() and model_path.suffix in {".keras", ".h5"}:
            try:
                self.model = tf.keras.models.load_model(str(model_path))
                logger.info("Keras model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load Keras model file: {e}")
                self._load_dummy_model()

        elif model_path.is_dir():
            try:
                self.model = tf.keras.models.load_model(str(model_path))
                logger.info("SavedModel loaded using keras.load_model")
            except Exception as e:
                logger.warning(
                    "tf.keras.models.load_model failed for directory. "
                    f"Error: {e}"
                )
                try:
                    self.model = tf.keras.models.Sequential([
                        tf.keras.layers.Input(shape=(*IMAGE_SIZE, 3)),
                        tf.keras.layers.TFSMLayer(str(model_path), call_endpoint="serving_default")
                    ])
                    self.model.trainable = False
                    logger.info("Loaded model using TFSMLayer wrapper")
                except Exception as inner:
                    logger.error(f"TFSMLayer fallback failed: {inner}")
                    self._load_dummy_model()

        else:
            logger.warning(f"Model path not found: {MODEL_PATH}")
            self._load_dummy_model()

        if self.model is None:
            logger.warning("Model is not available; using dummy model")
            self._load_dummy_model()

        if hasattr(self.model, "summary"):
            try:
                self.model.summary()
            except Exception as e:
                logger.warning(f"Could not call model.summary(): {e}")
        else:
            logger.info("Loaded model does not support .summary().")

    def _load_dummy_model(self):
        logger.warning("Using dummy model for prediction (random output)")
        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Input(shape=(*IMAGE_SIZE, 3)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(len(self.class_names), activation="softmax")
        ])
        self.model.compile(optimizer="adam", loss="sparse_categorical_crossentropy")

    
    async def predict(self, image_file: BytesIO) -> PredictionResponse:
        """
        Make prediction on uploaded image
        
        Args:
            image_file: BytesIO object containing image data
            
        Returns:
            PredictionResponse with prediction results
        """
        try:
            # Load and preprocess image
            image_array = preprocess_image(image_file)

            # Make prediction
            if hasattr(self.model, "predict"):
                predictions = self.model.predict(image_array, verbose=0)
            else:
                # Handle TF SavedModel callable
                input_tensor = tf.convert_to_tensor(image_array, dtype=tf.float32)
                output = self.model(input_tensor)

                if isinstance(output, dict):
                    # choose first output key as prediction scores
                    key = next(iter(output))
                    predictions = output[key]
                else:
                    predictions = output

                predictions = np.array(predictions)

            prediction_array = np.array(predictions)[0]

            # Get predicted class
            predicted_idx = int(np.argmax(prediction_array))
            confidence = float(prediction_array[predicted_idx])
            predicted_class = self.class_names[predicted_idx]

            # Create predictions dictionary
            all_predictions = {
                self.class_names[i]: float(prediction_array[i])
                for i in range(min(len(self.class_names), len(prediction_array)))
            }
            
            response = PredictionResponse(
                predicted_class=predicted_class,
                confidence=confidence,
                confidence_percentage=confidence * 100,
                all_predictions=all_predictions
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}", exc_info=True)
            raise
