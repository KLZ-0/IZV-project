#!/usr/bin/python3.8
# coding=utf-8
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily
import sklearn.cluster
import numpy as np


# muzete pridat vlastni knihovny


def make_geo(df: pd.DataFrame) -> geopandas.GeoDataFrame:
    """
    Konvertovani dataframe
    do geopandas.GeoDataFrame se spravnym kodovani
    """
    # Remove rows without location
    df = df[(df["d"] != np.nan) & (df["e"] != np.nan)]

    # Make a date column
    df["date"] = pd.to_datetime(df["p2a"], cache=True)

    # Convert af few object columns to categories
    _category_cols = ["k", "p", "q", "t", "l", "i", "h"]
    df[_category_cols] = df[_category_cols].astype("category")

    # transform to GeoDataFrame
    return geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df["d"], df["e"]), crs="EPSG:5514")


def plot_geo(gdf: geopandas.GeoDataFrame, fig_location: str = None,
             show_figure: bool = False):
    """
    Vykresleni grafu s sesti podgrafy podle lokality nehody
     (dalnice vs prvni trida) pro roky 2018-2020
     """
    pass


def plot_cluster(gdf: geopandas.GeoDataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """
    Vykresleni grafu s lokalitou vsech nehod
    v kraji shlukovanych do clusteru
    """
    pass


if __name__ == "__main__":
    # zde muzete delat libovolne modifikace
    gdf_v = make_geo(pd.read_pickle("accidents.pkl.gz"))
    plot_geo(gdf_v, "geo1.png", True)
    plot_cluster(gdf_v, "geo2.png", True)
