# Skin Cancer Detection Project

This project aims to develop a model for skin cancer detection based on images. The workflow includes data preprocessing, feature engineering, and model training using neural networks.

## Project Structure

The project is organized as follows:

```
skin-cancer-detection
├── conf
│   ├── base
│   │   ├── catalog.yml          # Data catalog for data sources and outputs
│   │   ├── logging.yml          # Logging configuration
│   │   └── parameters.yml       # Project parameters and hyperparameters
│   └── local
│       └── credentials.yml      # Local environment credentials
├── data
│   ├── 01_raw                   # Raw data files (skin cancer images)
│   ├── 02_intermediate          # Intermediate data files
│   ├── 03_primary               # Primary datasets for analysis
│   ├── 04_feature               # Feature-engineered datasets
│   └── 05_model_input           # Datasets ready for model input
├── logs                         # Log files generated during execution
├── notebooks
│   └── exploratory.ipynb        # Jupyter notebook for exploratory data analysis
├── src
│   ├── skin_cancer_detection
│   │   ├── __init__.py          # Marks the directory as a Python package
│   │   ├── nodes
│   │   │   ├── data_preprocessing.py  # Functions for image preprocessing
│   │   │   └── model_training.py      # Functions for model training
│   │   ├── pipelines
│   │   │   ├── __init__.py          # Marks the pipelines directory as a Python package
│   │   │   └── pipeline.py          # Defines the Kedro pipeline
│   │   └── settings.py              # Project settings and configurations
│   ├── requirements.txt             # Python dependencies for the project
│   └── setup.py                     # Packaging information for the project
└── README.md                       # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd skin-cancer-detection
   ```

2. Install the required dependencies:
   ```
   pip install -r src/requirements.txt
   ```

3. Configure your local environment by updating `conf/local/credentials.yml` with any necessary credentials.

## Usage Guidelines

- Use the `notebooks/exploratory.ipynb` for exploratory data analysis to understand the dataset better.
- The data preprocessing and model training are orchestrated through the Kedro pipeline defined in `src/skin_cancer_detection/pipelines/pipeline.py`.
- Adjust parameters in `conf/base/parameters.yml` to fine-tune the model training process.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.