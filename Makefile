.PHONY: all raw_data data_feature_eng imputed_datasets VIF MICE model_metrics optimization

all: raw_data data_feature_eng imputed_datasets VIF MICE model_metrics optimization

raw_data:
	mkdir -p raw_data

data_feature_eng:
	mkdir -p "data/Feature Engineering"

imputed_datasets:
	mkdir -p "data/MICE Imputed Datasets"

VIF:
	mkdir -p "data/MICE VIF Imputed Datasets"

MICE:
	mkdir -p "results/MICE"

model_metrics:
	mkdir -p "results/Model Metrics"

optimization:
	mkdir -p "results/Optimization Results"

