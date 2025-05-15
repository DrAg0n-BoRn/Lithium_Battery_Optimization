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
MICE_BASE_DIR = os.path.join(ROOT_DIR, "MICE")
MICE_IMPUTED_METRICS_DIR = os.path.join(MICE_BASE_DIR, "Distribution Metrics")
IMPUTED_DATASETS_DIR = os.path.join(MICE_BASE_DIR, "Imputed Datasets")

### Files ###
RAW_CSV_PATH = os.path.join(DATA_DIR, "start_data.csv")
PROCESSED_CSV_PATH = os.path.join(DATA_DIR, "processed_data.csv")


# Function to make directories if they do not exist
def make_directories():
    """
    Creates directories if they do not exist
    """
    for d in [RAW_DATA_DIR, DATA_DIR, RESULTS_DIR, MICE_BASE_DIR, MICE_IMPUTED_METRICS_DIR, IMPUTED_DATASETS_DIR]:
        os.makedirs(d, exist_ok=True)


if __name__ == "__main__":
    # make directories if they do not exist
    make_directories()
        
