#!/usr/bin/env python3.9
# coding=utf-8
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import os

# muzete pridat libovolnou zakladni knihovnu ci knihovnu predstavenou na prednaskach
# dalsi knihovny pak na dotaz

""" Ukol 1:
načíst soubor nehod, který byl vytvořen z vašich dat. Neznámé integerové hodnoty byly mapovány na -1.

Úkoly:
- vytvořte sloupec date, který bude ve formátu data (berte v potaz pouze datum, tj sloupec p2a)
- vhodné sloupce zmenšete pomocí kategorických datových typů. Měli byste se dostat po 0.5 GB. Neměňte však na kategorický typ region (špatně by se vám pracovalo s figure-level funkcemi)
- implementujte funkci, která vypíše kompletní (hlubkou) velikost všech sloupců v DataFrame v paměti:
orig_size=X MB
new_size=X MB

Poznámka: zobrazujte na 1 desetinné místo (.1f) a počítejte, že 1 MB = 1e6 B. 
"""

# Columns to be converted into categories - could "o" be float?
_category_cols = ["k", "p", "q", "t", "l", "i", "h"]


def _get_usage_mib(df: pd.DataFrame):
    """
    Returns the deep memory usage of the given dataframe in mebibytes
    :param df:
    :return:
    """
    return df.memory_usage(index=True, deep=True).sum() / (2 ** 20)


def get_dataframe(filename: str, verbose: bool = False) -> pd.DataFrame:
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


# Ukol 2: počty nehod v jednotlivých regionech podle druhu silnic

def plot_roadtype(df: pd.DataFrame, fig_location: str = None,
                  show_figure: bool = False):
    pass


# Ukol3: zavinění zvěří
def plot_animals(df: pd.DataFrame, fig_location: str = None,
                 show_figure: bool = False):
    pass


# Ukol 4: Povětrnostní podmínky
def plot_conditions(df: pd.DataFrame, fig_location: str = None,
                    show_figure: bool = False):
    pass


if __name__ == "__main__":
    # zde je ukazka pouziti, tuto cast muzete modifikovat podle libosti
    # skript nebude pri testovani pousten primo, ale budou volany konkreni ¨
    # funkce.

    # tento soubor si stahnete sami, při testování pro hodnocení bude existovat
    accidents_df = get_dataframe("accidents.pkl.gz")
    plot_roadtype(accidents_df, fig_location="01_roadtype.png", show_figure=True)
    plot_animals(accidents_df, "02_animals.png", True)
    plot_conditions(accidents_df, "03_conditions.png", True)
