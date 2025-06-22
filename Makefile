.PHONY: all logs raw_data feature_eng MICE VIF model_metrics optimization

all: logs raw_data feature_eng MICE VIF model_metrics optimization

logs:
	mkdir -p Logs

raw_data:
	mkdir -p raw_data

feature_eng:
	mkdir -p "data/Feature Engineering"
	mkdir -p "data/Engineered Datasets"

MICE:
	mkdir -p "data/MICE Imputed Datasets"
	mkdir -p "results/MICE Metrics"

VIF:
	mkdir -p "data/VIF Imputed Datasets"
	mkdir -p "results/VIF Metrics"

model_metrics:
	mkdir -p "data/Train Datasets"
	mkdir -p "results/Model Metrics"

optimization:
	mkdir -p "data/Optimization Models"
	mkdir -p "results/Optimization Results"
