# settings.py

import os

PROJECT_NAME = "skin-cancer-detection"
DATA_DIR = os.path.join(os.getcwd(), "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "01_raw")
INTERMEDIATE_DATA_DIR = os.path.join(DATA_DIR, "02_intermediate")
PRIMARY_DATA_DIR = os.path.join(DATA_DIR, "03_primary")
FEATURE_DATA_DIR = os.path.join(DATA_DIR, "04_feature")
MODEL_INPUT_DATA_DIR = os.path.join(DATA_DIR, "05_model_input")
LOGS_DIR = os.path.join(os.getcwd(), "logs")

# Model parameters
MODEL_PARAMS = {
    "learning_rate": 0.001,
    "batch_size": 32,
    "num_epochs": 50,
}

# Image preprocessing parameters
IMAGE_PARAMS = {
    "image_size": (224, 224),
    "normalization": True,
    "augmentation": {
        "rotation_range": 20,
        "width_shift_range": 0.2,
        "height_shift_range": 0.2,
        "shear_range": 0.2,
        "zoom_range": 0.2,
        "horizontal_flip": True,
        "fill_mode": "nearest",
    },
}