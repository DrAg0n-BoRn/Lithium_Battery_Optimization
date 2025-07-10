from ml_tools.VIF_factor import compute_vif_multi
from paths import MICE_DATASETS_DIR, VIF_DATASETS_DIR, VIF_METRICS_DIR, SERIALIZED_OBJECTS_DIR
from helpers.constants import TARGETS
from ml_tools.utilities import yield_dataframes_from_dir, serialize_object


def main():
    compute_vif_multi(input_directory=MICE_DATASETS_DIR,
                    output_plot_directory=VIF_METRICS_DIR,
                    output_dataset_directory=VIF_DATASETS_DIR,
                    ignore_columns=TARGETS)


def save_info():
    # Remaining columns after VIF drop
    for df, df_name in yield_dataframes_from_dir(VIF_DATASETS_DIR):
        feature_columns = [col_name for col_name in df.columns if col_name not in TARGETS]
        serialize_object(obj=feature_columns, save_dir=SERIALIZED_OBJECTS_DIR, filename="FEAT_COLS_" + df_name, raise_on_error=True)
   
    
if __name__ == "__main__":
    main()
    save_info()
