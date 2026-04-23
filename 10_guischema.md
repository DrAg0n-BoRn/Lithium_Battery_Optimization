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

```python
from ml_tools.schema import FeatureSchema, create_guischema_template, make_multibinary_groups

from paths import PM
from helpers.constants import CONTINUOUS_OPTIMIZATION_RANGE, TARGETS
```

## 1. Load Feature Schema

```python
feature_schema = FeatureSchema.from_json(directory=PM.optimization_engineering)
```

## 2. Construct multibinary groups

```python
multibinary_groups_list = ["Dopant", "Electrolyte Solvent", "Precursor Method", "Space"]

multibinary_groups = make_multibinary_groups(feature_schema=feature_schema, group_prefixes=multibinary_groups_list)
```

## 3. Create GUI Schema

```python
create_guischema_template(directory=PM.results,
                          feature_schema=feature_schema,
                          continuous_ranges=CONTINUOUS_OPTIMIZATION_RANGE,
                          targets=TARGETS,
                          multibinary_groups=multibinary_groups)
```
