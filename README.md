# Data Analysis and Visualization in Python (IZV)

*Project for the academic year 2021/2022*

# Results

The project is evaluated in 3 separate parts

Total points: 93 (easy 1A)

Total time: ~6 days (probably less if you are using your time efficiently...)

## [Part 1](/zadani1.pdf)

Contents:

- [download.py](/download.py)
- [get_stat.py](/get_stat.py)

Generated figures:

- [get_stat.get_stat()](/fig/01/get_stat.pdf)

Rating (20/20):

```
Hodnoceni projektu 1: xkalaz00
================================================================================
+2 delky vsech datovych sloupcu jsou stejne (az 2 bodu)
+2 stahlo se 95_835 zaznamu (az 2 bodu)
+2 uspesne se stahl Plzensky kraj (s chybou v textu) (az 2 bodu)
+1 stahl se Karlovarsky kraj bez duplikatu (az 1 bodu)
+1 podarilo se vytvorit pandas.DataFrame (az 1 bodu)
+1 rozumne rozlozeni datovych typu (az 1 bodu)
+1 souradnice jsou spravne jako floaty i s desetinnymi misty (az 1 bodu)
+1.00 rychlost zpracovani 1.42 s  (az 1 bodu)
+1 obrazky se ulozily spravne (a.png, ./b.png, t/c.png) (az 1 bodu)
+3.00 kvalita kodu downloader.py (az 3 bodu)
+3.00 kvalita kodu get_stat.py (az 3 bodu)
+2.00 graf z get_stat.py (az 2 bodu)
+0 bonus (az 0 bodu)
CELKEM: 20.0 bodu

Komentar k hodnoceni
================================================================================
takto jsem si ten kod prestavoval.
Dokonce odpustim i to, ze cbar nema definovane krajove
hodnoty :-)
```

## [Part 2](/zadani2.pdf)

Contents:

- [analysis.py](/analysis.py)

Generated figures:

- [analysis.plot_roadtype()](/fig/02/01_roadtype.pdf)
- [analysis.plot_animals()](/fig/02/02_animals.pdf)
- [analysis.plot_conditions()](/fig/02/03_conditions.pdf)

Rating (19/20):

```
Hodnoceni druhe casti projektu: xkalaz00
================================================================================
+1.00 pouzite kategoricke typy (>=2) (az 1 bodu)
+1.00 ostatni typy jsou korektni (ints>30 & floats>=6) (az 1 bodu)
+1.00 vhodne vyuziti pameti (< 500 MB) (az 1 bodu)
+1.00 spravne konvertovane datum (rok 2016 - 2021) (az 1 bodu)
+0.12 funkce get_dataframe ma spravne docstring (PEP257) (az 0.125 bodu)
+0.12 funkce plot_roadtype ma spravne docstring (PEP257) (az 0.125 bodu)
+0.12 funkce plot_animals ma spravne docstring (PEP257) (az 0.125 bodu)
+0.12 funkce plot_conditions ma spravne docstring (PEP257) (az 0.125 bodu)
+0.50 funkce plot_conditions trva do 1500 ms (az 0.5 bodu)
+2.00 kvalita kodu funkce plot_conditions (az 2 bodu)
+2.00 vizualni dojem z grafu plot_conditions (az 2 bodu)
+0.50 funkce plot_animals trva do 1200 ms (az 0.5 bodu)
+1.00 kvalita kodu funkce plot_animals (az 2 bodu)
+2.00 vizualni dojem z grafu plot_animals (az 2 bodu)
+0.50 funkce plot_roadtype trva do 1000 ms (az 0.5 bodu)
+2.00 kvalita kodu funkce plot_roadtype (az 2 bodu)
+2.00 vizualni dojem z grafu plot_roadtype (az 2 bodu)
+2.00 kvalita kodu dle PEP8 (0 kritickych, 0 E2.., 0 E7..)) (az 2 bodu)
CELKEM: 19.0 bodu

Komentar k hodnoceni (zejmena k vizualizacim)
================================================================================
v poradku, jen animals nejsou filtrovane dle p58
```

## [Part 3](/nehody-zadani.pdf)

Contents:

- [geo.py](/geo.py)
- [stat.ipynb](/stat.ipynb)
- [doc.py](/doc.py)
- [doc.pdf](/doc.pdf)

Generated figures:

- [geo.plot_geo()](/fig/03/geo1.png)
- [geo.plot_cluster()](/fig/03/geo2.png)
- [doc.plot_fig()](/fig/03/fig.pdf)

Rating (54/60):

```
Hodnoceni treti casti projektu: xkalaz00
================================================================================
Geograficka data
--------------------------------------------------------------------------------
+1.00 spravne CRS (5514, 3857) (az 1 b)
+2.00 spravne rozsah (viz FAQ) (az 2 b)
+2.00 pocet radku 571225 > 10 000 (az 2 b)
+2.00 bez NaN v souradnicich (az 2 b)
+3.00 plot_geo: prehlednost, vzhled (az 3 b)
+2.00 plot_geo: zobrazeni ve WebMercator (a ne v S-JTSK) (az 2 b)
+1.00 plot_cluster: prehlednost, vzhled (az 2 b)
+3.00 plot_cluster: clustering (az 3 b)
+1.00 funkce make_geo ma spravne docstring (PEP257) (az 1 b)
+0.50 funkce plot_geo ma spravne docstring (PEP257) (az 0.5 b)
+0.50 funkce plot_cluster ma spravne docstring (PEP257) (az 0.5 b)
+1.00 kvalita kodu dle PEP8 (0 kritickych, 0 E2.., 0 E7..)) (az 1 b)

Overeni hypotezy
--------------------------------------------------------------------------------
+1.00 #1: kontingencni tabulka (az 1 b)
+2.00 #1: vypocet chi2 testu (az 2 b)
+2.00 #1: zaver: dochazi k silnemu ovlivneni (az 2 b)
+0.00 #2 filtrace (az 1 b)
+0.00 #2 vypocet a zaver (az 4 b)

Vlastni analyza
--------------------------------------------------------------------------------
+5.00 tabulka: prehlednost, vzhled (az 5 b)
+4.00 graf: popis, vzhled (az 4 b)
+4.00 graf: vhodna velikost, citelnost (az 4 b)
+2.00 graf: pouziti vektoroveho formatu (az 2 b)
+3.00 textovy popis (az 3 b)
+4.00 statisticka smysluplnost analyzy (az 4 b)
+3.00 dalsi ciselne hodnoty v textu (az 3 b)
+3.00 generovani hodnot skriptem (az 3 b)
+2.00 kvalita kodu dle PEP8 (0 kritickych, 0 E2.., 0 E7..)) (az 2 b)

CELKEM: 54.0 bodu

Komentar k hodnoceni (zejmena k vizualizacim)
================================================================================
cluster: nepopsany cbar
hypo2: nedela se pres kontingencni tabulku!!!
doc: pekne
```
