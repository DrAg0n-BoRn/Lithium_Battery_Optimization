import polars as pl
import re


def coating_material(column: pl.Series) -> pl.Series:
    """
    Binary: present (1) or absent (0) coating material.
    """
    return column.map_elements(
        function=lambda x: 1 if x is not None and str(x).strip() not in ['无包覆', '/', '-', ''] else 0,
        return_dtype=pl.Int8
    ).alias("coating_material")


def dopant_element(column: pl.Series) -> pl.DataFrame:
    """
    One-hot encoding of dopant elements using Python regex and Polars
    """
    dopant_elements = [
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
    
    # Precompile regex patterns using Python re
    pattern_dict = {
        f"dopant_{element}": re.compile(rf"(?<![A-Za-z]){element}(?![a-z])") for element in dopant_elements
    }

    # Apply to each row in the column (a Polars Series) using Python logic
    def match_row(row_val: str) -> dict:
        row_val = str(row_val) if row_val is not None else ''
        return {
            col_name: int(bool(pattern.search(row_val)))
            for col_name, pattern in pattern_dict.items()
        }

    # Map across all values in the column
    encoded_rows = [match_row(val) for val in column]

    # Convert to Polars DataFrame
    df_dopant_raw = pl.DataFrame(encoded_rows)

    # Extract columns with sum > 0
    col_sums = df_dopant_raw.sum()
    valid_cols = [col for col in col_sums.columns if col_sums[col][0] > 0]
    df_dopant = df_dopant_raw.select(valid_cols)

    return df_dopant



def crystal_space_group(column: pl.Series) -> pl.DataFrame:
    """
    One-hot encoding of crystal space groups
    """
    groups = ["R-3m", 
              "C2/m", 
              "Fd-3m",
              "R-3m+C2/m-mix", 
              "R-3m+Fd-3m-mix", 
              "R-3m+C2/m+Fd-3m-mix",
              "Hexagonal", 
              "Orthorhombic", 
              "Cubic",
              "Monoclinic", 
              "Triclinic"]
    
    groups_dict = {group : list() for group in groups}
    
    def _assign_value(winner: str):
        for _group in groups.copy():
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
    

def primary_particle_size(column: pl.Series) -> pl.Series:
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
    size_col = (pl.when(size_col_um.is_not_null()).then(size_col_um).otherwise(size_col_nm).alias('particle_size_primary(um)'))
    
    #Evaluate expression
    size = pl.select(size_col).to_series()
    
    return size


def secondary_particle_size(column: pl.Series) -> pl.Series:
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
    size_col = (pl.when(size_col_um.is_not_null()).then(size_col_um).otherwise(size_col_nm).alias('particle_size_secondary(um)'))
    
    #Evaluate expression
    size = pl.select(size_col).to_series()
    
    return size
    
    
def precursor_type(column: pl.Series) -> pl.DataFrame:
    """
    One-hot encoding with 3 categories: hydroxide, carbonate, other
    """
    hydroxide_expr = (
        pl.when(column.str.contains(r'氢氧化物|[Hh]ydroxide')).then(1)
        .otherwise(0)
        .alias('precursor_hydroxide')
    )
    carbonate_expr = ( 
        pl.when(column.str.contains(r'碳酸盐|[Cc]arbonate')).then(1)
        .otherwise(0)
        .alias('precursor_carbonate')
    )
    # Otherwise, if it does not contain "氢氧化物|hydroxide" or "碳酸盐|carbonate", then it is "other"
    # REMOVE DUE TO COLLINEARITY
    # other_expr = (
    #     pl.when(column.str.contains(r'氢氧化物|[Hh]ydroxide|碳酸盐|[Cc]arbonate'))
    #     .then(0)
    #     .otherwise(1)
    #     .alias('other precursor')
    # )
    
    # evaluate expressions and create a dataframe
    df_combined = pl.concat([pl.select(hydroxide_expr), pl.select(carbonate_expr)], how='horizontal')
    
    return df_combined
    
    
def precursor_preparation_method(column: pl.Series) -> pl.DataFrame:
    """
    One-hot encoding with 5 categories: solid state, sol-gel, co-precipitation, hydrothermal, mechanical
    """
    solid_state_expr = (
        pl.when(column.str.contains(r'固相|(?i)solid[-\s]?state')).then(1)
        .otherwise(0)
        .alias('precursor_preparation_solid_state')
    )
    sol_gel_expr = (
        pl.when(column.str.contains(r'溶胶|(?i)sol[-\s]?gel')).then(1)
        .otherwise(0)
        .alias('precursor_preparation_sol-gel')
    )
    co_precipitation_expr = (
        pl.when(column.str.contains(r'共沉淀|(?i)co[\s\-]?precipitation')).then(1)
        .otherwise(0)
        .alias('precursor_preparation_co-precipitation')
    )
    hydrothermal_expr = (
        pl.when(column.str.contains(r'水热|(?i)hydrothermal')).then(1)
        .otherwise(0)
        .alias('precursor_preparation_hydrothermal')
    )
    mechanical_expr = (
        pl.when(column.str.contains(r'机械|(?i)mechanical')).then(1)
        .otherwise(0)
        .alias('precursor_preparation_mechanical')
    )
    
    # evaluate expressions and create a dataframe
    df_combined = pl.concat([pl.select(solid_state_expr), pl.select(sol_gel_expr), pl.select(co_precipitation_expr), 
                             pl.select(hydrothermal_expr), pl.select(mechanical_expr)], how='horizontal')
    
    return df_combined


def precursor_preparation_conditions(column: pl.Series) -> pl.DataFrame:
    """
    Parse pH and temperature from the column -> 2 columns
    
    Transform temperature from Celsius to Kelvin
    """
    # Extract pH from the column
    ph_col = column.str.extract(r'(?i)pH\D{0,3}(\d+\.?\d*)').cast(pl.Float64, strict=False).alias('precursor_pH')
    # Extract temperature from the column
    temp_col_c = column.str.extract(r'(\d+\.?\d*)\s?\D?\d*\s?°?\s?[Cc]').cast(pl.Float64, strict=False).alias('precursor_temperature')
    # Convert temperature from Celsius to Kelvin
    temp_col = temp_col_c + 273.15
    
    # Combine the two columns into a dataframe
    df_combined = pl.concat([ph_col.to_frame(), temp_col.to_frame()], how='horizontal')
    
    return df_combined


def annealing_temperature(column: pl.Series) -> pl.DataFrame:
    """
    Parse up to 3 temperatures in 3 columns
    
    Transform temperature from Celsius to Kelvin
    
    Avoid false matches with "hour" values in the column
    """
    # Set column names
    column_name_1 = "annealing_temperature_1(K)"
    column_name_2 = "annealing_temperature_2(K)"
    column_name_3 = "annealing_temperature_3(K)"
    
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


def annealing_time(column: pl.Series) -> pl.DataFrame:
    """
    Parse up to 3 times expressed in hours in 3 columns
    
    Avoid capturing time in other units
    """
    # Set column names
    column_name_1 = "annealing_time_1(hour)"
    column_name_2 = "annealing_time_2(hour)"
    column_name_3 = "annealing_time_3(hour)"
    
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
    

def single_poly_crystal(column: pl.Series) -> pl.Series:
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


def voltage_range(column: pl.Series) -> pl.Series:
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


def electrolyte_system(column: pl.Series) -> pl.DataFrame:
    """
    One-hot encoding of electrolyte system
    """
    # parse electrolyte molarity
    mol = column.str.extract(r'(\d+\.?\d*)\s?M').cast(pl.Float64, strict=False).alias('electrolyte_molarity')
    
    # parse electrolyte (Binary: if LiPF6, 1, else 0)
    electrolyte_expr = (pl.when(column.str.contains(r'LiPF6?')).then(1).otherwise(0).alias('electrolyte_LiPF6'))
    # evaluate expression
    electrolyte = pl.select(electrolyte_expr).to_series()
    
    # parse solvents and one hot encode
    solvents = [
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
    
    pattern_dict = {
        f"solvent_{solvent.strip().replace(" ", "_")}": rf'\b{solvent}\b' for solvent in solvents
    }
    
    # create a new dataframe with one-hot encoding
    df_solvents_raw = pl.DataFrame({solvent: column.str.contains(pattern).cast(pl.Int8) for solvent, pattern in pattern_dict.items()})
    
    # drop columns with all zeros (unused solvents)
    col_sums = df_solvents_raw.sum()
    valid_cols = [col for col in col_sums.columns if col_sums[col][0] > 0]
    df_solvents = df_solvents_raw.select(valid_cols)
    
    # merge the series and the dataframe
    df_combined = pl.concat([mol.to_frame(), electrolyte.to_frame(), df_solvents], how='horizontal')
    
    return df_combined


def cycles(column: pl.Series) -> pl.Series:
    """ 
    Number of cycles
    """
    # parse cycles from the column (integer)
    column_cycles = column.str.extract(r'(\d+)', 1).cast(pl.Int64, strict=False)
    return column_cycles


def anode_material(column: pl.Series) -> pl.DataFrame:
    '''
    One-hot encoding of anode material matched with full cell
    '''
    lithium_metal = ["Li", "锂"]
    graphite = ["石墨", "Graphite", "graphite", "MCMB", "SGC"]
    
    # make 2 new columns: lithium-metal and graphite
    lithium_metal_col = (pl.when(column.str.contains('|'.join(lithium_metal))).then(1).otherwise(0).alias('anode_lithium_metal'))
    graphite_col = (pl.when(column.str.contains('|'.join(graphite))).then(1).otherwise(0).alias('anode_graphite'))
    ## if both are 0, then it is assumed to be other anode materials
    
    # create a dataframe and return it (evaluate expressions)
    df_combined = pl.select([lithium_metal_col, graphite_col])
    
    return df_combined


def capacity(column: pl.Series) -> pl.Series:
    """
    Target column
    
    Capacity in mAh/g
    """
    # use regex to try and match 'mAh/g'. else fallback to any number found in the string
    column_mAh = column.str.extract(r'(\d+\.?\d*)\s?mAh', 1).cast(pl.Float64, strict=False)
    column_fallback = column.str.extract(r'(\d+\.?\d*)', 1).cast(pl.Float64, strict=False)
    
    # combine the two columns,\. If column_mAh is not null, use it, else use column_fallback
    result_col_exp = (pl.when(column_mAh.is_not_null()).then(column_mAh).otherwise(column_fallback).cast(pl.Float64).alias('capacity(mAh/g)'))
    
    # evaluate expression
    result_col = pl.select(result_col_exp).to_series()
    
    return result_col


def capacity_retention(column: pl.Series) -> pl.Series:
    """
    Capacity retention
       
    Handles:
    - Overscaled values (e.g. 9065 → 90.65)
    - Decimal values (e.g. 0.746 → 74.60)
    - Regular percentage values (e.g. 83.0% -> 83.00)
    """
    # parse capacity retention from the column (float)
    column_percentage_raw = column.str.extract(r'(\d+\.?\d*)\s?%?', 1).cast(pl.Float64, strict=False)
    
    # normalize values to percentage
    column_percentage_exp = (
        pl.when((column_percentage_raw > 100.0) & (column_percentage_raw < 10000.0)).then(column_percentage_raw / 100.0)
        .when(column_percentage_raw <= 1.0).then(column_percentage_raw * 100.0)
        .when(column_percentage_raw.is_null()).then(None)
        .otherwise(column_percentage_raw).round(2).cast(pl.Float64, strict=False)
        .alias('capacity_retention(%)')
    )
    
    # evaluate expression
    column_percentage = pl.select(column_percentage_exp).to_series()
    
    return column_percentage


def first_coulombic(column: pl.Series) -> pl.Series:
    """
    First Coulombic Efficiency (FCE)
       
    Handles:
    - Overscaled values (e.g. 9065 → 90.65)
    - Decimal values (e.g. 0.746 → 74.60)
    - Regular percentage values (e.g. 83.0% -> 83.00)
    """
    # parse capacity retention from the column (float)
    column_percentage_raw = column.str.extract(r'(\d+\.?\d*)\s?%?', 1).cast(pl.Float64, strict=False)
    
    # normalize values to percentage
    column_percentage_exp = (
        pl.when((column_percentage_raw > 100.0) & (column_percentage_raw < 10000.0)).then(column_percentage_raw / 100.0)
        .when(column_percentage_raw <= 1.0).then(column_percentage_raw * 100.0)
        .when(column_percentage_raw.is_null()).then(None)
        .otherwise(column_percentage_raw).round(2).cast(pl.Float64, strict=False)
        .alias('first_coulombic_efficiency(%)')
    )
    
    # evaluate expression
    column_percentage = pl.select(column_percentage_exp).to_series()
    
    return column_percentage


def parse_special_case(df: pl.DataFrame) -> pl.DataFrame:
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
        
        # if molar_ratio_list is None, fill it with as many 1s as the length of element_list
        if molar_ratio_list is None:
            molar_ratio_list = [1.0] * len(element_list)
        
        # Ideally sizes should be the same, but in case they are not we use the length of the element_list 
        # and modify values to the molar_ratio_list as needed
        while len(element_list) < len(molar_ratio_list):
            molar_ratio_list.pop()
        
        while len(element_list) > len(molar_ratio_list):
            molar_ratio_list.append(1.0)
            
        # initialize a dict with zero for all elements for this row
        row_values = {element: 0.0 for element in one_hot_columns}
            
        # populate the dictionary with values based on the presence of elements
        for element, molar_ratio in zip(element_list, molar_ratio_list):
            new_molar_value = float(molar_ratio)
            # attempt to fix input value
            if new_molar_value < 0.0010:
                continue
            if element in one_hot_columns:
                row_values[element] = (new_molar_value)
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



### Distribute rules to the columns
function_map = {
    'coating material': coating_material,
    'dopant element': dopant_element,
    'crystal space group': crystal_space_group,
    'primary particle size': primary_particle_size,
    'secondary particle size': secondary_particle_size,
    'precursor type': precursor_type,
    'precursor preparation method': precursor_preparation_method,
    'precursor preparation conditions': precursor_preparation_conditions,
    'annealing temperature': annealing_temperature,
    'annealing time': annealing_time,
    'single crystal or polycrystalline': single_poly_crystal,
    'voltage range': voltage_range,
    'electrolyte system': electrolyte_system,
    'cycles': cycles,
    'anode material': anode_material,
    'element composition': None,    #handle as special case
    'molar ratio': None,    #handle as special case
    
    'capacity': capacity,
    'capacity retention': capacity_retention,
    'first Coulombic efficiency': first_coulombic,
}

