from kedro.pipeline import node, Pipeline
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def create_model(input_shape):
    model = keras.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(1, activation='sigmoid')  # Assuming binary classification
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_model(X_train, y_train, input_shape, epochs=10, batch_size=32):
    model = create_model(input_shape)
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)
    return model

def model_training(X_train, y_train):
    input_shape = X_train.shape[1:]  # Assuming X_train is of shape (num_samples, height, width, channels)
    model = train_model(X_train, y_train, input_shape)
    return model

def create_pipeline():
    return Pipeline([
        node(
            func=model_training,
            inputs=["X_train", "y_train"],
            outputs="trained_model",
            name="model_training_node"
        )
    ])