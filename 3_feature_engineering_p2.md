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

# Feature Engineering

```python
from paths import PM
from helpers.constants import TARGETS, CONTINUOUS_FEATURES_RANGE, TARGETS_RANGE
from ml_tools.utilities import load_dataframe, save_dataframe, merge_dataframes
from ml_tools.serde import serialize_object
from ml_tools.data_exploration import info
info()
```

```python
from ml_tools.data_exploration import (drop_outlier_samples,
                                       plot_value_distributions,
                                       plot_correlation_heatmap,
                                       split_features_targets,
                                       split_continuous_binary)
```

## Load and Split data

```python
df_raw, _ = load_dataframe(df_path=PM.engineered_raw_file, kind="pandas")
```

```python
df_drop = drop_outlier_samples(df=df_raw, bounds_dict=CONTINUOUS_FEATURES_RANGE | TARGETS_RANGE)
```

```python
df_features, df_targets = split_features_targets(df=df_drop, targets=TARGETS)
```

```python
df_continuous, df_binary = split_continuous_binary(df=df_features)
```

## Value Distributions

```python
plot_value_distributions(df=df_continuous, save_dir=PM.feature_engineering_final, categorical_cardinality_threshold=0)
```

```python
plot_value_distributions(df=df_targets, save_dir=PM.feature_engineering_final, categorical_cardinality_threshold=0)
```

## Plot correlation heatmap

```python
plot_correlation_heatmap(df=df_continuous, save_dir=PM.feature_engineering_metrics, plot_title="Continuous Features")
```

```python
plot_correlation_heatmap(df=df_binary, save_dir=PM.feature_engineering_metrics, plot_title="Binary Features")
```

## Save

```python
df_final = merge_dataframes(df_continuous, df_binary, df_targets)
```

```python
save_dataframe(df=df_final, full_path=PM.engineered_final_file)
```

```python
serialize_object(obj=df_binary.columns.to_list(), file_path=PM.binary_columns_file)
```

```python
serialize_object(obj=df_continuous.columns.to_list(), file_path=PM.continuous_columns_file)
```

## Make train datasets

```python
from ml_tools.utilities import train_dataset_orchestrator

train_dataset_orchestrator(list_of_dirs=[PM.engineered_final_file.parent],
                           target_columns=TARGETS,
                           save_dir=PM.train_datasets)
```
