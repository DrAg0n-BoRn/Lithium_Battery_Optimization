from pathlib import Path
import os
import sys


# set root directory
ROOT_DIR = Path(__file__).resolve().parent
# Add the root directory to the system path
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))


### Directories ###
RAW_DATA_DIR = os.path.join(ROOT_DIR, "raw_data")
DATA_DIR = os.path.join(ROOT_DIR, "data")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")
LOGS_DIR = os.path.join(ROOT_DIR, "Logs")

FEATURE_ENG_DIR = os.path.join(DATA_DIR, "Feature Engineering")
ENGINEERED_CSVS_DIR = os.path.join(DATA_DIR, "Engineered Datasets")

MICE_IMPUTED_DATASETS_DIR = os.path.join(DATA_DIR, "MICE Imputed Datasets")
MICE_METRICS_DIR = os.path.join(RESULTS_DIR, "MICE Metrics")

VIF_IMPUTED_DATASETS_DIR = os.path.join(DATA_DIR, "VIF Imputed Datasets")
VIF_METRICS_DIR = os.path.join(RESULTS_DIR, "VIF Metrics")

TRAIN_DATASETS_DIR = os.path.join(DATA_DIR, "Train Datasets")
MODEL_METRICS_DIR = os.path.join(RESULTS_DIR, "Model Metrics")

OPTIMIZATION_MODELS_DIR = os.path.join(DATA_DIR, "Optimization Models")
OPTIMIZATION_RESULTS_DIR = os.path.join(RESULTS_DIR, "Optimization Results")


### Files ###
RAW_CSV_FILE = os.path.join(DATA_DIR, "start_data.csv")
PROCESSED_CSV_FILE = os.path.join(DATA_DIR, "preprocessed_data.csv")


def make_directories():
    """
    Creates directories if they do not exist
    """
    for d in [RAW_DATA_DIR, 
              DATA_DIR, 
              RESULTS_DIR, 
              LOGS_DIR,
              FEATURE_ENG_DIR,
              ENGINEERED_CSVS_DIR,
              MICE_IMPUTED_DATASETS_DIR,
              MICE_METRICS_DIR,
              VIF_IMPUTED_DATASETS_DIR,
              VIF_METRICS_DIR,
              TRAIN_DATASETS_DIR,
              MODEL_METRICS_DIR,
              OPTIMIZATION_MODELS_DIR,
              OPTIMIZATION_RESULTS_DIR]:
        os.makedirs(d, exist_ok=True)


if __name__ == "__main__":
    # make directories if they do not exist
    make_directories()
