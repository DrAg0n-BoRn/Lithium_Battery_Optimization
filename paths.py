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

MICE_BASE_DIR = os.path.join(RESULTS_DIR, "MICE")
MICE_IMPUTED_DATASETS_DIR = os.path.join(MICE_BASE_DIR, "Imputed Datasets")

MODEL_METRICS_DIR = os.path.join(RESULTS_DIR, "Model Metrics")

OPTIMIZATION_RESULTS_DIR = os.path.join(RESULTS_DIR, "Optimization Results")

### Files ###
RAW_CSV_FILE = os.path.join(DATA_DIR, "start_data.csv")
PROCESSED_CSV_FILE = os.path.join(DATA_DIR, "preprocessed_data.csv")
ENGINEERED_CSV_FILE = os.path.join(DATA_DIR, "engineered_data.csv")


def make_directories():
    """
    Creates directories if they do not exist
    """
    for d in [RAW_DATA_DIR, 
              DATA_DIR, 
              RESULTS_DIR, 
              MICE_BASE_DIR, 
              MICE_IMPUTED_DATASETS_DIR,
              MODEL_METRICS_DIR,
              OPTIMIZATION_RESULTS_DIR]:
        os.makedirs(d, exist_ok=True)


if __name__ == "__main__":
    # make directories if they do not exist
    make_directories()
