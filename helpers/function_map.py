import polars as pl


def coating_material(column: pl.Series) -> pl.Series:
    """
    Binary: present (1) or absent (0) coating material.
    """
    # check if the value is '无包覆', or '/', or '-' or empty
    return column.apply(lambda x: 1 if x is not None and str(x).strip() not in ['无包覆', '/', '-', ''] else 0)


#TODO: check unit conflict nm and wt%
def coating_thickness(column: pl.Series) -> pl.Series:
    """
    Coating thickness in nm.
    """
    # use regex to try and match 'nm'. else fallback to any number found in the string
    column_nm = column.str.extract(r'(\d+\.?\d*)\s?nm', 1).cast(pl.Float64)
    column_fallback = column.str.extract(r'(\d+\.?\d*)', 1).cast(pl.Float64)
    
    # combine the two columns, if column_nm is not null, use it, else use column_fallback
    column_combined_expr = pl.when(column_nm.is_not_null()).then(column_nm).otherwise(column_fallback).cast(pl.Float64).alias('coating thickness')
    
    # evaluate expression
    column_combined = pl.select(column_combined_expr).to_series()
    
    return column_combined


def dopant_element(column: pl.Series) -> pl.DataFrame:
    """
    One-hot encoding of dopant elements
    """
    # list of dopant elements
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
    
    pattern_dict = {
        element: rf'(?<![A-Za-z]){element}(?![a-z])' for element in dopant_elements
    }
    
    # create a new dataframe with one-hot encoding
    df_dopant_raw = pl.DataFrame({element: column.str.contains(pattern).cast(pl.Int8) for element, pattern in pattern_dict.items()})   
    
    # Drop columns with all zeros (unused elements)
    df_dopant = df_dopant_raw.select(pl.all().filter(pl.sum() > 0))
    
    return df_dopant


# TODO: Unit mismatch
def dopant_concentration(column: pl.Series) -> pl.Series:
    """
    
    """
    pass


# TODO: Molar ratio / elements



def crystal_space_group(column: pl.Series) -> pl.Series:
    """
    Return the number of groups found: 1 (multiple), or 0 (single)
    """
    crystal_group_expr = (
        pl.when(column.str.strip_chars().is_in(["", None, "N/A", "无", "NA"]))
        .then(None)
        .when(column.str.contains(r"[、,和;]"))
        .then(1)
        .otherwise(0)
        .alias("multiple crystal space group")
    )
    
    # evaluate expression
    crystal_group = pl.select(crystal_group_expr).to_series()
    return crystal_group
    

# TODO: Define categories
def morphology(column: pl.Series) -> pl.DataFrame:
    """
    One-hot encoding of morphology
    """
    pass


# TODO: particle and size


# TODO: Precursor type


# TODO: Precursor preparation method



def precursor_preparation_conditions(column: pl.Series) -> pl.DataFrame:
    """
    Parse pH and temperature from the column -> 2 columns
    
    Transform temperature from Celsius to Kelvin
    """
    # Extract pH from the column
    ph_col = column.str.extract(r'pH\D{0,3}(\d+\.?\d*)').cast(pl.Float64).alias('precursor pH')
    # Extract temperature from the column
    temp_col_c = column.str.extract(r'(\d+\.?\d*)\s?\D?\d*\s?°?\s?C').cast(pl.Float64).alias('precursor temperature')
    # Convert temperature from Celsius to Kelvin
    temp_col = temp_col_c + 273.15
    
    # Combine the two columns into a dataframe
    df_combined = pl.concat([ph_col, temp_col], how='horizontal')
    
    return df_combined


# TODO: Annealing temperature


# TODO: Time


def single_poly_crystal(column: pl.Series) -> pl.Series:
    """
    Binary: single crystal (0) or polycrystalline (1)
    """
    poly_expr = (
    pl.when(column.str.contains(r'单|Single|single')).then(0)
    .when(column.str.contains(r'多|Poly|poly')).then(1)
    .otherwise(None)
    .alias('polycrystalline')
    )
    
    # evaluate expression
    poly = pl.select(poly_expr).to_series()
    return poly


def voltage_range(column: pl.Series) -> pl.DataFrame:
    """
    Parse voltage range from the column -> 2 columns
    """
    # Extract minimum voltage
    voltage_min = column.str.extract(r'(\d+\.?\d*)\D').cast(pl.Float64).alias('minimum voltage')
    
    # Extract maximum voltage
    voltage_max = column.str.extract(r'\d+\.?\d*\D+(\d+\.?\d*)').cast(pl.Float64).alias('maximum voltage')
    
    # Combine the two columns into a dataframe
    df_combined = pl.concat([voltage_min, voltage_max], how='horizontal')
    
    return df_combined


