#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import io
import os.path
import sys
import re
import urllib.parse
from pathlib import Path

import numpy as np
import zipfile


# Kromě vestavěných knihoven (os, sys, re, requests …) byste si měli vystačit s: gzip, pickle, csv, zipfile, numpy, matplotlib, BeautifulSoup.
# Další knihovny je možné použít po schválení opravujícím (např ve fóru WIS).
import psutil as psutil
import requests
from bs4 import BeautifulSoup


class DataDownloader:
    """ TODO: dokumentacni retezce 

    Attributes:
        headers    Nazvy hlavicek jednotlivych CSV souboru, tyto nazvy nemente!  
        regions     Dictionary s nazvy kraju : nazev csv souboru
    """

    # 64 total, 8 in each row
    headers = [
        "p1", "p36", "p37", "p2a", "weekday(p2a)", "p2b", "p6", "p7",
        "p8", "p9", "p10", "p11", "p12", "p13a", "p13b", "p13c",
        "p14", "p15", "p16", "p17", "p18", "p19", "p20", "p21",
        "p22", "p23", "p24", "p27", "p28", "p34", "p35", "p39",
        "p44", "p45a", "p47", "p48a", "p49", "p50a", "p50b", "p51",
        "p52", "p53", "p55a", "p57", "p58", "a", "b", "d",
        "e", "f", "g", "h", "i", "j", "k", "l",
        "n", "o", "p", "q", "r", "s", "t", "p5a"
    ]

    types = [
        "U", "i", "i", "M", "U", "i", "i", "i",
        "i", "i", "i", "i", "i", "i", "i", "i",
        "i", "i", "i", "i", "i", "i", "i", "i",
        "i", "i", "i", "i", "i", "i", "i", "i",
        "i", "i", "i", "i", "i", "i", "i", "i",
        "i", "i", "i", "i", "i", "f", "f", "f",
        "f", "f", "f", "U", "U", "i", "U", "U",
        "U", "U", "U", "U", "i", "i", "U", "i"
    ]

    regions = {
        "PHA": "00",
        "STC": "01",
        "JHC": "02",
        "PLK": "03",
        "ULK": "04",
        "HKK": "05",
        "JHM": "06",
        "MSK": "07",
        "OLK": "14",
        "ZLK": "15",
        "VYS": "16",
        "PAK": "17",
        "LBK": "18",
        "KVK": "19",
    }

    # replace these with a valid number
    _invalid_num_values = ["", "XX"] + [c + ":" for c in "ABDEFGHIL"]
    _invalid_num_replacement = "0"

    _re_file_standard = re.compile(r"data-?gis-?(\d\d)-(\d\d\d\d).*")
    _re_file_december = re.compile(r"data-?gis-?(rok)?-?(\d\d\d\d).*")

    def __init__(self, url="https://ehw.fit.vutbr.cz/izv/", folder="data", cache_filename="data_{}.pkl.gz"):
        self._url = url
        self._folder = folder
        self._cache_filename = cache_filename
        self.type_map = dict(zip(self.headers, self.types))

    def download_data(self):
        Path(self._folder).mkdir(parents=True, exist_ok=True)

        resp = requests.get(self._url)
        if resp.status_code != 200:
            print(f"Error: repsonse code {resp.status_code}", file=sys.stderr)
            return

        soup = BeautifulSoup(resp.text, features="html.parser")
        for button in soup.findAll("button"):
            file_location = button["onclick"].split("'")[1]
            file_name = os.path.basename(file_location)

            url = urllib.parse.urljoin(self._url, file_location)
            dest = os.path.join(self._folder, file_name)

            if Path(dest).exists():
                # print(f"Skipping: {file_name}")
                continue

            # print(f"Downloading: {file_name}")
            with requests.get(url, stream=True) as r:
                with open(dest, "wb") as f:
                    for chunk in r:
                        f.write(chunk)

    def _decode_filename(self, filename):
        """
        Decodes the given datagis file name into month and year
        :param filename: file name to be decoded
        :return: tuple(month : str, year : str) or None if got utter trash
        """
        res = self._re_file_standard.match(filename)
        if res is not None:
            return res.groups()

        res = self._re_file_december.match(filename)
        if res is not None:
            return "12", res.groups()[1]

    def parse_region_data(self, region):
        if not Path(self._folder).exists():
            self.download_data()

        reg_code = self.regions.get(region)
        if reg_code is None:
            return

        dataset = {colname: [] for colname in self.headers}

        for file_zip in os.listdir(self._folder):
            if not file_zip.endswith(".zip"):
                print("Not a ZIP file", file_zip, file=sys.stderr)
                continue

            with zipfile.ZipFile(os.path.join(self._folder, file_zip), "r") as data_zip:
                with data_zip.open(reg_code + ".csv", "r") as file_csv:
                    data_csv = csv.reader(io.TextIOWrapper(file_csv, encoding="cp1250"), delimiter=";", quotechar="\"")
                    for row in data_csv:
                        for i, csv_col in enumerate(row):
                            if self.types[i] in ["i", "f"] and csv_col in self._invalid_num_values:
                                dataset[self.headers[i]].append(self._invalid_num_replacement)
                                continue

                            if self.types[i] == "f":
                                csv_col = csv_col.replace(",", ".")

                            dataset[self.headers[i]].append(csv_col)

        for colname in dataset.keys():
            try:
                dataset[colname] = np.asarray(dataset[colname], dtype=self.type_map[colname])
            except ValueError as e:
                print(f"Conversion failed for {colname}", e)

        dataset["region"] = np.full(dataset[self.headers[0]].shape[0], region)

        return dataset

    def get_dict(self, regions=None):
        pass


# TODO vypsat zakladni informace pri spusteni python3 download.py (ne pri importu modulu)
if __name__ == '__main__':
    process = psutil.Process(os.getpid())
    print("MEM before", process.memory_info().rss / 1000000, "MB")

    dd = DataDownloader()
    bigdata = []
    for reg in dd.regions.keys():
        print(f"Processing {reg}")
        bigdata.append(dd.parse_region_data(reg))

    print("MEM after", process.memory_info().rss / 1000000, "MB")

    print(len(bigdata))
