from ml_tools.VIF_factor import compute_vif_multi
from paths import PM
from helpers.constants import TARGETS

def main():
    compute_vif_multi(input_directory=PM.mice_datasets,
                    output_plot_directory=PM.vif_metrics,
                    output_dataset_directory=PM.vif_datasets,
                    ignore_columns=TARGETS)


if __name__ == "__main__":
    main()
