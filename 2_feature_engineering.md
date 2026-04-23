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
from helpers.constants import TARGETS
from ml_tools.utilities import load_dataframe, save_dataframe, merge_dataframes
from ml_tools.data_exploration import info
info()
```

```python
from ml_tools.data_exploration import (summarize_dataframe, 
                                       drop_macro,
                                       clean_column_names,
                                       split_features_targets,
                                       split_continuous_binary, 
                                       plot_value_distributions, 
                                       standardize_percentages)
```

## 1. Load dataset

```python
df_raw, _ = load_dataframe(df_path=PM.processed_data_file, kind="pandas")
```

## 2. Drop dummy columns and fix entries

```python
df_clean_drop = drop_macro(df=df_raw,
                      log_directory=PM.feature_engineering_metrics,
                      targets=TARGETS,
                      skip_targets=True,
                      threshold=0.7)
```

### 2.1 Sanitize column names

```python
df_clean_drop_sanitized = clean_column_names(df=df_clean_drop)
```

### 2.2 Fix percentage values

```python
df_clean_drop_sanitized_standard = standardize_percentages(df=df_clean_drop_sanitized, columns=[TARGETS[1], TARGETS[2]])
```

```python
summarize_dataframe(df_clean_drop_sanitized_standard)
```

## 3. Get splits: Features, Targets

```python
df_features, df_targets = split_features_targets(df=df_clean_drop_sanitized_standard, targets=TARGETS)
```

## 4. Split features: Continuous, Binary

```python
df_continuous, df_binary = split_continuous_binary(df=df_features)
```

```python
summarize_dataframe(df_continuous)
```

```python
summarize_dataframe(df_binary)
```

## 5. Value Distributions


Plot all distributions to get corrected value ranges (except binary columns)

```python
plot_value_distributions(df=df_continuous, save_dir=PM.feature_engineering_raw, categorical_cardinality_threshold=0)
```

```python
plot_value_distributions(df=df_targets, save_dir=PM.feature_engineering_raw, categorical_cardinality_threshold=0)
```

## 6. Merge Dataframe

```python
df_processed_full = merge_dataframes(df_continuous, df_binary, df_targets)
```

## 7. Save dataset & Objects

```python
save_dataframe(df=df_processed_full, full_path=PM.engineered_raw_file)
```
