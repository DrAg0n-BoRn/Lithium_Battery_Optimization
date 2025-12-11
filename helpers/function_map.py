from helpers.constants import TARGETS
from ml_tools.constants import CHEMICAL_ELEMENT_SYMBOLS
from ml_tools.ETL_engineering import (DragonTransformRecipe,
                                      BinaryTransformer,
                                      MultiBinaryDummifier,
                                      NumberExtractor,
                                      MultiNumberExtractor,
                                      MultiTemperatureExtractor,
                                      AutoDummifier, 
                                      MolecularFormulaTransformer)


### Define recipe ###
TRANSFORMATION_RECIPE = DragonTransformRecipe()

### 1. Molecular Formula
# Multi-Continuous 
TRANSFORMATION_RECIPE.add(
    input_col_name="molecular formula",
    output_col_names="Fraction",
    transform=MolecularFormulaTransformer()
)

### 2. coating material
# One-hot approach
TRANSFORMATION_RECIPE.add(
    input_col_name = "coating material",
    output_col_names = "Coating",
    transform = AutoDummifier()
)

### 3. dopant element
# Multi-binary encoding of dopant elements using \b to avoid substring matching
regex_elements = [fr"\b{element}\b" for element in CHEMICAL_ELEMENT_SYMBOLS]

TRANSFORMATION_RECIPE.add(
    input_col_name = "dopant element",
    output_col_names="Dopant",
    transform=MultiBinaryDummifier(
        keywords=regex_elements,
        case_insensitive=False,
        use_regex=True
    )
)

### 4. crystal space group
# MultiBinary encoding
_space_groups = [
    'C2/c',
    'C2/m',
    'Fd-3m',
    'Fm-3m',
    'I4/mmm',
    'Ia-3',
    'P-3m1',
    'P21/c',
    'P4332',
    'P63/mmc',
    'Pbcn',
    'Pm-3m',
    'Pnma',
    'R-3c',
    'R-3m'
]

TRANSFORMATION_RECIPE.add(
    input_col_name="crystal space group",
    output_col_names="Space",
    transform=MultiBinaryDummifier(
        keywords=_space_groups,
        case_insensitive=False
    )
)

### 5. Primary particle size - 6. Secondary particle size
# extract size in 'nm'
TRANSFORMATION_RECIPE.add(
    input_col_name="primary particle size",
    output_col_names="Particle Size Primary(nm)",
    transform=NumberExtractor()
)

TRANSFORMATION_RECIPE.add(
    input_col_name="secondary particle size",
    output_col_names="Particle Size Secondary(nm)",
    transform=NumberExtractor()
)

### 7. Precursor type
# One-hot encoding
TRANSFORMATION_RECIPE.add(
    input_col_name="precursor type",
    output_col_names="Precursor Type",
    transform=AutoDummifier()
)

### 8. Precursor preparation method
# MultiBinary
_precursor_preparation_methods = [
    'Annealing',
    'Atomic layer deposition',
    'Ball milling',
    'CVD',
    'Calcination',
    'Chemical lithiation',
    'Co-precipitation',
    'Combustion synthesis',
    'Commercial',
    'Deposition',
    'Electrochemical',
    'Electrospinning',
    'Grinding',
    'High-shear dry mixing',
    'Hydrolysis',
    'Hydrothermal',
    'Impregnation',
    'Ion exchange reaction',
    'Mechanical mixing',
    'Microwave-assisted',
    "Modified Hummers",
    'Molten salt synthesis',
    'Na-embedded precursor',
    'Nano',
    'Oxalate precipitation',
    'Pechini',
    'Pickering emulsion',
    'Plasma-assisted',
    'Polymer-assisted chemical solution',
    'Pyrolysis',
    'Sintering',
    'Sol-gel',
    'Solid solution',
    'Solid-state reaction',
    'Solvothermal',
    'Spin coating',
    'Spray drying',
    'Spray pyrolysis',
    'Thermal polymerization',
    'Ultrasound-triggered cation chelation',
    'Wet chemistry',
    'Wet mixing'
]

TRANSFORMATION_RECIPE.add(
    input_col_name="precursor preparation method",
    output_col_names="Precursor Method",
    transform=MultiBinaryDummifier(
        keywords=_precursor_preparation_methods,
        case_insensitive=True
    )
)

### 9. Annealing temperature
# Parse up to 3 temperatures, convert to Kelvin
_annealing_temperature_columns = ["Annealing Temperature 1(K)",
                                  "Annealing Temperature 2(K)",
                                  "Annealing Temperature 3(K)"]

