from ml_tools.IO_tools import load_json
from ml_tools.utilities import load_dataframe, save_dataframe_filename

from helpers import balance_and_update_dataframe
from paths import PM


def main():
    # Load bounds
    bounds = load_json(PM.optimization_engineering / "optimization_bounds.json")
    
    # Load optimization results
    df, _ = load_dataframe(PM.optimization_results / "Pareto_Solutions.csv")
    
    # Balance and update DataFrame
    balanced_df = balance_and_update_dataframe(df, bounds)
    
    # Save the updated DataFrame
    save_dataframe_filename(df=balanced_df, save_dir=PM.optimization_results, filename="balanced_NonDominatedSolutions.csv")
    

if __name__ == "__main__":
    main()
