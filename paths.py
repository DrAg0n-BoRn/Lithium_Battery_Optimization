from pathlib import Path
import sys


# set root directory
ROOT_DIR = Path(__file__).resolve().parent
# Add the root directory to the system path
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))


### Directories ###
RAW_DATA_DIR = ROOT_DIR / "raw_data"
DATA_DIR = ROOT_DIR / "data"
RESULTS_DIR = ROOT_DIR / "results"
LOGS_DIR = ROOT_DIR / "Logs"

FEATURE_ENG_METRICS_DIR = DATA_DIR / "Feature Engineering"
FEATURE_ENG_DATASETS_DIR = DATA_DIR / "Feature Eng Datasets"

MICE_DATASETS_DIR = DATA_DIR / "MICE Datasets"
MICE_METRICS_DIR = RESULTS_DIR / "MICE Metrics"

VIF_DATASETS_DIR = DATA_DIR / "VIF Datasets"
VIF_METRICS_DIR = RESULTS_DIR / "VIF Metrics"

TRAIN_DATASETS_DIR = DATA_DIR / "Train Datasets"
ENSEMBLE_RESULTS_DIR = RESULTS_DIR / "Model Metrics"

OPTIMIZATION_MODELS_DIR = DATA_DIR / "Optimization Models"
OPTIMIZATION_RESULTS_DIR = RESULTS_DIR / "Optimization Results"


### Files ###
RAW_CSV_FILE = RAW_DATA_DIR / "raw_data.csv"
CLEANED_CSV_FILE = DATA_DIR / "cleaned_data.csv"


def make_directories():
    """
    Creates directories if they do not exist
    """
    for dir in [ DATA_DIR, 
              RESULTS_DIR, 
              LOGS_DIR,
              FEATURE_ENG_METRICS_DIR,
              FEATURE_ENG_DATASETS_DIR,
              MICE_DATASETS_DIR,
              MICE_METRICS_DIR,
              VIF_DATASETS_DIR,
              VIF_METRICS_DIR,
              TRAIN_DATASETS_DIR,
              ENSEMBLE_RESULTS_DIR,
              OPTIMIZATION_MODELS_DIR,
              OPTIMIZATION_RESULTS_DIR]:
        dir.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    make_directories()
