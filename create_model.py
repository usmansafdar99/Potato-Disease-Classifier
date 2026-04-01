import tensorflow as tf
import numpy as np
from pathlib import Path

# Create a simple CNN model for potato disease classification
def create_potato_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(224, 224, 3)),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(3, activation='softmax')  # 3 classes: Early Blight, Late Blight, Healthy
    ])

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model

# Create and save the model
if __name__ == "__main__":
    print("Creating potato disease classification model...")

    # Create model
    model = create_potato_model()

    # Create dummy training data to initialize weights properly
    dummy_x = np.random.random((100, 224, 224, 3)).astype(np.float32)
    dummy_y = tf.keras.utils.to_categorical(np.random.randint(0, 3, 100), num_classes=3)

    # Train briefly to initialize weights
    print("Training model briefly to initialize weights...")
    model.fit(dummy_x, dummy_y, epochs=1, batch_size=32, verbose=1)

    # Save model
    model_path = Path("models/potato_model.keras")
    model_path.parent.mkdir(exist_ok=True)
    model.save(str(model_path))

    print(f"Model saved to: {model_path}")
    print("Model summary:")
    model.summary()

    # Test prediction
    test_input = np.random.random((1, 224, 224, 3)).astype(np.float32)
    prediction = model.predict(test_input, verbose=0)
    print(f"Test prediction shape: {prediction.shape}")
    print(f"Test prediction: {prediction[0]}")
    print(f"Predicted class: {np.argmax(prediction[0])}")