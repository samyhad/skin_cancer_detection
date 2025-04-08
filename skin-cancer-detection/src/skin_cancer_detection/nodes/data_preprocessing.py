from kedro.pipeline import node, Pipeline
import cv2
import os
import numpy as np

def preprocess_images(input_dir: str, output_dir: str, image_size: tuple = (224, 224)):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(input_dir, filename)
            image = cv2.imread(img_path)

            # Resize image
            image = cv2.resize(image, image_size)

            # Normalize image
            image = image / 255.0

            # Save preprocessed image
            output_path = os.path.join(output_dir, filename)
            cv2.imwrite(output_path, image * 255)  # Convert back to uint8 for saving

def create_pipeline():
    return Pipeline(
        [
            node(
                func=preprocess_images,
                inputs=dict(input_dir="params:input_dir", output_dir="params:output_dir"),
                outputs="preprocessed_images",
                name="data_preprocessing_node",
            )
        ]
    )