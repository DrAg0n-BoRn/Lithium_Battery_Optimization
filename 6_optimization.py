from ml_tools.PSO_optimization import run_pso, multiple_objective_functions_from_dir, plot_optimal_feature_distributions
from ml_tools.utilities import deserialize_object
from paths import OPTIMIZATION_RESULTS_DIR, OPTIMIZATION_MODELS_DIR, SERIALIZED_CONTINUOUS_FILE, SERIALIZED_BINARY_FILE


def main():
    # load value range for continuous features 
    cont_features_value_range: dict[str, tuple[float,float]] = deserialize_object(SERIALIZED_CONTINUOUS_FILE) # type: ignore

    # set boundaries
    lower_boundaries = [value[0] for key, value in cont_features_value_range.items()]
    upper_boundaries = [value[1] for key, value in cont_features_value_range.items()]

    # Set number of binary columns
    binary_columns: list[str] = deserialize_object(SERIALIZED_BINARY_FILE) # type: ignore
    number_binary_columns = len(binary_columns)

    # Set objective functions
    objective_functions, _filenames = multiple_objective_functions_from_dir(directory=OPTIMIZATION_MODELS_DIR, 
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
                swarm_size=500,
                max_iterations=6000,
                post_hoc_analysis=20)


def make_plots():
    plot_optimal_feature_distributions(results_dir=OPTIMIZATION_RESULTS_DIR,
                                       save_dir=OPTIMIZATION_RESULTS_DIR)


if __name__ == "__main__":
    main()
    make_plots()
