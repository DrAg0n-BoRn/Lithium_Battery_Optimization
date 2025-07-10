from helpers.function_map import TRANSFORMATION_RECIPE
from paths import CLEANED_CSV_FILE, PROCESSED_CSV_FILE
from ml_tools.ETL_engineering import DataProcessor
from ml_tools.utilities import load_dataframe, save_dataframe


def process_data() -> None:
    """
    Transform data to numerical values
    """
    data_processor = DataProcessor(TRANSFORMATION_RECIPE)
    
    df_cleaned, _ = load_dataframe(df_path=CLEANED_CSV_FILE, kind="polars", all_strings=True)
    
    df_processed = data_processor.transform(df=df_cleaned) # type: ignore
    
    save_dataframe(df=df_processed, save_dir=PROCESSED_CSV_FILE.parent, filename=PROCESSED_CSV_FILE.name)


if __name__ == "__main__":
    process_data()
