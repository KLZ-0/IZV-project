#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path
import sys
import re
import urllib.parse
from pathlib import Path

import numpy as np
import zipfile


# Kromě vestavěných knihoven (os, sys, re, requests …) byste si měli vystačit s: gzip, pickle, csv, zipfile, numpy, matplotlib, BeautifulSoup.
# Další knihovny je možné použít po schválení opravujícím (např ve fóru WIS).
import requests
from bs4 import BeautifulSoup


class DataDownloader:
    """ TODO: dokumentacni retezce 

    Attributes:
        headers    Nazvy hlavicek jednotlivych CSV souboru, tyto nazvy nemente!  
        regions     Dictionary s nazvy kraju : nazev csv souboru
    """

    headers = ["p1", "p36", "p37", "p2a", "weekday(p2a)", "p2b", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13a",
               "p13b", "p13c", "p14", "p15", "p16", "p17", "p18", "p19", "p20", "p21", "p22", "p23", "p24", "p27",
               "p28",
               "p34", "p35", "p39", "p44", "p45a", "p47", "p48a", "p49", "p50a", "p50b", "p51", "p52", "p53", "p55a",
               "p57", "p58", "a", "b", "d", "e", "f", "g", "h", "i", "j", "k", "l", "n", "o", "p", "q", "r", "s", "t",
               "p5a"]

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

    _re_file_standard = re.compile(r"data-?gis-?(\d\d)-(\d\d\d\d).*")
    _re_file_december = re.compile(r"data-?gis-?(rok)?-?(\d\d\d\d).*")

    def __init__(self, url="https://ehw.fit.vutbr.cz/izv/", folder="data", cache_filename="data_{}.pkl.gz"):
        self._url = url
        self._folder = folder
        self._cache_filename = cache_filename

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

        # table = soup.find("table")
        # # print(table)
        # for row in table.findAll("tr"):
        #     for cell in row.findAll("td"):

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
        # self.download_data()

        reg_code = self.regions.get(region)
        if reg_code is None:
            return

        for file_zip in sorted(os.listdir(self._folder)):
            when = self._decode_filename(file_zip)
            if when is None:
                print("!!!", file_zip)
                continue

            print(file_zip, when)

    def get_dict(self, regions=None):
        pass


# TODO vypsat zakladni informace pri spusteni python3 download.py (ne pri importu modulu)
if __name__ == '__main__':
    dd = DataDownloader()
    dd.parse_region_data("STC")
