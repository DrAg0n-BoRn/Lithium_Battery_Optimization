---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.1
  kernelspec:
    display_name: lithiumbatterydesign
    language: python
    name: python3
---

# Optimization Engineering

```python
from paths import PM
from helpers.constants import TARGETS
from ml_tools.optimization_tools import make_continuous_bounds_template
from ml_tools.utilities import load_dataframe_greedy, merge_dataframes, save_dataframe_with_schema
from ml_tools.data_exploration import info
info()
```

# 1. Load functions

```python
from ml_tools.data_exploration import (reconstruct_one_hot,
                                       reconstruct_binary,
                                       reconstruct_multibinary,
                                       summarize_dataframe,
                                       show_null_columns,
                                       split_features_targets,
                                       encode_categorical_features,
                                       drop_constant_columns,
                                       finalize_feature_schema)
```

## 2. Load dataframe

```python
df_raw = load_dataframe_greedy(directory=PM.mice_datasets)
```

```python
df_raw_no_const = drop_constant_columns(df_raw)
```

```python
summarize_dataframe(df_raw_no_const)
```

## 3. Reconstruct one-hot encoded features and binary features

```python
one_hot_columns = ["Coating", "Precursor Type", "Anode"]

df_reconstructed_I = reconstruct_one_hot(df=df_raw_no_const, features_to_reconstruct=one_hot_columns) # type: ignore
```

```python
binary_map = {
    "Crystal Structure": ("is Polycrystalline", "Single-crystal", "Polycrystalline"),
    "LiPF6 Electrolyte": ("Electrolyte LiPF6", "No", "Yes")
}

df_reconstructed_II = reconstruct_binary(df=df_reconstructed_I, reconstruction_map=binary_map)
```

```python
multibinary_pattern = r"Dopant|Space|Precursor Method|Electrolyte Solvent"

df_reconstructed_III, multibinary_columns = reconstruct_multibinary(df=df_reconstructed_II, pattern=multibinary_pattern, case_sensitive=True)
```

```python
show_null_columns(df_reconstructed_III)
```

## 3.5 Feature Selection

```python
# Drop columns unused by the experimental group
from ml_tools.data_exploration import match_and_filter_columns_by_regex

_, unused_columns = match_and_filter_columns_by_regex(df=df_reconstructed_III, 
                                                      pattern=r'^Dopant|^Precursor Method|^Electrolyte Solvent',
                                                      case_sensitive=True)
```

```python
df_reconstructed_III = df_reconstructed_III.drop(columns=unused_columns)
```

```python
summarize_dataframe(df_reconstructed_III)
```

## 4. Encode categorical features

```python
columns_to_encode = one_hot_columns + list(binary_map.keys()) + multibinary_columns

df_encoded, categorical_mapping = encode_categorical_features(df=df_reconstructed_III, 
                                                                 columns_to_encode=columns_to_encode, 
                                                                 encode_nulls=False, 
                                                                 split_resulting_dataset=False)
```

```python
summarize_dataframe(df_encoded)
```

```python
show_null_columns(df_encoded)
```

## 5. Make a FeatureSchema for the model

```python
df_features, df_targets = split_features_targets(df=df_encoded, targets=TARGETS)
```

```python
feature_schema = finalize_feature_schema(df_features=df_features, categorical_mappings=categorical_mapping)
```

## 6. Make optimization bounds template for continuous features

```python
make_continuous_bounds_template(directory=PM.optimization_results, feature_schema=feature_schema)
```

## 7. Save Artifacts

```python
df_final = merge_dataframes(df_features, df_targets)
```

```python
save_dataframe_with_schema(df=df_final, 
                           full_path=PM.optimization_data_file,
                           schema=feature_schema)
```

```python
feature_schema.to_json(PM.optimization_engineering)
```

```python
feature_schema.save_artifacts(directory=PM.optimization_engineering)
```
