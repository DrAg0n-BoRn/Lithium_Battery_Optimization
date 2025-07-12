import polars as pl
from ml_tools.utilities import normalize_mixed_list
from helpers.constants import TARGETS
from ml_tools.ETL_engineering import (TransformationRecipe,
                                      BinaryTransformer,
                                      MultiBinaryDummifier,
                                      KeywordDummifier,
                                      NumberExtractor
                                      )


### Define recipe ###
TRANSFORMATION_RECIPE = TransformationRecipe()


### coating material
# Binary: present (1) or absent (0)
coating_material_transformer = BinaryTransformer(
    false_keywords = ['无包覆', '/', '-',]
)

TRANSFORMATION_RECIPE.add(
    input_col_name = "coating material",
    output_col_names = "has_coating_material",
    transform = coating_material_transformer
)


### dopant element
# Multi-binary encoding of dopant elements
_dopant_elements = [
        'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
        'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar',
        'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni',
        'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
        'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd',
        'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe',
        'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd',
        'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu',
        'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl',
        'Pb', 'Bi', 'Po', 'At', 'Rn',
        'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm',
        'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr',
        'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn',
        'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og'
    ]

_dopant_group_names = [f"dopant_{element}" for element in _dopant_elements]

dopant_element_transformer = MultiBinaryDummifier(
    keywords= _dopant_elements,
    case_insensitive=False
)

TRANSFORMATION_RECIPE.add(
    input_col_name = "dopant element",
    output_col_names=_dopant_group_names,
    transform=dopant_element_transformer
)


### crystal space group
# One-hot encoding
_crystal_space_groups = [
    "R-3m", 
    "C2/m", 
    "Fd-3m",
    "R-3m+C2/m-mix", 
    "R-3m+Fd-3m-mix", 
    "R-3m+C2/m+Fd-3m-mix",
    "hexagonal", 
    "orthorhombic", 
    "cubic",
    "monoclinic", 
    "triclinic"
]

def crystal_space_group_transformer(column: pl.Series) -> pl.DataFrame:
    """
    One-hot encoding of crystal space groups
    """
    groups = _crystal_space_groups
    
    groups_dict = {group : list() for group in groups}
    
    def _assign_value(winner: str):
        for _group in groups:
            if _group == winner:
                groups_dict[_group].append(1)
            else:
                groups_dict[_group].append(0)
    
    for string in column:
        if string is None:
            _assign_value("")
        elif "R" in string and "C2" in string and "Fd" in string:
            _assign_value(groups[5])
        elif "R" in string and "Fd" in string:
            _assign_value(groups[4])
        elif "R" in string and "C2" in string:
            _assign_value(groups[3])
        elif "Fd" in string:
            _assign_value(groups[2])
        elif "C2" in string:
            _assign_value(groups[1])
        elif "R" in string:
            _assign_value(groups[0])
        elif "hexagonal" in string.lower() or "P6" in string or "P3" in string:
            _assign_value(groups[6])
        elif "orthorhombic" in string.lower() or "Pn" in string:
            _assign_value(groups[7])
        elif "cubic" in string.lower():
            _assign_value(groups[8])
        elif "monoclinic" in string.lower():
            _assign_value(groups[9])
        elif "triclinic" in string.lower():
            _assign_value(groups[10])
        else:
            _assign_value("")
    
    # make dataframe
    groups_df = pl.DataFrame(groups_dict)
    
    return groups_df

TRANSFORMATION_RECIPE.add(
    input_col_name="crystal space group",
    output_col_names=[f"crystal_{space_group}" for space_group in _crystal_space_groups],
    transform=crystal_space_group_transformer
)


### Primary particle size - Secondary particle size
# extract size in 'um'
def particle_size_transformer(column: pl.Series) -> pl.Series:
    """
    Parse particle size from the column in um, μm
    
    Transform particle size from nm to um
    """
    # Extract particle size from the column
    size_col_um = column.str.extract(r'(?i)(\d+\.?\d*)\s?[μu]m').cast(pl.Float64, strict=False).alias('size um')
    size_col_nm = column.str.extract(r'(?i)(\d+\.?\d*)\s?nm').cast(pl.Float64, strict=False).alias('size nm')
    
    # Transform nm to um
    size_col_nm = size_col_nm / 1000.0
    
    # Merge the two columns
    size_col = (pl.when(size_col_um.is_not_null()).then(size_col_um).otherwise(size_col_nm).alias('particle_size(um)'))
    
    #Evaluate expression
    size = pl.select(size_col).to_series()
    
    return size

