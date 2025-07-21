RAW_COLUMNS = [
    "coating material",
    "dopant element", 
    "element composition",
    "molar ratio",
    "crystal space group",
    "primary particle size",
    "secondary particle size",
    "precursor type",
    "precursor preparation method", 
    "precursor preparation conditions",
    "annealing temperature",
    "annealing time", 
    "single crystal or polycrystalline",
    "voltage range",
    "electrolyte system",
    "capacity",
    "cycles", 
    "capacity retention",
    "first Coulombic efficiency",
    "anode material"
]

TARGETS = [
    "capacity(mAh/g)", 
    "capacity_retention(%)", 
    "first_coulombic_efficiency(%)"
]

# Range values set by the experts
CONT_FEATURES_VALUE_RANGE = {
    "particle_size_primary(um)": (0.1, 40.0),
    "particle_size_secondary(um)": (0.1, 40.0),
    "annealing_temperature_1(K)": (600.0, 1300.0),
    "annealing_temperature_2(K)": (600.0, 1300.0),
    "annealing_time_1(hour)": (2.0, 24.0),
    "annealing_time_2(hour)": (2.0, 24.0),
    "average_voltage(V)": (0.5, 5.0),
    "electrolyte_molarity": (0.1, 10.0),
    "cycles": (5, 3500)
}

TARGETS_VALUE_RANGE = {
    TARGETS[0]: (0.0, 350.0),
    TARGETS[1]: (0.0, 100.0),
    TARGETS[2]: (0.0, 100.0)
}