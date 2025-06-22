from ml_tools.particle_swarm_optimization import run_pso, multiple_objective_functions_from_dir
from ml_tools.utilities import deserialize_object
from paths import OPTIMIZATION_RESULTS_DIR, OPTIMIZATION_MODELS_DIR, DATA_DIR
import os


def main():
    # load value range for continuous features 
    cont_features_value_range: dict[str, tuple] = deserialize_object(os.path.join(DATA_DIR, "CONT_FEATURES_VALUE_RANGE_dict.joblib")) # type: ignore

    # set boundaries
    lower_boundaries = [value[0] for key, value in cont_features_value_range.items()]
    upper_boundaries = [value[1] for key, value in cont_features_value_range.items()]

    # Set number of binary columns
    binary_columns: list = deserialize_object(os.path.join(DATA_DIR, "BINARY_COLUMNS_list.joblib")) # type: ignore
    number_binary_columns = len(binary_columns)

    # Set objective functions
    objective_functions, _objective_functions_names = multiple_objective_functions_from_dir(directory=OPTIMIZATION_MODELS_DIR, 
                                                                                            add_noise=True, 
                                                                                            task="maximization",
                                                                                            binary_features=number_binary_columns)

    # run optimization
    for objective_func in objective_functions:
        run_pso(lower_boundaries=lower_boundaries,
                upper_boundaries=upper_boundaries,
                objective_function=objective_func,
                save_results_dir=OPTIMIZATION_RESULTS_DIR,
                auto_binary_boundaries=True,
                swarm_size=200,
                max_iterations=2,
                post_hoc_analysis=2,
                workers=1)


if __name__ == "__main__":
    main()
