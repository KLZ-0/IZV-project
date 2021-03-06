#!/usr/bin/env python3.9
# coding=utf-8
from pathlib import Path

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

# Columns to be converted into categories
_category_cols = ["k", "p", "q", "t", "l", "i", "h"]


def _get_usage_mib(df: pd.DataFrame):
    """
    Returns the deep memory usage of the given dataframe in mebibytes
    :param df: dataframe to examine
    :return: None
    """
    return df.memory_usage(index=True, deep=True).sum() / (2 ** 20)


def get_dataframe(filename: str, verbose: bool = False) -> pd.DataFrame:
    """
    Load a dataframe from the given pickle file
    :param filename: valid dataframe pickle - gz, bz2, zip, or xz compressed
    :param verbose: print verbose information about the dataframe memory usage
    :return: the loaded dataframe
    """
    df = pd.read_pickle(filename)

    if verbose:
        print(f"orig_size={_get_usage_mib(df):.1f} MB")

    # Make a date column
    df["date"] = pd.to_datetime(df["p2a"], cache=True)

    # Convert af few object columns to categories
    df[_category_cols] = df[_category_cols].astype("category")

    if verbose:
        print(f"new_size={_get_usage_mib(df):.1f} MB")

    return df


def plot_roadtype(df: pd.DataFrame, fig_location: str = None,
                  show_figure: bool = False):
    """
    Plot accidents by road type in 4 selected regions
    :param df: dataframe to examine
    :param fig_location: file name where the figure should be saved
    :param show_figure: if True shows the figure at runtime
    :return: None
    """
    # static things
    selected_regions = ["JHM", "JHC", "PLK", "ULK"]
    labels = ["Žiadna z uvedených", "Dvojpruhová",
              "Trojpruhová", "Štvorpruhová",
              "Viacpruhová", "Rýchlostná cesta"]
    labels_order = labels[1:] + labels[:1]

    # set background for subplots
    sns.set_style("darkgrid")

    # remove top and right spines
    sns.despine()

    # categorize and label the road types
    df["road_type"] = pd.cut(df["p21"], [-1, 0, 1, 2, 4, 5, 6], labels=labels)

    # select regions
    data = df[df["region"].isin(selected_regions)]

    # group and count
    data = data.groupby(["road_type", "region"]).agg(
        {"p1": "count"}).reset_index()

    # plot
    s = sns.catplot(data=data, x="region", y="p1",
                    col="road_type",
                    col_wrap=3, kind="bar",
                    height=2.5, aspect=1.15, legend=False,
                    col_order=labels_order, hue_order=labels_order,
                    hue="road_type", dodge=False,
                    sharey=False, sharex=False)

    plt.suptitle("Počet nehôd podľa druhu cesty")
    s.set_titles("{col_name}")
    s.set_xlabels("Kraj")
    s.set_ylabels("Počet nehôd")
    s.tight_layout()

    if fig_location:
        Path(fig_location).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(fig_location)

    if show_figure:
        plt.show()


def plot_animals(df: pd.DataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """
    Plot causes for each month in 4 selected regions
    :param df: dataframe to examine
    :param fig_location: file name where the figure should be saved
    :param show_figure: if True shows the figure at runtime
    :return: None
    """
    # static things
    selected_regions = ["JHM", "JHC", "PLK", "ULK"]
    labels = ["Vodičom", "Zverou", "Iné"]

    # set background for subplots
    sns.set_style("darkgrid")

    # remove all spines
    sns.despine(top=True, bottom=True, left=True, right=True)

    # make new column
    df["cause"] = df["p10"]

    # remap "pedestrians" cause from 3 -> 8 so we can use category intervals
    df.loc[df["cause"] == 3, "cause"] = 8

    # categorize and label the causes
    df["cause"] = pd.cut(df["cause"], [-1, 2, 4, 10], labels=labels)

    # select regions and consider only years before 2021
    data = df[
        df["region"].isin(selected_regions) & (df["date"].dt.year < 2021)]

    # group and count
    data = data.groupby(["region", data.date.dt.month, "cause"]).agg(
        {"p1": "count"}).reset_index()

    # plot
    s = sns.catplot(data=data, x="date", y="p1",
                    hue="cause", col="region",
                    col_wrap=2, kind="bar",
                    height=2.5, aspect=1.4,
                    legend=True, legend_out=True,
                    sharey=False, sharex=False)

    s.set_titles("Kraj: {col_name}")
    s.set_xlabels("Mesiac")
    s.set_ylabels("Počet nehôd")
    s.legend.set(title="Zavinenie")
    s.tight_layout()

    if fig_location:
        Path(fig_location).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(fig_location)

    if show_figure:
        plt.show()


def plot_conditions(df: pd.DataFrame, fig_location: str = None,
                    show_figure: bool = False):
    """
    Plot conditions during each month in 4 selected regions
    :param df: dataframe to examine
    :param fig_location: file name where the figure should be saved
    :param show_figure: if True shows the figure at runtime
    :return: None
    """
    # static things
    selected_regions = ["JHM", "JHC", "PLK", "ULK"]
    labels = ["Nesťažené", "Hmla", "Na počiatku dažďa", "Dážď",
              "Sneženie", "Tvorí sa námraza", "Nárazový vietor"]

    # set background for subplots
    sns.set_style("darkgrid")

    # remove all spines
    sns.despine(top=True, bottom=True, left=True, right=True)

    # make new column
    df["weather"] = df["p18"]

    # categorize and label the weather
    df["weather"] = pd.cut(df["weather"], [i for i in range(8)],
                           labels=labels)

    # select regions, drop rows with "other" weather condition
    # and consider only years before 2021
    data = df[df["region"].isin(selected_regions)
              & (df["p18"] != 0)
              & (df["date"].dt.year < 2021)]

    # make a pivot table
    data = pd.pivot_table(data, columns=["weather"], values="p1",
                          index=["region", "date"], aggfunc="count")

    # rearrange index to match the desired index in the next step
    target = data.stack(level="weather").unstack(level="region")

    # resample for every region and store in the target dataframe
    for i, region in enumerate(selected_regions):
        tmp = data.loc[region].resample("M").sum()
        target[region] = tmp.stack(level="weather")

    # drop nans, stack the region and reset the index to expand the dataframe
    target.dropna(how='all', inplace=True)
    target = target.stack(level="region").reset_index()

    # plot
    s = sns.relplot(data=target, x="date", y=0,
                    hue="weather", col="region",
                    col_wrap=2, kind="line",
                    height=2.5, aspect=1.4)

    s.set_titles("Kraj: {col_name}")
    s.set_xlabels("")
    s.set_ylabels("Počet nehôd")
    s.legend.set(title="Podmienky")
    s.set(xmargin=0)
    s.set(xticks=[f"20{year}-01" for year in range(16, 22)])
    s.set_xticklabels([f"01/{year}" for year in range(16, 22)])
    s.tight_layout()

    if fig_location:
        Path(fig_location).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(fig_location)

    if show_figure:
        plt.show()


if __name__ == "__main__":
    accidents_df = get_dataframe("accidents.pkl.gz", verbose=True)
    plot_roadtype(accidents_df, fig_location="01_roadtype.png",
                  show_figure=True)
    plot_animals(accidents_df, "02_animals.png", True)
    plot_conditions(accidents_df, "03_conditions.png", True)
