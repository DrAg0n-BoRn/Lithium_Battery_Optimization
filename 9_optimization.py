from ml_tools.ML_optimization_pareto import DragonParetoOptimizer
from ml_tools.ML_inference import DragonInferenceHandler
from ml_tools.ML_models_advanced import DragonNodeModel
from ml_tools.ML_configuration import DragonParetoConfig
from ml_tools.ML_utilities import ArtifactFinder

from helpers.constants import CONTINUOUS_INTEGER_FEATURES, TARGET_capacity, TARGET_capacity_retention, TARGET_first_coulombic_eff, CONTINUOUS_OPTIMIZATION_RANGE
from paths import PM


def optimization_config():
    # Define optimization objectives
    _objectives = {
        TARGET_capacity: 'max',
        TARGET_capacity_retention: 'max',
        TARGET_first_coulombic_eff: 'max'
    }

    # Optimizer configuration
    PARETO_CONFIG = DragonParetoConfig(
        save_directory=PM.optimization_results,
        target_objectives=_objectives, # type: ignore
        # continuous_bounds_map=PM.optimization_results,
        continuous_bounds_map=CONTINUOUS_OPTIMIZATION_RANGE,
        columns_to_round=CONTINUOUS_INTEGER_FEATURES,
        population_size=500,
        generations=1000,
    )

    # ML Artifacts
    ARTIFACTS = ArtifactFinder(directory=PM.optimization_train_artifacts, load_scaler=True, load_schema=True)
    
    return PARETO_CONFIG, ARTIFACTS


def main():
    # get config
    PARETO_CONFIG, ARTIFACTS = optimization_config()
    
    # Define model architecture
    model = DragonNodeModel.load(ARTIFACTS.model_architecture_path)

    # Define inference handler
    inference_handler = DragonInferenceHandler(
        model=model,
        state_dict=ARTIFACTS.weights_path,
        device="cuda:0",
        scaler=ARTIFACTS.scaler_path
    )

    # Initialize optimizer
    optimizer = DragonParetoOptimizer(inference_handler=inference_handler,
                                      schema=ARTIFACTS.feature_schema,
                                      config=PARETO_CONFIG)

    # Run optimization
    optimizer.run()

    # Plot 3D results
    optimizer.plot_pareto_3d(x_target=TARGET_capacity,
                            y_target=TARGET_capacity_retention,
                            z_target=TARGET_first_coulombic_eff)

    # Save solutions to CSV
    optimizer.save_solutions(save_to_sql=False)


if __name__ == "__main__":
    main()
