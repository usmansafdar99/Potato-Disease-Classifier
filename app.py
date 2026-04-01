import streamlit as st
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
