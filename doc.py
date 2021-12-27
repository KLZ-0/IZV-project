import sys
from pathlib import Path
from typing import TextIO

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


def get_dataframe(filename: str) -> pd.DataFrame:
    """
    Load a dataframe from the given pickle file
    :param filename: valid dataframe pickle - gz, bz2, zip, or xz compressed
    :return: the loaded dataframe
    """
    df = pd.read_pickle(filename)

    # Make a date column
    df["date"] = pd.to_datetime(df["p2a"], cache=True)

    # Convert af few object columns to categories
    _category_cols = ["k", "p", "q", "t", "l", "i", "h"]
    df[_category_cols] = df[_category_cols].astype("category")

    return df


def plot_fig(df: pd.DataFrame,
             fig_location: str = None,
             show_figure: bool = False):
    """
    Plot the figure for the report
    Dependence of wather on accidents and deaths
    :param df: dataframe to examine
    :param fig_location: file name where the figure should be saved
    :param show_figure: if True shows the figure at runtime
    :return: None
    """
    # Static things
    labels = ["Hmla", "Na počiatku dažďa", "Dážď",
              "Sneženie", "Tvorí sa námraza", "Nárazový vietor"]

    # plot setup
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7.5))
    sns.set_theme(style="whitegrid")

    # categorize and label the weather
    df["weather"] = pd.cut(df["p18"], [i for i in range(1, 8)],
                           labels=labels)

    # filter out non-fatal accidents and remove normal weather
    df = df[(df["p13a"] > 0) & (df["p18"] > 1)]

    # fatal accidents (p13a > 0) depending on weather
    groups = df.groupby("weather").agg({"p1": "count"})

    pivot = pd.pivot_table(df, columns=["region"], values="p1",
                           index=["weather"], aggfunc="count")

    data = df.groupby(["region", "weather"]).agg({"p1": "count"}).reset_index()

    s = sns.barplot(data=data, x="region", y="p1", hue="weather", ax=ax2)

    # s = sns.catplot(data=data, x="region", y="p1", hue="weather", legend=True, legend_out=True, kind="bar")

    # s = sns.catplot(data=data, x="region", y="p1",
    #                 col="weather", col_wrap=3, kind="bar",
    #                 height=2.5, aspect=1.15, legend=False,
    #                 sharey=False, sharex=False)

    if fig_location:
        Path(fig_location).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(fig_location)

    if show_figure:
        plt.show()

    pass


def create_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Format the table so that it represents something useful
    :param df: dataframe to examine
    :return: formatted dataframe
    """
    pass


def table_to_tex(df: pd.DataFrame,
                 stream: TextIO = sys.stdout):
    """
    Print the formatted table as output from create_table to the given stream in proper latex format
    :param df: dataframe to examine
    :param stream: stream to write the data
    :return: None
    """
    pass


if __name__ == '__main__':
    # TODO: turn off show_figure
    df_v = get_dataframe("accidents.pkl.gz")
    plot_fig(df_v, fig_location="fig.pdf", show_figure=True)
    table_to_tex(create_table(df_v))
