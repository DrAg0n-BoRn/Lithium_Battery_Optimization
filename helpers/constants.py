# Targets
TARGET_capacity = "Capacity(mAh/g)"
TARGET_capacity_retention = "Capacity Retention(%)"
TARGET_first_coulombic_eff = "First Coulombic Efficiency(%)"

TARGETS = [
    TARGET_capacity, 
    TARGET_capacity_retention, 
    TARGET_first_coulombic_eff
]

# Ranges
TARGETS_RANGE = {
    TARGET_capacity: (0.0, 400.0),
    TARGET_capacity_retention: (0.0, 190.0),
    TARGET_first_coulombic_eff: (0.0, 190.0)
}

_FRACTION_RANGE = (0.0, 5.0)
_PARTICLE_SIZE_nm = (100, 20000)
_TEMPERATURE_RANGE_K = (300, 1400)
_TIME_RANGE_h = (2, 24)
_VOLTAGE_RANGE = (0.1, 5.0)

CONTINUOUS_FEATURES_RANGE = {
    'Fraction_Li': _FRACTION_RANGE,
    'Fraction_O': _FRACTION_RANGE,
    'Fraction_Mg': _FRACTION_RANGE,
    'Fraction_Al': _FRACTION_RANGE,
    'Fraction_Ti': _FRACTION_RANGE,
    'Fraction_Mn': _FRACTION_RANGE,
    'Fraction_Co': _FRACTION_RANGE,
    'Fraction_Ni': _FRACTION_RANGE,
    'Fraction_Sr': _FRACTION_RANGE,
    'Fraction_Nb': _FRACTION_RANGE,
    'Fraction_Mo': _FRACTION_RANGE,
    'Fraction_Sb': _FRACTION_RANGE,
    'Fraction_Ta': _FRACTION_RANGE,
    'Fraction_W': _FRACTION_RANGE,
    'Particle Size Primary(nm)': _PARTICLE_SIZE_nm,
    'Particle Size Secondary(nm)': _PARTICLE_SIZE_nm,
    'Annealing Temperature 1(K)': _TEMPERATURE_RANGE_K,
    'Annealing Temperature 2(K)': _TEMPERATURE_RANGE_K,
    'Annealing Time 1(h)': _TIME_RANGE_h,
    'Annealing Time 2(h)': _TIME_RANGE_h,
    'Minimum Voltage(V)': _VOLTAGE_RANGE,
    'Maximum Voltage(V)': _VOLTAGE_RANGE,
    'Cycles': (1, 3500)
}

# General optimization
# CONTINUOUS_OPTIMIZATION_RANGE = {
#     'Fraction_Li': (0.1, 2.0),
#     'Fraction_O': (0.0, 5.0),
#     'Fraction_Mg': (0.0, 1.0),
#     'Fraction_Al': (0.0, 1.0),
#     'Fraction_Ti': (0.0, 1.0),
#     'Fraction_Mn': (0.0, 2.0),
#     'Fraction_Co': (0.0, 1.0),
#     'Fraction_Ni': (0.0, 2.0),
#     'Fraction_Sr': (0.0, 0.1),
#     'Fraction_Nb': (0.0, 1.0),
#     'Fraction_Mo': (0.0, 1.0),
#     'Fraction_Sb': (0.0, 0.1),
#     'Fraction_Ta': (0.0, 0.5),
#     'Fraction_W': (0.0, 0.1),
#     'Particle Size Primary(nm)': (100, 5000),
#     'Particle Size Secondary(nm)': (5000, 20000),
#     'Annealing Temperature 1(K)': (725, 925),
#     'Annealing Temperature 2(K)': (925, 1175),
#     'Annealing Time 1(h)': (2, 6),
#     'Annealing Time 2(h)': (10, 24),
#     'Minimum Voltage(V)': (1.0, 3.5),
#     'Maximum Voltage(V)': (3.7, 5.0),
#     'Cycles': (5, 2000)
# }

# Optimization focused to experimental formula: Li1.2Mn0.54Ni0.13Co0.13O2 and related
CONTINUOUS_OPTIMIZATION_RANGE = {
    'Fraction_Li': (1.20, 1.26),
    'Fraction_O': (2, 2),
    'Fraction_Mg': (0.0, 0.0),
    'Fraction_Al': (0.0, 0.0),
    'Fraction_Ti': (0.0, 0.0),
    'Fraction_Mn': (0.54, 0.54),
    'Fraction_Co': (0.12, 0.13),
    'Fraction_Ni': (0.13, 0.13),
    'Fraction_Sr': (0.0, 0.0),
    'Fraction_Nb': (0.0, 0.01),
    'Fraction_Mo': (0.0, 0.0),
    'Fraction_Sb': (0.0, 0.0),
    'Fraction_Ta': (0.0, 0.0),
    'Fraction_W': (0.0, 0.0),
    'Particle Size Primary(nm)': (120, 200),
    'Particle Size Secondary(nm)': (5000, 7000),
    'Annealing Temperature 1(K)': (700, 800),
    'Annealing Temperature 2(K)': (920, 1125),
    'Annealing Time 1(h)': (3, 6),
    'Annealing Time 2(h)': (12, 38),
    'Minimum Voltage(V)': (2.0, 2.1),
    'Maximum Voltage(V)': (4.7, 4.9),
    'Cycles': (5, 20)
}


CONTINUOUS_INTEGER_FEATURES = [
    'Particle Size Primary(nm)',
    'Particle Size Secondary(nm)',
    'Annealing Temperature 1(K)',
    'Annealing Temperature 2(K)',
    'Annealing Time 1(h)',
    'Annealing Time 2(h)',
    'Cycles'
]