TRANSFORMATION_RECIPE.add(
    input_col_name="primary particle size",
    output_col_names="particle_size_primary(um)",
    transform=particle_size_transformer
)

TRANSFORMATION_RECIPE.add(
    input_col_name="secondary particle size",
    output_col_names="particle_size_secondary(um)",
    transform=particle_size_transformer
)


### Precursor type
# One-hot encoding with 2 categories:
precursor_type_transformer = KeywordDummifier(
    group_names = ["precursor_hydroxide", "precursor_carbonate"],
    group_keywords = [
        ["氢氧化物", "hydroxide"],
        ["碳酸盐", "carbonate"]
    ],
    case_insensitive=True
)

TRANSFORMATION_RECIPE.add(
    input_col_name="precursor type",
    output_col_names=precursor_type_transformer.group_names,
    transform=precursor_type_transformer
)


### Precursor preparation method
# One-hot encoding with 5 categories: solid state, sol-gel, co-precipitation, hydrothermal, mechanical
precursor_preparation_method_transformer = KeywordDummifier(
    group_names=[
        "precursor_is_solid_state",
        "precursor_is_sol-gel",
        "precursor_is_co-precipitation",
        "precursor_is_hydrothermal",
        "precursor_is_mechanical"
    ],
    group_keywords=[
        ["固相", "solid"],
        ["溶胶", "sol", "gel"],
        ["共沉淀", "co-", "precipitation"],
        ["水热", "hydrothermal"],
        ["机械", "mechanical"]
    ],
    case_insensitive=True
)

TRANSFORMATION_RECIPE.add(
    input_col_name="precursor preparation method",
    output_col_names=precursor_preparation_method_transformer.group_names,
    transform=precursor_preparation_method_transformer
)


### Precursor preparation conditions
# Parse pH and temperature, convert temperature to Kelvin
def precursor_preparation_conditions_transformer(column: pl.Series) -> pl.DataFrame:
    """
    Parse pH and temperature from the column -> 2 columns
    
    Transform temperature from Celsius to Kelvin
    """
    # Extract pH from the column
    ph_col = column.str.extract(r'(?i)pH\D{0,3}(\d+\.?\d*)').cast(pl.Float64, strict=False).alias('precursor_pH')
    # Extract temperature from the column
    temp_col_c = column.str.extract(r'(\d+\.?\d*)\s?°?[Cc℃]').cast(pl.Float64, strict=False).alias('precursor_temperature')
    # Convert temperature from Celsius to Kelvin
    temp_col = temp_col_c + 273.15
    
    # Combine the two columns into a dataframe
    df_combined = pl.concat([ph_col.to_frame(), temp_col.to_frame()], how='horizontal')
    
    return df_combined

TRANSFORMATION_RECIPE.add(
    input_col_name="precursor preparation conditions",
    output_col_names=["precursor_pH", "precursor_temperature(K)"],
    transform=precursor_preparation_conditions_transformer
)


### Annealing temperature
# Parse up to 3 temperatures, convert to Kelvin
_annealing_temp_column_names = [
    "annealing_temperature_1(K)",
    "annealing_temperature_2(K)",
    "annealing_temperature_3(K)"
]

def annealing_temperature_transformer(column: pl.Series) -> pl.DataFrame:
    """
    Parse up to 3 temperatures in 3 columns
    
    Transform temperature from Celsius to Kelvin
    
    Avoid false matches with "hour" values in the column
    """
    # Set column names
    column_name_1 = _annealing_temp_column_names[0]
    column_name_2 = _annealing_temp_column_names[1]
    column_name_3 = _annealing_temp_column_names[2]
    
    # Extract all numbers (including possible time-related)
    all_numbers = column.str.extract_all(r'(?i)(\d+\.?\d*)').to_list()

    # Extract time-related numbers (with h or 小时)
    time_related = column.str.extract_all(r'(?i)(\d+\.?\d*)\s*(?:h|小时)').to_list()

    # Filter out time-related numbers and convert to Kelvin
    filtered_numbers = []
    for nums, times in zip(all_numbers, time_related):
        nums = nums or []
        times = times or []
        temps = [float(x) + 273.15 for x in nums if x not in times]
        filtered_numbers.append(temps)
        
    data = {
        column_name_1: [],
        column_name_2: [],
        column_name_3: [],
    }

    for temp_list in filtered_numbers:
        # Pad with None for missing values
        padded = temp_list[:3] + [None] * (3 - len(temp_list))
        data[column_name_1].append(padded[0])
        data[column_name_2].append(padded[1])
        data[column_name_3].append(padded[2])

    return pl.DataFrame(data)

