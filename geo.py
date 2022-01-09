#!/usr/bin/python3.8
# coding=utf-8
from pathlib import Path

import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily as ctx
import sklearn.cluster
import numpy as np


def make_geo(df: pd.DataFrame) -> geopandas.GeoDataFrame:
    """
    Converts the given dataframe to a GeoDataFrame
    :param df: dataframe with "d" and "e" columns as coordinates
    :return: a valid GeoDataFrame
    """
    # Make a date column
    df["date"] = pd.to_datetime(df["p2a"], cache=True)

    # Convert af few object columns to categories
    _category_cols = ["k", "p", "q", "t", "l", "i", "h"]
    df[_category_cols] = df[_category_cols].astype("category")

    # Remove rows without location
    df = df[(df["d"].notna()) & (df["e"].notna())]

    # transform to GeoDataFrame
    return geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df["d"], df["e"]), crs="EPSG:5514")


def plot_geo(gdf: geopandas.GeoDataFrame, fig_location: str = None,
             show_figure: bool = False):
    """
    Plots accident locations to 6 subplots depending on road type and year
    :param gdf: the GeoDataFrame from which to plot
    :param fig_location: file name where the figure should be saved
    :param show_figure: if True shows the figure at runtime
    :return: None
    """
    # Static things
    colors = ["green", "red"]
    roadtypes = ["dialnice", "cesty prvej triedy"]
    chosen_region = "JHM"
    title_str = chosen_region + " kraj: {road_type} ({year})"

    # Subplots
    fig, ax = plt.subplots(3, 2, figsize=(8, 10))

    # filter region and transform to webmercator
    data = gdf[gdf["region"] == chosen_region].to_crs("EPSG:3857")

    # filter to only the data we need
    # this is also needed to determine the envelope for the maps
    data = data[data["date"].dt.year.isin([2018, 2019, 2020]) & data["p36"].isin([0, 1])]

    # Save the map using the whole boundary -> same map for each subplot
    bounds = data.total_bounds

    for i, ax_year in enumerate(ax):
        target_year = 2018 + i
        bitmap_year = data["date"].dt.year == target_year

        for u, ax_roadtype in enumerate(ax_year):
            ax_roadtype.set_axis_off()
            ax_roadtype.set_xlim(xmin=bounds[0], xmax=bounds[2])
            ax_roadtype.set_ylim(ymin=bounds[1], ymax=bounds[3])
            data[bitmap_year & (data["p36"] == u)].plot(ax=ax_roadtype, markersize=1, color=colors[u])
            ctx.add_basemap(ax_roadtype, crs=data.crs.to_string(), alpha=0.9, attribution_size=6,
                            reset_extent=False, source=ctx.providers.Stamen.TonerLite)
            ax_roadtype.set_title(title_str.format(road_type=roadtypes[u], year=target_year), fontsize="small")

    plt.tight_layout()

    if fig_location:
        Path(fig_location).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(fig_location)

    if show_figure:
        plt.show()


def plot_cluster(gdf: geopandas.GeoDataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """
    Plots accident locations with clustered color depending on the frequency of accidents in that location
    :param gdf: the GeoDataFrame from which to plot
    :param fig_location: file name where the figure should be saved
    :param show_figure: if True shows the figure at runtime
    :return: None
    """
    # Static things
    chosen_region = "JHM"
    title_str = f"Nehody v {chosen_region} kraji na cestách 1. triedy"

    # Subplots
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))

    # filter region, roadtype and transform to webmercator
    data = gdf[(gdf["region"] == chosen_region) & (gdf["p36"] == 1)].to_crs("EPSG:3857")

    # collect points in a 2d array
    points = np.reshape(list(zip(data.geometry.x, data.geometry.y)), (-1, 2))

    # cluster into frequency groups
    # Agglomerative clustering was chosen because of many clusters and connectivity constraints
    # The results after agglomerative clustering also resemble the given example map the most
    # and this clustering method produces similar results in each run unlike e.g. MiniBatch KMeans
    data["frequency_group"] = sklearn.cluster.AgglomerativeClustering(n_clusters=20).fit(points).labels_

    # magic at this point.. for each group of points assign the cluster size
    # this value will represent the color in the resulting map
    data = data.dissolve(by="frequency_group", aggfunc={"p1": "count"})

    data.plot(ax=ax, markersize=1, column="p1", legend=True)
    ax.set_axis_off()
    ctx.add_basemap(ax, crs=data.crs.to_string(), alpha=0.9, attribution_size=6,
                    reset_extent=False, source=ctx.providers.Stamen.TonerLite)
    ax.set_title(title_str, fontsize="small")
    plt.tight_layout()

    if fig_location:
        Path(fig_location).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(fig_location)

    if show_figure:
        plt.show()


if __name__ == "__main__":
    # zde muzete delat libovolne modifikace
    gdf_v = make_geo(pd.read_pickle("accidents.pkl.gz"))
    plot_geo(gdf_v, "geo1.png", True)
    plot_cluster(gdf_v, "geo2.png", True)
