from ml_tools.MICE_imputation import run_mice_pipeline
from paths import PM
from helpers.constants import TARGETS
from ml_tools.serde import deserialize_object


# Set number of iterations
ITERATIONS = 25


def main():
    binary_columns = deserialize_object(filepath=PM.binary_columns_file, expected_type=list)

    # Run pipeline
    run_mice_pipeline(df_path_or_dir=PM.engineered_final_file,
                  target_columns=[],
                  save_datasets_dir=PM.mice_datasets,
                  save_metrics_dir=PM.mice_metrics,
                  binary_columns=binary_columns,
                  iterations=ITERATIONS)


if __name__ == "__main__":
    main()