TRANSFORMATION_RECIPE.add(
    input_col_name="annealing temperature",
    output_col_names=_annealing_temp_column_names,
    transform=annealing_temperature_transformer
)


### Annealing time
# Parse up to 3 times expressed in hours
_annealing_time_column_names = [
    "annealing_time_1(hour)",
    "annealing_time_2(hour)",
    "annealing_time_3(hour)"
]

def annealing_time_transformer(column: pl.Series) -> pl.DataFrame:
    """
    Parse up to 3 times expressed in hours in 3 columns
    
    Avoid capturing time in other units
    """
    # Set column names
    column_name_1 = _annealing_time_column_names[0]
    column_name_2 = _annealing_time_column_names[1]
    column_name_3 = _annealing_time_column_names[2]
    
    # Extract all numbers
    all_numbers = column.str.extract_all(r'(?i)(\d+\.?\d*)').to_list()

    # Extract numbers followed by m (minutes), 分 (minutes), °C (degrees Celsius)
    excluded_units = column.str.extract_all(r'(?i)(\d+\.?\d*)\s*(?:m|分|°?C)').to_list()

    # Filter out numbers associated with excluded units
    filtered_times = []
    for nums, excludes in zip(all_numbers, excluded_units):
        nums = nums or []
        excludes = excludes or []
        times = [float(x) for x in nums if x not in excludes]
        filtered_times.append(times)

    data = {
        column_name_1: [],
        column_name_2: [],
        column_name_3: [],
    }

    for time_list in filtered_times:
        # Pad with None instead of -1.0 for missing values
        padded = time_list[:3] + [None] * (3 - len(time_list))
        data[column_name_1].append(padded[0])
        data[column_name_2].append(padded[1])
        data[column_name_3].append(padded[2])

    return pl.DataFrame(data)

TRANSFORMATION_RECIPE.add(
    input_col_name="annealing time",
    output_col_names=_annealing_time_column_names,
    transform=annealing_time_transformer
)    


### Crystal
# Binary: single crystal (0) or polycrystalline (1)
def single_poly_crystal_transformer(column: pl.Series) -> pl.Series:
    """
    Binary: single crystal (0) or polycrystalline (1)
    """
    poly_expr = (
    pl.when(column.str.contains(r'单|(?i)single')).then(0)
    .when(column.str.contains(r'多|(?i)poly')).then(1)
    .otherwise(None)
    .alias('polycrystalline')
    )
    
    # evaluate expression
    poly = pl.select(poly_expr).to_series()
    return poly

TRANSFORMATION_RECIPE.add(
    input_col_name="single crystal or polycrystalline",
    output_col_names="is_polycrystalline",
    transform=single_poly_crystal_transformer
)


### Voltage range
# Parse average voltage range
def voltage_range_transformer(column: pl.Series) -> pl.Series:
    """
    Parse voltage range from the column
    """
    # Extract minimum voltage
    voltage_min = column.str.extract(r'(\d+\.?\d*)\D').cast(pl.Float64, strict=False)
    
    # Extract maximum voltage
    voltage_max = column.str.extract(r'\d+\.?\d*\D+(\d+\.?\d*)').cast(pl.Float64, strict=False)
    
    # get average voltage
    voltage_avg = ((voltage_min + voltage_max) / 2).fill_null(voltage_min).fill_null(voltage_max).alias("average_voltage(V)")
    
    return voltage_avg

TRANSFORMATION_RECIPE.add(
    input_col_name="voltage range",
    output_col_names="average_voltage(V)",
    transform=voltage_range_transformer
)


