from kedro.pipeline import Pipeline, node
from skin_cancer_detection.nodes.data_preprocessing import preprocess_data
from skin_cancer_detection.nodes.model_training import train_model

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=preprocess_data,
                inputs="raw_images",
                outputs="preprocessed_images",
                name="data_preprocessing_node",
            ),
            node(
                func=train_model,
                inputs="preprocessed_images",
                outputs="model",
                name="model_training_node",
            ),
        ]
    )