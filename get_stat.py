#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pathlib import Path

import matplotlib.colors
import numpy as np
import matplotlib.pyplot as plt
# povolene jsou pouze zakladni knihovny (os, sys) a knihovny numpy, matplotlib a argparse

from download import DataDownloader

causes = ["Přerušovaná žlutá", "Semafor mimo provoz", "Dopravní značky", "Přenosné dopravní značky",
          "Nevyznačena", "Žádná úprava"]


def plot_stat(data_source,
              fig_location=None,
              show_figure=False):

    # p24

    regions = np.unique(data_source["region"])

    valarr = np.ndarray((regions.shape[0], 6), dtype="i")
    for i, region in enumerate(regions):
        regdata = data_source["p24"][data_source["region"] == region]
        for cause in range(6):
            valarr[i][cause] = np.count_nonzero(regdata == cause)

    valarr = valarr.T[[1, 2, 3, 4, 5, 0]]
    valarr2 = (valarr.T / np.sum(valarr, axis=1)).T

    # draw
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex="all", sharey="all", figsize=(10, 8))
    im1 = ax1.imshow(valarr, norm=matplotlib.colors.LogNorm())
    im2 = ax2.imshow(valarr2)

    # Create colorbar
    cbar1 = ax1.figure.colorbar(im1, ax=ax1)
    cbar1.ax.set_ylabel("Počet nehod", rotation=-90, va="bottom")
    cbar2 = ax2.figure.colorbar(im2, ax=ax2)
    cbar2.ax.set_ylabel("Počet nehod", rotation=-90, va="bottom")

    # We want to show all ticks...
    ax1.set_xticks(np.arange(len(regions)))
    ax1.set_yticks(np.arange(len(causes)))
    # ... and label them with the respective list entries
    ax1.set_xticklabels(regions)
    ax1.set_yticklabels(causes)

    ax1.set_title("Absolutně")
    fig.tight_layout()

    if fig_location:
        Path(os.path.dirname(fig_location)).mkdir(parents=True, exist_ok=True)
        plt.savefig(fig_location)

    if show_figure:
        plt.show()


# TODO pri spusteni zpracovat argumenty
if __name__ == '__main__':
    dd = DataDownloader()
    data = dd.get_dict()
    # data = dd.get_dict(["KVK", "JHC", "PLK"])
    plot_stat(data, fig_location="/tmp/figs/fig1.png", show_figure=True)
    # plot_stat(data)
