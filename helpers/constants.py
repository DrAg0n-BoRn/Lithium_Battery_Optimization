
TARGETS = [
    "capacity(mAh/g)", 
    "capacity_retention(%)", 
    "first_coulombic_efficiency(%)"
]


FEATURES_VALUE_RANGE = {
    "particle_size_primary(um)": (0.0, 40.0),
    "particle_size_secondary(um)": (0.0, 40.0),
    "annealing_temperature_1(K)": (600.0, 1250.0),
    "annealing_temperature_2(K)": (600.0, 1250.0),
    "annealing_time_1(hour)": (0.0, 24.0),
    "annealing_time_2(hour)": (0.0, 24.0),
    "average_voltage(V)": (0.0, 5.0),
    "cycles": (5, 3500)
}


TARGETS_VALUE_RANGE = {
    TARGETS[0]: (0.0, 400.0),
    TARGETS[1]: (0.0, 100.0),
    TARGETS[2]: (0.0, 100.0)
}