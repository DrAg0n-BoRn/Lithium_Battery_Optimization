import pandas as pd
from ml_tools.schema import FeatureSchema
from ml_tools.utilities import load_dataframe_with_schema, save_dataframe_with_schema
from ml_tools.data_exploration import reconstruct_from_schema

from paths import PM
from helpers.constants import TARGET_capacity, TARGET_capacity_retention, TARGET_first_coulombic_eff


feature_schema = FeatureSchema.from_json(PM.optimization_engineering)

df, _ = load_dataframe_with_schema(df_path=PM.optimization_data_file, schema=feature_schema)


df_reconstructed = reconstruct_from_schema(df=df, schema=feature_schema, targets=[TARGET_capacity, TARGET_capacity_retention, TARGET_first_coulombic_eff])


save_dataframe_with_schema(df=df_reconstructed, schema=feature_schema, full_path=PM.backups / "training_data.csv")
