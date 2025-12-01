from ml_tools.ensemble_learning import RegressionTreeModels, run_ensemble_pipeline
from paths import PM
from helpers.constants import TARGETS


if __name__ == "__main__":
    hyperparameters = {
        "L1_regularization": 1.5,
        "L2_regularization": 1.5,
        "learning_rate": 0.001,
        "n_estimators": 3000,   #xgb - lightgbm
        "max_depth": 8,
        "subsample": 0.8,
        "colsample_bytree": 0.8,    #xgb - lightgbm
        "min_child_weight": 3,  #xgb
        "gamma": 1, #xgb
        "num_leaves": 31,   #lightgbm
        "min_data_in_leaf": 40  #lightgbm
    }

    factory_class = RegressionTreeModels(**hyperparameters)
    
    run_ensemble_pipeline(datasets_dir=PM.train_datasets,
                      save_dir=PM.train_metrics,
                      target_columns=TARGETS,
                      model_object=factory_class)
