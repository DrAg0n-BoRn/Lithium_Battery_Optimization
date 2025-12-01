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
_PARTICLE_SIZE_nm = (100, 30000)
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
    'Cycles': (10, 3500)
}
