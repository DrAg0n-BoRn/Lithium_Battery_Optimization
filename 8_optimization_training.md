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
from ml_tools.ML_datasetmaster import DragonDatasetMulti
from ml_tools.ML_models import DragonTabularTransformer
from ml_tools.ML_models_advanced import DragonNodeModel
from ml_tools.ML_trainer import DragonTrainer
from ml_tools.ML_callbacks import DragonModelCheckpoint, DragonPatienceEarlyStopping, DragonReduceLROnPlateau
from ml_tools.ML_utilities import build_optimizer_params
from ml_tools.ML_configuration import (
    MultiTargetRegressionMetricsFormat, 
    FinalizeMultiTargetRegression, 
    DragonNodeParams, 
    DragonTabularTransformerParams, 
    DragonTrainingConfig
    )
from ml_tools.ML_utilities import inspect_model_architecture
from ml_tools.utilities import load_dataframe_with_schema
from ml_tools.IO_tools import train_logger
from ml_tools.schema import FeatureSchema
from ml_tools.keys import TaskKeys

from torch.optim import AdamW

from paths import PM
from helpers.constants import TARGETS
```

## 1. Parameters

```python
train_config = DragonTrainingConfig(
    validation_size=0.2,
    test_size=0.1,
    initial_learning_rate=0.001,
    batch_size=64,
    random_state=101,
    early_stop_patience=15,
    scheduler_patience=3,
    scheduler_lr_factor=0.5,
    task = TaskKeys.MULTITARGET_REGRESSION,
    device = "cuda:0",
    finalized_filename = "node_full"
)
```

## 2. Load Schema and Dataframe

```python
schema = FeatureSchema.from_json(PM.optimization_engineering)

df, _ = load_dataframe_with_schema(df_path=PM.optimization_data_file, schema=schema)
```

## 3. Make Datasets

```python
dataset = DragonDatasetMulti(pandas_df=df,
                             target_columns=TARGETS,
                             schema=schema,
                             kind=train_config.task, # type: ignore
                             feature_scaler="fit",
                             target_scaler="fit",
                             validation_size=train_config.validation_size,
                             test_size=train_config.test_size,
                             random_state=train_config.random_state)
```

## 4. Model and Trainer

```python
### MODEL SELECTION ###
use_NODE = True
#######################

if use_NODE:
    # NODE
    model_params = DragonNodeParams(
        schema=schema,
        out_targets=dataset.number_of_targets,
        embedding_dim=16,    
        num_trees=512,       
        num_layers=2,        
        tree_depth=5,
        additional_tree_output_dim=2,
        input_dropout=0.0,
        embedding_dropout=0.0,
        choice_function='entmax',
        bin_function='entmoid',
        batch_norm_continuous=False
    )
    
    model = DragonNodeModel(**model_params)
    # Initialize decision thresholds before training.
    model.data_aware_initialization(train_dataset=dataset.train_dataset, num_samples=1000)
    
else:
    # Tabular transformer
    model_params = DragonTabularTransformerParams(
        schema=schema,
        out_targets=dataset.number_of_targets,
        embedding_dim=1024,
        num_heads=4,
        num_layers=2,
        dropout=0.1
    )
    
    model = DragonTabularTransformer(**model_params)

# optimizer
optim_params = build_optimizer_params(model=model, weight_decay=0.001)
optimizer = AdamW(params=optim_params, lr=train_config.initial_learning_rate)

trainer = DragonTrainer(model=model,
                        train_dataset=dataset.train_dataset,
                        validation_dataset=dataset.validation_dataset,
                        kind=train_config.task, # type: ignore
                        optimizer=optimizer,
                        device=train_config.device, # type: ignore
                        checkpoint_callback=DragonModelCheckpoint(save_dir=PM.optimization_train_checkpoints),
                        early_stopping_callback=DragonPatienceEarlyStopping(patience=train_config.early_stop_patience),  # type: ignore
                        lr_scheduler_callback=DragonReduceLROnPlateau(patience=train_config.scheduler_patience,  # type: ignore
                                                                     factor=train_config.scheduler_lr_factor),  # type: ignore
                        )
```

## 5. Training

```python
history = trainer.fit(save_dir=PM.optimization_train_artifacts,
                    epochs=500,
                    batch_size=train_config.batch_size)
```

## 6. Evaluation

```python
trainer.evaluate(save_dir=PM.optimization_train_evaluation,
                 model_checkpoint="best",
                 test_data=dataset.test_dataset,
                 val_format_configuration=MultiTargetRegressionMetricsFormat(),
                 test_format_configuration=MultiTargetRegressionMetricsFormat(scatter_color='tab:brown'))
```

## 7. Explanation

```python
trainer.explain_captum(save_dir=PM.optimization_train_evaluation,
                       n_samples=200,
                       n_steps=100)
```

## 8. Save artifacts

```python
# Dataset artifacts
dataset.save_artifacts(PM.optimization_train_artifacts)

# Model artifacts
model.save(PM.optimization_train_artifacts)
inspect_model_architecture(model=model, save_dir=PM.optimization_train_artifacts)

# FeatureSchema
schema.to_json(PM.optimization_train_artifacts)

# Train log
train_logger(train_config=train_config,
             model_parameters=model_params,
             train_history=history,
             save_directory=PM.optimization_train_metrics)
```

## 9. Finalize Deep Learning

```python
trainer.finalize_model_training(model_checkpoint='current',
                                save_dir=PM.optimization_train_artifacts,
                                finalize_config=FinalizeMultiTargetRegression(filename=train_config.finalized_filename, # type: ignore
                                                                              target_names=dataset.target_names))
```
