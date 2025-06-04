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

FEATURE_ENG_DIR = os.path.join(DATA_DIR, "Feature Engineering")

MICE_IMPUTED_DATASETS_DIR = os.path.join(DATA_DIR, "MICE Imputed Datasets")
MICE_VIF_IMPUTED_DATASETS_DIR = os.path.join(DATA_DIR, "MICE VIF Imputed Datasets")

MICE_METRICS_DIR = os.path.join(RESULTS_DIR, "MICE")
MODEL_METRICS_DIR = os.path.join(RESULTS_DIR, "Model Metrics")

OPTIMIZATION_RESULTS_DIR = os.path.join(RESULTS_DIR, "Optimization Results")


### Files ###
RAW_CSV_FILE = os.path.join(DATA_DIR, "start_data.csv")
PROCESSED_CSV_FILE = os.path.join(DATA_DIR, "preprocessed_data.csv")
ENGINEERED_CSV_FILE = os.path.join(DATA_DIR, "engineered_data.csv")


### Constants ###
TARGETS = ["capacity(mAh/g)", "capacity_retention(%)", "first_coulombic_efficiency(%)"]



def make_directories():
    """
    Creates directories if they do not exist
    """
    for d in [RAW_DATA_DIR, 
              DATA_DIR, 
              RESULTS_DIR, 
              FEATURE_ENG_DIR,
              MICE_IMPUTED_DATASETS_DIR,
              MICE_VIF_IMPUTED_DATASETS_DIR,
              MICE_METRICS_DIR, 
              MODEL_METRICS_DIR,
              OPTIMIZATION_RESULTS_DIR]:
        os.makedirs(d, exist_ok=True)


if __name__ == "__main__":
    # make directories if they do not exist
    make_directories()
