import streamlit as st
<<<<<<< HEAD
import numpy as np
from PIL import Image
import tensorflow as tf

st.title("🥔 Potato Disease Classifier")

# Dummy load (replace later with real path or download)
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("models/potato_model.keras")

model = load_model()

uploaded_file = st.file_uploader("Upload Potato Leaf Image", type=["jpg","png","jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Predict"):
        img = image.resize((224,224))
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        prediction = model.predict(img)
        st.write("Prediction:", prediction)
=======
import tensorflow as tf
import numpy as np
from PIL import Image
import os
from pathlib import Path

# --- Configuration ---
IMAGE_SIZE = (224, 224)
DISEASE_CLASSES = ["Early Blight", "Late Blight", "Healthy"]

# --- Page Config ---
st.set_page_config(
    page_title="Potato Disease Classifier",
    page_icon="🥔",
    layout="centered"
)

# --- Define Paths ---
# Use the keras file if it exists, otherwise use the saved model folder
if Path("models/potato_model.keras").exists():
    MODEL_PATH = "models/potato_model.keras"
else:
    MODEL_PATH = "1"

@st.cache_resource
def load_disease_model():
    """Loads the model exactly once, caching it using Streamlit's cache_resource"""
    try:
        if Path(MODEL_PATH).is_file():
            model = tf.keras.models.load_model(MODEL_PATH)
        else:
            model = tf.keras.models.load_model(MODEL_PATH)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def preprocess_image(image: Image.Image) -> np.ndarray:
    """Preprocess image for model input."""
    # Convert to RGB
    image = image.convert("RGB")
    # Resize
    image = image.resize(IMAGE_SIZE, Image.LANCZOS)
    # Convert to array and normalize
    array = np.asarray(image).astype(np.float32) / 255.0
    # Add batch dimension
    array = np.expand_dims(array, axis=0)
    # Ensure C order
    array = np.ascontiguousarray(array)
    return array

def predict(model, image_array: np.ndarray):
    """Run prediction on preprocessed image."""
    if hasattr(model, "predict"):
        predictions = model.predict(image_array, verbose=0)
    else:
        # Handle TF SavedModel callable
        input_tensor = tf.convert_to_tensor(image_array, dtype=tf.float32)
        output = model(input_tensor)
        if isinstance(output, dict):
            key = next(iter(output))
            predictions = output[key]
        else:
            predictions = output
            
    prediction_array = np.array(predictions)[0]
    predicted_idx = int(np.argmax(prediction_array))
    confidence = float(prediction_array[predicted_idx])
    predicted_class = DISEASE_CLASSES[predicted_idx]
    
    return predicted_class, confidence, prediction_array

# --- UI Layout ---
st.title("🥔 Potato Disease Classifier")
st.markdown("Upload a photo of a potato leaf to detect whether it is **Healthy**, or if it has **Early Blight** or **Late Blight**.")

# Show a loading spinner while the model loads
with st.spinner("Loading AI model..."):
    model = load_disease_model()

if model is None:
    st.error("Failed to load the model. Please check the model path and files.")
    st.stop()

uploaded_file = st.file_uploader("Upload Leaf Image (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_container_width=True)
    
    # Predict button
    if st.button("Analyze Image", type="primary"):
        with st.spinner("Analyzing..."):
            try:
                # Preprocess
                processed_img = preprocess_image(img)
                # Predict
                predicted_class, confidence, all_probs = predict(model, processed_img)
                
                # Display results
                st.success(f"**Prediction:** {predicted_class}")
                st.info(f"**Confidence:** {confidence * 100:.2f}%")
                
                # Show confidence for all classes
                st.write("---")
                st.write("### Detailed Confidence Scores")
                for i, class_name in enumerate(DISEASE_CLASSES):
                    st.write(f"- **{class_name}**: {float(all_probs[i]) * 100:.2f}%")
                    
            except Exception as e:
                st.error(f"Error during prediction: {e}")
>>>>>>> a401064 (Add Streamlit app.py and update requirements.txt for deployment)