### Electrolyte system
# Step 1: electrolyte molarity number
electrolyte_molarity_transformer = NumberExtractor(
    regex_pattern=r'(\d+\.?\d*)\s?M',
    dtype="float",
    round_digits=1
)

TRANSFORMATION_RECIPE.add(
    input_col_name="electrolyte system",
    output_col_names="electrolyte_molarity",
    transform=electrolyte_molarity_transformer
)

# Step 2: Binary 'is_LiPF6'
is_lipf6_transformer = BinaryTransformer(
    true_keywords=["LiPF"],
    case_insensitive=True
)

TRANSFORMATION_RECIPE.add(
    input_col_name="electrolyte system",
    output_col_names="electrolyte_is_LiPF6",
    transform=is_lipf6_transformer
)

# Step 3: Multiple Binary encoding of solvents
solvent_transformer = MultiBinaryDummifier(
    keywords = [
        # "EC",  # Ethylene carbonate
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
        "1,4-dioxane",
        "formamide",
        "sulfolane",
        "acetone",
        "methanol",
        "ethanol",
        "isopropanol",
        "n-butanol",
        "t-butanol",
        "ethyl acetate",
        "methyl acetate",
        "butyl acetate",
        "diethyl ether",
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
)

TRANSFORMATION_RECIPE.add(
    input_col_name="electrolyte system",
    output_col_names=[f"solvent_{solvent.replace(" ", "_")}" for solvent in solvent_transformer.keywords],
    transform=solvent_transformer
)


### Cycles
# Extract number of cycles, integer
cycles_transformer = NumberExtractor(
    regex_pattern=r'(\d+)',
    dtype="int"
)

TRANSFORMATION_RECIPE.add(
    input_col_name="cycles",
    output_col_names="cycles",
    transform=cycles_transformer
)


### Anode material
# One-hot encoding of anode material
anode_material_transformer = KeywordDummifier(
    group_names=[
        "anode_lithium_metal", 
        "anode_graphite"
    ],
    group_keywords=[
        ["Li", "锂"],
        ["石墨", "Graphite", "graphite", "MCMB", "SGC"]
    ],
    case_insensitive=True
)

TRANSFORMATION_RECIPE.add(
    input_col_name="anode material",
    output_col_names=anode_material_transformer.group_names,
    transform=anode_material_transformer
)

### Element composition
# A series of binary columns for elements other than: Li, O
element_composition_transformer = MultiBinaryDummifier(
    keywords = [
        "Na", "K", "Mg", "Ca", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
        "B", "F", "P", "S", "Al", "Si", "Zr", "Nb", "Mo", "W", "Sn", "Sb", "C", "H",
        "Cl", "Br", "I", "Se", "Y", "La", "Ce", "Gd", "Ta"
    ],
    case_insensitive=False
)

TRANSFORMATION_RECIPE.add(
    input_col_name="element composition",
    output_col_names=[f"has_{element}" for element in element_composition_transformer.keywords],
    transform=element_composition_transformer
)


### Molar ratio
# Cannot be parsed in the current state of the data


# NOTE: TARGETS

### Capacity 
# Parse a float number
def capacity_transformer(column: pl.Series) -> pl.Series:
    """
    Target column
    
    Capacity in mAh/g
    """
    # use regex to try and match 'mAh/g'. else fallback to any number found in the string
    column_mAh = column.str.extract(r'(\d+\.?\d*)\s?mAh', 1).cast(pl.Float64, strict=False)
    column_fallback = column.str.extract(r'(\d+\.?\d*)', 1).cast(pl.Float64, strict=False)
    
    # combine the two columns,\. If column_mAh is not null, use it, else use column_fallback
    result_col_exp = (pl.when(column_mAh.is_not_null()).then(column_mAh).otherwise(column_fallback).cast(pl.Float64).alias(TARGETS[0]))
    
    # evaluate expression
    result_col = pl.select(result_col_exp).to_series()
    
    return result_col

TRANSFORMATION_RECIPE.add(
    input_col_name="capacity",
    output_col_names=TARGETS[0],
    transform=capacity_transformer
)


### Capacity Retention
# extract and handle percentage
def percentage_transformer(column: pl.Series) -> pl.Series:
    """
    Parse special percentage

    Handles:
    - Decimal values (e.g. 0.746 → 74.60)
    - Regular percentage values (e.g. 83.0% -> 83.00)
    """
    # parse capacity retention from the column (float)
    column_percentage_raw = column.str.extract(r'(\d+\.?\d*)\s?%?', 1).cast(pl.Float64, strict=False)
    
    # normalize values to percentage
    column_percentage_exp = (
        pl.when(column_percentage_raw <= 1.0).then(column_percentage_raw * 100.0)
        .when(column_percentage_raw.is_null()).then(None)
        .otherwise(column_percentage_raw).round(2).cast(pl.Float64, strict=False)
        .alias("temp_percentage")
    )
    
    # evaluate expression
    column_percentage = pl.select(column_percentage_exp).to_series()
    
    return column_percentage

TRANSFORMATION_RECIPE.add(
    input_col_name="capacity retention",
    output_col_names=TARGETS[1],
    transform=percentage_transformer
)


### First coulombic efficiency
# extract and handle percentage
TRANSFORMATION_RECIPE.add(
    input_col_name="first Coulombic efficiency",
    output_col_names=TARGETS[2],
    transform=percentage_transformer
)


# Special case (Deprecated)
def _parse_special_case(df: pl.DataFrame) -> pl.DataFrame:
    """
    Parse "element composition" and "molar ratio" then one hot encode them and return a dataframe.
    """
    columns_to_fix = ["element composition", "molar ratio"]
    
    df_to_fix = df.select(columns_to_fix)
    # parse element composition
    elements_col = df_to_fix["element composition"].str.extract_all(r'([A-Z][a-z]?)').to_list()
    # parse molar ratio
    molar_ratio_col = df_to_fix["molar ratio"].str.extract_all(r'(\d+\.?\d*)').to_list()
    
    # list of new columns
    one_hot_columns = [
        "Li", "Na", "K", "Mg", "Ca", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
        "B", "O", "F", "P", "S", "Al", "Si", "Zr", "Nb", "Mo", "W", "Sn", "Sb", "C", "H",
        "Cl", "Br", "I", "Se", "Y", "La", "Ce", "Gd", "Ta"
    ]
    
    # create a dictionary of lists to hold the one-hot encoded values
    one_hot_dict = {element: [] for element in one_hot_columns}
    
    # populate dictionary
    for element_list, molar_ratio_list in zip(elements_col, molar_ratio_col):
        # if element_list is None, fill dictionary with 0s
        if element_list is None or len(element_list) == 0:
            for element in one_hot_columns:
                one_hot_dict[element].append(0.0)
            continue
        
        # if molar_ratio_list is None, fill it with as many 0 as the length of element_list
        if molar_ratio_list is None:
            molar_ratio_list = [0.0] * len(element_list)
        
        # Ideally sizes should be the same, but in case they are not we use the length of the element_list 
        # and modify values to the molar_ratio_list as needed
        while len(element_list) < len(molar_ratio_list):
            molar_ratio_list.pop()
        
        while len(element_list) > len(molar_ratio_list):
            molar_ratio_list.append(0.0)
            
        # initialize a dict with zero for all elements for this row
        row_values = {element: 0.0 for element in one_hot_columns}
        
        #### Normalize molar ratios ###
        molar_ratio_list = normalize_mixed_list(data=molar_ratio_list, threshold=2)
        
        # populate the dictionary with values based on the presence of elements
        for element, molar_ratio in zip(element_list, molar_ratio_list):
            if element in one_hot_columns:
                row_values[element] = (molar_ratio)
        # append 1 value to each list of the main dict
        for element in one_hot_columns:
            one_hot_dict[element].append(row_values[element])
    
    # create a new dataframe from the dictionary
    one_hot_df_raw = pl.DataFrame({f"molar_ratio_{k}": pl.Series(k, v, dtype=pl.Float64) for k, v in one_hot_dict.items()})
    # drop columns with all zeros (unused elements)
    col_sums = one_hot_df_raw.sum()
    valid_cols = [col for col in col_sums.columns if col_sums[col][0] > 0]
    one_hot_df = one_hot_df_raw.select(valid_cols)

    return one_hot_df

