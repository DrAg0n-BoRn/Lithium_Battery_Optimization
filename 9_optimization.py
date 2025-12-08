from ml_tools.ML_optimization_pareto import DragonParetoOptimizer
from ml_tools.ML_inference import DragonInferenceHandler
from ml_tools.schema import FeatureSchema
from ml_tools.ML_models_advanced import DragonNodeModel
from ml_tools.ML_utilities import ArtifactFinder

from helpers.constants import CONTINUOUS_OPTIMIZATION_RANGE, CONTINUOUS_INTEGER_FEATURES, TARGET_capacity, TARGET_capacity_retention, TARGET_first_coulombic_eff
from paths import PM


# reconstruct feature schema
feature_schema = FeatureSchema.from_json(directory=PM.optimization_engineering)

# Load artifacts
artifacts = ArtifactFinder(directory=PM.optimization_train_artifacts, load_scaler=True)

# Define model architecture
model = DragonNodeModel.load(artifacts.model_architecture_path)

# Define inference handler
inference_handler = DragonInferenceHandler(
    model=model,
    state_dict=artifacts.weights_path,
    device="cuda:0",
    scaler=artifacts.scaler_path
)

# Define optimization objectives
objectives = {
    TARGET_capacity: 'max',
    TARGET_capacity_retention: 'max',
    TARGET_first_coulombic_eff: 'max'
}

# Initialize optimizer
optimizer = DragonParetoOptimizer(
    inference_handler=inference_handler,
    schema=feature_schema,
    target_objectives=objectives, # type: ignore
    continuous_bounds_map=CONTINUOUS_OPTIMIZATION_RANGE,
    population_size=500,
)

# Run optimization
optimizer.run(
    generations=1000,
    save_dir=PM.optimization_results
)

# Plot 3D results
optimizer.plot_pareto_3d(x_target=TARGET_capacity,
                         y_target=TARGET_capacity_retention,
                         z_target=TARGET_first_coulombic_eff)

# Save solutions to CSV
optimizer.save_solutions(columns_to_round=CONTINUOUS_INTEGER_FEATURES, save_to_sql=False)