TRANSFORMATION_RECIPE.add(
    input_col_name="annealing temperature",
    output_col_names=_annealing_temperature_columns,
    transform=MultiTemperatureExtractor(
        num_outputs=len(_annealing_temperature_columns),
        convert="K"
    )
)

### 10. Annealing time
# Parse up to 3 times expressed in hours
_annealing_time_columns = ["Annealing Time 1(h)",
                           "Annealing Time 2(h)",
                           "Annealing Time 3(h)"]

TRANSFORMATION_RECIPE.add(
    input_col_name="annealing time",
    output_col_names=_annealing_time_columns,
    transform=MultiNumberExtractor(
        num_outputs=len(_annealing_time_columns),
    )
)

### 11. Crystal
# Binary: single crystal (0) or polycrystalline (1)
TRANSFORMATION_RECIPE.add(
    input_col_name="single crystal or polycrystalline",
    output_col_names="is Polycrystalline",
    transform=BinaryTransformer(
        true_keywords=['Poly'],
    )
)

### 12. Voltage range
# minimum and maximum voltage
_voltage_columns = ["Minimum Voltage(V)",
                    "Maximum Voltage(V)"]

TRANSFORMATION_RECIPE.add(
    input_col_name="voltage range",
    output_col_names=_voltage_columns,
    transform=MultiNumberExtractor(
        num_outputs=len(_voltage_columns)
    )
)
### 13. Electrolyte system
# Step 1: Binary 'is_LiPF6'
TRANSFORMATION_RECIPE.add(
    input_col_name="electrolyte system",
    output_col_names="Electrolyte LiPF6",
    transform=BinaryTransformer(
        true_keywords=["LiPF"],
        case_insensitive=True
    )
)

# Step 2: Multiple Binary encoding of solvents
_solvent_list = [
    "EC",  # Ethylene carbonate
    "DMC", # Dimethyl carbonate
    "EMC", # Ethyl methyl carbonate
    "DEC", # Diethyl carbonate
    "PC",  # Propylene carbonate
    "VC",  # Vinylene carbonate
    "FEC", # Fluoroethylene carbonate
    "ACN", # Acetonitrile
    "THF", # Tetrahydrofuran
    "DME", # Dimethoxyethane
    "DMF", # Dimethylformamide
    "DMSO",# Dimethyl sulfoxide
    "NMP", # N-Methyl-2-pyrrolidone
    "DMAc",# Dimethylacetamide
    "MTBE",# Methyl tert-butyl ether
    "dioxane",
    "formamide",
    "sulfolane",
    "acetone",
    "methanol",
    "ethanol",
    "isopropanol",
    "butanol",
    "ethyl",
    "methyl",
    "butyl",
    "diethyl",
    "chloroform",
    "dichloromethane",
    "toluene",
    "xylene",
    "benzene",
    "cyclohexane",
    "hexane",
    "heptane",
    "water"
]

# use regex word boundaries to avoid substring matching issues
regex_solvents = [fr"\b{solvent}\b" for solvent in _solvent_list]

TRANSFORMATION_RECIPE.add(
    input_col_name="electrolyte system",
    output_col_names="Electrolyte Solvent",
    transform=MultiBinaryDummifier(
        keywords = regex_solvents,
        case_insensitive=True,
        use_regex=True
    )
)

### 15. Cycles
# Extract number of cycles, integer
TRANSFORMATION_RECIPE.add(
    input_col_name="cycles",
    output_col_names="Cycles",
    transform=NumberExtractor(
        regex_pattern=r'(\d+)',
        dtype="int",
        round_digits=None
    )
)

### 18. Anode material
# One-hot encoding of anode material
TRANSFORMATION_RECIPE.add(
    input_col_name="anode material",
    output_col_names="Anode",
    transform=AutoDummifier()
)

# NOTE: TARGETS
### 14. Capacity 
# Parse a float number
TRANSFORMATION_RECIPE.add(
    input_col_name="capacity",
    output_col_names=TARGETS[0],
    transform=NumberExtractor()
)

### 16. Capacity Retention
# extract relative and full percentage
TRANSFORMATION_RECIPE.add(
    input_col_name="capacity retention",
    output_col_names=TARGETS[1],
    transform=NumberExtractor()
)

### 17. First coulombic efficiency
# extract relative and full percentage
TRANSFORMATION_RECIPE.add(
    input_col_name="first Coulombic efficiency",
    output_col_names=TARGETS[2],
    transform=NumberExtractor()
)
