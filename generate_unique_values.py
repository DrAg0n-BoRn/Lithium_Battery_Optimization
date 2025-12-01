from ml_tools.ETL_cleaning import save_unique_values
from paths import PM

if __name__ == "__main__":
    save_unique_values(csv_path=PM.clean_data_file, 
                       output_dir=PM.clean_data, 
                       keep_column_order=True)
