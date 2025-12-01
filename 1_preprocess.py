from helpers.function_map import TRANSFORMATION_RECIPE
from paths import PM
from ml_tools.ETL_engineering import DragonProcessor


def process_data() -> None:
    """
    Transform data to numerical values
    """
    data_processor = DragonProcessor(TRANSFORMATION_RECIPE)
    
    data_processor.load_transform_save(input_path=PM.clean_data_file, output_path=PM.processed_data_file)

if __name__ == "__main__":
    process_data()