def electrolyte_system(column: pl.Series) -> pl.DataFrame:
    """
    One-hot encoding of electrolyte system
    """
    # parse electrolyte molarity
    mol = column.str.extract(r'(\d+\.?\d*)\s?M').cast(pl.Float64).alias('electrolyte molarity')
    
    # parse electrolyte (Binary: if LiPF6, 1, else 0)
    electrolyte_expr = (pl.when(column.str.contains(r'LiPF6?')).then(1).otherwise(0).alias('electrolyte LiPF6'))
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
        solvent: rf'(?<![A-Za-z]){solvent}(?![A-Za-z])' for solvent in solvents
    }
    
    # create a new dataframe with one-hot encoding
    df_solvents_raw = pl.DataFrame({solvent: column.str.contains(pattern).cast(pl.Int8) for solvent, pattern in pattern_dict.items()})
    
    # drop columns with all zeros (unused solvents)
    df_solvents = df_solvents_raw.select(pl.all().filter(pl.sum() > 0))
    
    # merge the series and the dataframe
    df_combined = pl.concat([mol, electrolyte, df_solvents], how='horizontal')
    
    return df_combined


# TODO: Current density



def cycles(column: pl.Series) -> pl.Series:
    """ 
    Number of cycles
    """
    # parse cycles from the column (integer)
    column_cycles = column.str.extract(r'(\d+)', 1).cast(pl.Int64)


def anode_material(column: pl.Series) -> pl.DataFrame:
    '''
    One-hot encoding of anode material matched with full cell
    '''
    lithium_metal = ["Li", "锂"]
    graphite = ["石墨", "Graphite", "graphite", "MCMB", "SGC"]
    
    # make 2 new columns: lithium-metal and graphite
    lithium_metal_col = (pl.when(column.str.contains('|'.join(lithium_metal))).then(1).otherwise(0).alias('anode lithium metal'))
    graphite_col = (pl.when(column.str.contains('|'.join(graphite))).then(1).otherwise(0).alias('anode graphite'))
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
    column_mAh = column.str.extract(r'(\d+\.?\d*)\s?mAh', 1).cast(pl.Float64)
    column_fallback = column.str.extract(r'(\d+\.?\d*)', 1).cast(pl.Float64)
    
    # combine the two columns,\. If column_mAh is not null, use it, else use column_fallback
    result_col_exp = (pl.when(column_mAh.is_not_null()).then(column_mAh).otherwise(column_fallback).cast(pl.Float64).alias('capacity'))
    
    # evaluate expression
    result_col = pl.select(result_col_exp).to_series()
    
    return result_col


def parse_percentage(column: pl.Series) -> pl.Series:
    """
    Capacity retention
    First Coulombic Efficiency (FCE)
       
    Handles:
    - Overscaled values (e.g. 9065 → 90.65)
    - Decimal values (e.g. 0.746 → 74.60)
    - Regular percentage values (e.g. 83.0% -> 83.00)
    """
    # parse capacity retention from the column (float)
    column_percentage_raw = column.str.extract(r'(\d+\.?\d*)\s?%?', 1).cast(pl.Float64)
    
    # normalize values to percentage
    column_percentage_exp = (
        pl.when((column_percentage_raw > 100.0) & (column_percentage_raw < 10000.0)).then(column_percentage_raw / 100.0)
        .when(column_percentage_raw <= 1.0).then(column_percentage_raw * 100.0)
        .otherwise(column_percentage_raw).round(2).cast(pl.Float64)
        .alias('capacity retention')
    )
    
    # evaluate expression
    column_percentage = pl.select(column_percentage_exp).to_series()
    
    return column_percentage


### Distribute rules to the columns
function_map = {
    'coating material': coating_material,
    'coating thickness': coating_thickness,
    'dopant element': dopant_element,
    'dopant concentration': dopant_concentration,
    'molar ratio': None,
    'crystal space group': crystal_space_group,
    'morphology': morphology,
    'primary particle': None,
    'size/diameter 1': None,
    'secondary particle': None,
    'size/diameter 2': None,
    'precursor type': None,
    'precursor preparation method': None,
    'precursor preparation conditions': precursor_preparation_conditions,
    'annealing temperature': None,
    'time': None,
    'single poly crystal': single_poly_crystal,
    'voltage range': voltage_range,
    'electrolyte system': electrolyte_system,
    'current density': None,
    'cycles': cycles,
    'anode material': anode_material,
    
    'capacity': capacity,
    'capacity retention': parse_percentage,
    'first Coulombic efficiency': parse_percentage,
}

