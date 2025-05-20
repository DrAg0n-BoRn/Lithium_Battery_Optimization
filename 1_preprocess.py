from helpers.function_map import function_map, parse_special_case
from paths import RAW_DATA_DIR, RAW_CSV_FILE, PROCESSED_CSV_FILE, make_directories
import polars as pl
import os


def concatenate_raw_data() -> None:
    """
    Concatenates .csv files in the raw data directory and makes a new single .csv
    """
    dfs = []
    filenames = []
    # Loop through all files in the raw data directory
    for file in os.listdir(RAW_DATA_DIR):
        if file.endswith(".csv"):
            # Construct the full file path
            df_path = os.path.join(RAW_DATA_DIR, file)
            # Read the CSV file into a DataFrame, ignoring data types
            df = pl.read_csv(df_path, infer_schema=False)
            # Append the DataFrame to the list
            dfs.append(df)
            filenames.append(file)
    
    # Concatenate all DataFrames in the list into a single DataFrame
    if dfs:
        if len(dfs) > 1:
            # Check if column names and order match
            for i in range(1, len(dfs)):
                if dfs[i].columns != dfs[0].columns:
                    raise ValueError(f"Column names or order do not match in files:\n\t{filenames[0]}\n\t{filenames[i]}.")
            concatenated_df = pl.concat(dfs, how="vertical")
            # Write the concatenated DataFrame to a new CSV file
            concatenated_df.write_csv(RAW_CSV_FILE)
        else:
            # If only one DataFrame, write it to the CSV file
            dfs[0].write_csv(RAW_CSV_FILE)
        print(f"Concatenated {len(dfs)} CSV files of raw data.")
    else:
        raise ValueError(f"No CSV files found in '{RAW_DATA_DIR}'")
    
    
def preprocess_data() -> None:
    """
    Preprocesses the data by applying functions from function_map
    """
    # If the data CSV file does not exist, create concatenate_raw_data 
    if not os.path.exists(RAW_CSV_FILE):
        concatenate_raw_data()
    
    # Read the data CSV file into a DataFrame
    df = pl.read_csv(RAW_CSV_FILE, infer_schema=False)
    
    # Check that column names match to function map
    for feature_name in df.columns:
        if feature_name not in function_map.keys():
            raise ValueError(f"Feature '{feature_name}' not found in function map.")
    
    # Apply the functions to the columns
    results = []
    for feature_name, function in function_map.items():
        if function is not None:
            output = function(df[feature_name])
            # Check if the output is a Series or DataFrame
            if isinstance(output, pl.Series):
                results.append(output)
            elif isinstance(output, pl.DataFrame):
                results.extend(output.get_columns())
            else:
                raise ValueError(f"Function for '{feature_name}' did not return a Series or DataFrame.")
    
    # Special case
    results.extend(parse_special_case(df).get_columns())
    
    if results:
        # Make a new DataFrame from the results
        results_df = pl.DataFrame(results)
        # save the results to a new CSV file
        results_df.write_csv(PROCESSED_CSV_FILE)
        print(f"Preprocessed data saved to '{PROCESSED_CSV_FILE}'")
    else:
        raise ValueError("No results. Check the function map and data.")


if __name__ == "__main__":
    make_directories()
    preprocess_data()
    