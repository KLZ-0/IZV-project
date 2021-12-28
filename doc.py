import sys
from pathlib import Path
from typing import TextIO

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt, gridspec, cm, colors

weather_labels = ["Ideal", "Fog", "Light rain", "Rain",
                  "Snow", "Frost", "Strong wind"]


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
    fatal accidents (p13a > 0) depending on weather
    :param df: dataframe to examine
    :param fig_location: file name where the figure should be saved
    :param show_figure: if True shows the figure at runtime
    :return: None
    """
    # Static things
    pie1_cmap = colors.ListedColormap(["darkred", "lightgrey"])

    # plot setup
    sns.set_theme(style="whitegrid")
    # fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7.5))
    fig = plt.figure(constrained_layout=True,
                     figsize=(10, 7.5))
    spec = gridspec.GridSpec(ncols=2, nrows=2,
                             figure=fig)

    ax1 = fig.add_subplot(spec[0, 0])
    ax2 = fig.add_subplot(spec[0, 1])
    ax3 = fig.add_subplot(spec[1, :])

    # categorize and label the weather
    df["weather"] = pd.cut(df["p18"], [i for i in range(8)],
                           labels=weather_labels)

    # filter out "other" weather conditions
    df = df[df["p18"] > 0]

    # aggregate by weather
    groups = df.groupby("weather").agg({"p1": "count"})

    # left pie chart - weather conditions generalized
    total_diff = groups.iloc[0].append(groups.iloc[1:].sum(), ignore_index=True)[::-1]
    total_diff.plot(kind="pie", ax=ax1, legend=False,
                    labels=["Worsened", "Ideal"], colormap=pie1_cmap, explode=(0, 0.1))
    ax1.set_title("Weather conditions at accidents overall")
    ax1.set_ylabel("")
    w_perc = (total_diff[1] / total_diff.sum()) * 100
    print(f"total percentage of worsened conditions during accidents: {w_perc:.2f}%")

    # right pie chart - worsened conditions by type
    worsened = groups.iloc[1:]
    worsened.plot(kind="pie", y="p1", ax=ax2, legend=False)
    ax2.set_title("Worsened weather conditions by type")
    ax2.set_ylabel("")

    # filter out normal weather so it does not affect the figure too much
    # we only want to see worsened conditions
    df = df[df["p18"] > 1]
    df["weather"] = pd.cut(df["p18"], [i for i in range(1, 8)],
                           labels=weather_labels[1:])

    # aggregate by weather and region
    data = df.groupby(["region", "weather"]).agg({"p1": "count"}).reset_index()

    # sort the dataframe so the regions are roughly descending
    data.sort_values(by=["p1"], ascending=False, inplace=True)

    # bottom bar plot
    s = sns.barplot(data=data, x="region", y="p1", hue="weather", ax=ax3)
    s.set_title("Accidents caused by worsened weather conditions across regions")
    s.set_xlabel("Region")
    s.set_ylabel("Accidents")
    s.get_legend().set(title="Weather condition")

    w_total_stc = data[data["region"] == "STC"]["p1"].sum()
    print(f"Total accidents caused while worsened conditions: {w_total_stc}")

    if fig_location:
        Path(fig_location).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(fig_location)

    if show_figure:
        plt.show()


def create_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Format the table so that it represents something useful
    :param df: dataframe to examine
    :return: formatted dataframe
    """
    # categorize and label the weather
    df["weather"] = pd.cut(df["p18"], [i for i in range(8)],
                           labels=weather_labels)

    # filter out "other" weather conditions and limit to years before 2021
    df = df[(df["p18"] > 0) & (df["date"].dt.year < 2021)]

    # aggregate by weather and date
    data = df.groupby(["weather", "date"]).agg({"p1": "count"})

    # expand index, undersample and restore index
    data = data.unstack("weather")
    data = data.resample("Y").sum()
    data = data.stack("weather")
    data.reset_index(inplace=True)

    # create pivot table
    return pd.pivot_table(data, index="weather", columns="date", values="p1")


def table_to_tex(df: pd.DataFrame,
                 stream: TextIO = sys.stdout):
    """
    Print the formatted table as output from create_table to the given stream in proper latex format
    :param df: dataframe to examine
    :param stream: stream to write the data
    :return: None
    """
    print("%%%%%%%% INSERT TABLE %%%%%%%%")
    df.columns = [col.year for col in df.columns]
    df.to_latex(buf=stream)
    print("%%%%%%%% INSERT TABLE %%%%%%%%")


if __name__ == '__main__':
    # TODO: turn off show_figure
    df_v = get_dataframe("accidents.pkl.gz")
    plot_fig(df_v, fig_location="fig.pdf", show_figure=True)
    table_to_tex(create_table(df_v))
