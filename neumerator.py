# CREATED: 6/20/15 4:56 PM by Justin Salamon <justin.salamon@nyu.edu>

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse


def majorityfilt(x, n):
    half_win = n // 2
    y = x.copy()
    for i in range(half_win, len(x)-half_win):
        data = x[i-half_win:i+half_win]
        counts = np.bincount(data)
        y[i] = np.argmax(counts)
    return y


def neumerator(csv_file):

    pitch = pd.read_csv('pitch/generosa.csv', header=None)
    cents_semi = 12*np.log2(pitch[1]/55.)
    cents_semi_round = np.round(cents_semi)

    time_nan = pitch[0][~np.isnan(cents_semi_round)]
    cents_semi_nan = cents_semi_round[~np.isnan(cents_semi_round)]

    cents_semi_maj = majorityfilt(np.array([int(c) for c in cents_semi_nan]), 300)

    plt.figure(figsize=(18,6))
    plt.plot(time_nan, cents_semi_maj)
    plt.axis([0, 25, 20, 40])
    plt.show()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file")

    args = parser.parse_args()

    neumerator(args.csv_file)