from ml_tools.path_manager import DragonPathManager

# 1. Initialize the PathManager using this file as the anchor, adding base directories.
PM = DragonPathManager(
    anchor_file=__file__,
    base_directories=["helpers", "clean_data", "data", "results", "backups"]
)

# 2. Define directories and files.
# 2.1 📁 Directories
PM.feature_engineering = PM.data / "Feature Engineering"
PM.feature_engineering_metrics = PM.results / "Feature Engineering Metrics"
PM.mice_datasets = PM.data / "MICE Datasets"
PM.mice_metrics = PM.results / "MICE Metrics"
PM.vif_datasets = PM.data / "VIF Datasets"
PM.vif_metrics = PM.results / "VIF Metrics"
PM.train_datasets = PM.data / "Train Datasets"
PM.train_metrics = PM.results / "Train Metrics"
# Optimization
PM.optimization_engineering = PM.data / "Optimization Engineering"
PM.optimization_train_metrics = PM.results / "Optimization Train Metrics"
PM.optimization_results = PM.results / "Optimization Results"

# 2.2 📁 Subdirectories
PM.feature_engineering_raw = PM.feature_engineering / "Feature Engineering Raw"
PM.feature_engineering_final = PM.feature_engineering / "Feature Engineering Final"
PM.optimization_train_checkpoints = PM.optimization_train_metrics / "checkpoints"
PM.optimization_train_artifacts = PM.optimization_train_metrics / "artifacts"
PM.optimization_train_evaluation = PM.optimization_train_metrics / "evaluation"

# 2.3 📄 Files
PM.clean_data_file = PM.clean_data / "clean_data.csv"
PM.processed_data_file = PM.data / "processed_data.csv"
PM.engineered_raw_file = PM.feature_engineering_raw / "engineered_data_raw.csv"
PM.engineered_final_file = PM.feature_engineering_final / "engineered_data_final.csv"
PM.binary_columns_file = PM.feature_engineering / "BINARY_COLUMNS_list.joblib"
PM.continuous_columns_file = PM.feature_engineering / "CONTINUOUS_COLUMNS_list.joblib"
# Optimization
PM.optimization_data_file = PM.optimization_engineering / "optimization_dataset.csv"

# 3. 🛠️ Make directories and check status
if __name__ == "__main__":
    PM.make_dirs()
    PM.status()
