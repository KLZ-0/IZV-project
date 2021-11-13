#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
from pathlib import Path

import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np

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
    valarr2 = (valarr.T / np.sum(valarr, axis=1)).T * 100
    valarr2[valarr2 == 0] = np.nan

    # draw
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex="all", sharey="all", figsize=(10, 7.5))
    im1 = ax1.imshow(valarr, norm=matplotlib.colors.LogNorm())
    im2 = ax2.imshow(valarr2, cmap="plasma")

    # Create colorbar
    cbar1 = ax1.figure.colorbar(im1, ax=ax1)
    cbar1.ax.set_ylabel("Počet nehod", rotation=90, va="top")
    cbar2 = ax2.figure.colorbar(im2, ax=ax2)
    cbar2.ax.set_ylabel("Podíl nehod pro danou příčinu [%]", rotation=90, va="top")

    # We want to show all ticks...
    ax1.set_xticks(np.arange(len(regions)))
    ax1.set_yticks(np.arange(len(causes)))
    # ... and label them with the respective list entries
    ax1.set_xticklabels(regions)
    ax1.set_yticklabels(causes)

    ax1.set_title("Absolutně")
    ax2.set_title("Relativně vůči příčině")
    fig.tight_layout()

    if fig_location:
        Path(os.path.dirname(fig_location)).mkdir(parents=True, exist_ok=True)
        plt.savefig(fig_location)

    if show_figure:
        plt.show()


# TODO pri spusteni zpracovat argumenty
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get basic stats")
    parser.add_argument('--fig_location', default=None,
                        help='Figure save location')
    parser.add_argument('--show_figure', action='store_true',
                        help='Show figures')

    args = parser.parse_args()

    dd = DataDownloader()
    data = dd.get_dict()
    plot_stat(data, fig_location=args.fig_location, show_figure=args.show_figure)
