import pandas as pd


def balance_and_update_dataframe(df: pd.DataFrame, bounds: dict[str, float]) -> pd.DataFrame:
    """
    Reads a pandas DataFrame and a bounds dictionary, calculates the required Fraction_O
    to ensure electroneutrality based on cationic fractions, and returns
    the modified DataFrame.
    """
    # Define oxidation states (Valence)
    valence_map = {
        'Li': 1,
        'Mg': 2,
        'Al': 3,
        'Ti': 4,
        'Mn': 4, 
        'Co': 3,
        'Ni': 2,
        'Sr': 2,
        'Nb': 5,
        'Mo': 6,
        'Sb': 5,
        'Ta': 5,
        'W': 6
    }
    
    # Identify cation columns dynamically from the JSON keys
    # look for keys starting with 'Fraction_' excluding 'Fraction_O'
    cation_cols = [
        key for key in bounds.keys() 
        if key.startswith('Fraction_') and key != 'Fraction_O'
    ]
    
    # Calculate total positive charge for each row
    # Sum(Fraction_Metal * Valence_Metal)
    total_cation_charge = 0
    for col in cation_cols:
        element_symbol = col.split('_')[1] # Extract 'Li' from 'Fraction_Li'
        if element_symbol in valence_map:
            charge = valence_map[element_symbol]
            total_cation_charge += df[col] * charge
    
    # Calculate required Oxygen fraction to balance charge
    # Charge_O = -2 -> 2 * Fraction_O = Total_Positive_Charge
    df['Fraction_O'] = total_cation_charge / 2.0
    
    # Round to 4 decimal places for consistency
    df['Fraction_O'] = df['Fraction_O'].round(4)
    
    return df
