from ml_tools.ML_optimization import DragonParetoOptimizer
from ml_tools.ML_inference import DragonInferenceHandler
from ml_tools.ML_models import DragonNodeModel
from ml_tools.ML_configuration import DragonParetoConfig
from ml_tools.ML_utilities import DragonArtifactFinder

from helpers.constants import CONTINUOUS_INTEGER_FEATURES, TARGET_capacity, TARGET_capacity_retention, TARGET_first_coulombic_eff
from paths import PM


# Number of iterations, make sure the optimizer is in "append" mode
ITERATIONS: int = 40


def optimization_config():
    # Define optimization objectives
    objectives = {
        TARGET_capacity: 'max',
        TARGET_capacity_retention: 'max',
        TARGET_first_coulombic_eff: 'max'
    }

    # Optimizer configuration
    PARETO_CONFIG = DragonParetoConfig(
        save_directory=PM.optimization_results,
        target_objectives=objectives, # type: ignore
        continuous_bounds_map=PM.optimization_engineering,
        columns_to_round=CONTINUOUS_INTEGER_FEATURES,
        population_size=500,
        generations=1000,
    )

    # ML Artifacts
    ARTIFACTS = DragonArtifactFinder(directory=PM.optimization_train_artifacts, 
                               load_scaler=True, 
                               load_schema=True,
                               strict=True)
    
    return PARETO_CONFIG, ARTIFACTS


def main():
    # get config
    PARETO_CONFIG, ARTIFACTS = optimization_config()
    
    # Define model architecture
    model = DragonNodeModel.load_architecture(ARTIFACTS.model_architecture_path) # type: ignore

    # Define inference handler
    inference_handler = DragonInferenceHandler(
        model=model,
        state_dict=ARTIFACTS.weights_path, # type: ignore
        device="cuda:0",
        scaler=ARTIFACTS.scaler_path
    )
    
    # LOOP for many iterations
    for i in range(ITERATIONS):
        # Initialize optimizer
        optimizer = DragonParetoOptimizer(inference_handler=inference_handler,
                                            schema=ARTIFACTS.feature_schema, # type: ignore
                                            config=PARETO_CONFIG)

        # Run optimization
        optimizer.run(plots_and_log=(ITERATIONS == 1))

        # Plot 3D results
        if ITERATIONS == 1:
            optimizer.plot_pareto_3d(x_target=TARGET_capacity,
                                    y_target=TARGET_capacity_retention,
                                    z_target=TARGET_first_coulombic_eff)

        # Save solutions to CSV
        optimizer.save_solutions(csv_if_exists="append",
                                save_to_sql=False)


if __name__ == "__main__":
    main()
