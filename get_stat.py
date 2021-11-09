#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
# povolene jsou pouze zakladni knihovny (os, sys) a knihovny numpy, matplotlib a argparse

from download import DataDownloader


def plot_stat(data_source,
              fig_location=None,
              show_figure=False):

    # p24

    regions = np.unique(data_source["region"])
    print(regions)

    valarr = np.ndarray((regions.shape[0], 6), dtype="i")
    for i, region in enumerate(regions):
        for cause in range(6):
            valarr[i][cause] = np.count_nonzero(data_source["p24"][data_source["region"] == region] == cause)

    print(valarr)


# TODO pri spusteni zpracovat argumenty
if __name__ == '__main__':
    dd = DataDownloader()
    data = dd.get_dict(["KVK", "JHC", "PLK"])
    plot_stat(data)
