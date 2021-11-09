#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pathlib import Path

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

    # log 10
    with np.errstate(divide='ignore'):
        valarr = np.log10(valarr)

    # draw
    fig, ax = plt.subplots(sharex="all", sharey="all", figsize=(10, 3.8))
    im = ax.imshow(valarr)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Počet nehod", rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(regions)))
    ax.set_yticks(np.arange(len(causes)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(regions)
    ax.set_yticklabels(causes)

    ax.set_title("Absolutně")
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
