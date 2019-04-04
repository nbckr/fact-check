import argparse

import matplotlib.pyplot as plt
import pandas as pd

from _4_B_fit_logistic_regression_model import fit_and_get_model, LOSS_HISTORY_FREQUENCY
from dataaccess.files_constants import GENERATED_LR_PREPROCESSED_TRAINING_DATA, GENERATED_LOGISTIC_REGRESSION_MODEL, \
    GENERATED_LOGISTIC_REGRESSION_LOSS_HISTORY
from dataaccess.files_io import read_pickle, write_pickle
from model.logistic_regression import LogisticRegressionModel
from util.logreg_preprocessing import extract_input_and_expected
from util.plots import show_plot_and_save_figure, prepare_seaborn_plots

parser = argparse.ArgumentParser()
parser.add_argument('--debug', help='use less data and less learning iterations', action='store_true')
parser.add_argument('--num_epochs', type=int, default=100000)
parser.add_argument('--learning_rate', type=float, default=0.01)
args = parser.parse_args()


def plot_loss_values(model: LogisticRegressionModel, loss_values: list):
    prepare_seaborn_plots()
    plt.xlabel('Epochs')
    plt.ylabel('Cross-Entropy Loss')
    plt.figtext(0.65, 0.8, r'$n = {:,}$'.format(model.num_epochs))
    plt.figtext(0.65, 0.75, r'$\alpha = {:,}$'.format(model.learning_rate))
    plt.plot([i * LOSS_HISTORY_FREQUENCY for i in range(len(loss_values))], loss_values, linewidth=4)
    show_plot_and_save_figure('logistic_regression_loss_values.png')


if __name__ == '__main__':
    training_data: pd.DataFrame = read_pickle(GENERATED_LR_PREPROCESSED_TRAINING_DATA)

    # use DataFrame.values to unpack the ndarrays in each cell
    train_input, train_expected = extract_input_and_expected(training_data)

    model, loss_values = fit_and_get_model(train_input, train_expected, args.num_epochs, args.learning_rate)
    write_pickle(GENERATED_LOGISTIC_REGRESSION_LOSS_HISTORY, loss_values)  # for plotting
    write_pickle(GENERATED_LOGISTIC_REGRESSION_MODEL, model)

    plot_loss_values(model, loss_values)
