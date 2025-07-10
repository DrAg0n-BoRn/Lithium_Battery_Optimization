from ml_tools.MICE_imputation import run_mice_pipeline
from paths import FEATURE_ENG_DATASETS_DIR, MICE_DATASETS_DIR, MICE_METRICS_DIR, SERIALIZED_BINARY_FILE
from helpers.constants import TARGETS
from ml_tools.utilities import deserialize_object


# Set number of iterations
ITERATIONS = 20


def main():
    # Load binary column names
    binary_columns: list[str]
    binary_columns = deserialize_object(filepath=SERIALIZED_BINARY_FILE) # type: ignore
    
    # Run pipeline
    run_mice_pipeline(df_path_or_dir=FEATURE_ENG_DATASETS_DIR,
                  target_columns=TARGETS,
                  save_datasets_dir=MICE_DATASETS_DIR,
                  save_metrics_dir=MICE_METRICS_DIR,
                  binary_columns=binary_columns,
                  iterations=ITERATIONS)


if __name__ == "__main__":
    main()
