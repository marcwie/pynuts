# pynuts

Easy access to NUTS and LAU codes for a given location. 

The package provides a quick way to find NUTS and LAU codes (and some additional information) for a given point (latitude, longitude) on the surface. The package automatically downloads the necessary input tables and shapefiles from Eurostat's servers. 

The package uses NUTS codes from 2016 and LAU codes from 2019 which is currently the most recent data. Future versions will enable users to select specific years for which updates to NUTS and LAU are available.

**Note:** This package has been developed and tested using Linux. Your mileage on Windows and MacOS may vary.

# Usage

## Installation
Clone this repository and do `python setup.py install`.

## Load data
If you only wish to obtain the official LAU and NUTS tables you can achieve this like so:
```python
from pynuts import dataio

lau = dataio.load_lau_table(country_code="FR")
nuts = dataio.load_nuts_table(country_code="FR", spatial_resolution=10, level=2)
```
You need to specify a two-character country-code. For NUTS-tables you also need to specify the desired resolution (1, 3, 10, 20, 60 -- the lower the better) and the NUTS level (1, 2, or 3 -- the higher the finer).

## Find NUTS-region corresponding to a specific location
Let's assume you know the latitude and longitude of your location (for instance in Italy). You can then obtain the corresponding NUTS1 regions like so:
```python
from pynuts import NutsFinder

finder = NutsFinder(country_code="IT", spatial_resolution=60, level=1)
region = finder.find(lat=42.61923574439346, lon=13.010336619663239)
print("Point lies in NUTS1-Region", region.NUTS_NAME, "with ID", region.NUTS_ID)
```
which prints
```
Loading LEVEL1 NUTS data from 2021 for IT at 60m spatial resolution
Point lies in NUTS1-Region Centro (IT) with ID ITI
```
Similarly, you could do the same for NUTS2- and NUTS3-regions:
```python
from pynuts import NutsFinder

finder = NutsFinder(country_code="IT", spatial_resolution=60, level=2)
region = finder.find(lat=42.61923574439346, lon=13.010336619663239)
print("Point lies in NUTS2-Region", region.NUTS_NAME, "with ID", region.NUTS_ID, end="\n\n")

finder = NutsFinder(country_code="IT", spatial_resolution=60, level=3)
region = finder.find(lat=42.61923574439346, lon=13.010336619663239)
print("Point lies in NUTS3-Region", region.NUTS_NAME, "with ID", region.NUTS_ID)
```
which prints
```
Loading LEVEL2 NUTS data from 2021 for IT at 60m spatial resolution
Point lies in NUTS2-Region Lazio with ID ITI4

Loading LEVEL3 NUTS data from 2021 for IT at 60m spatial resolution
Point lies in NUTS3-Region Rieti with ID ITI42
```

## Find LAU-region corresponding to a specific location
You can do the same now for LAU-regions which is a very fine grained tessalation of countries. 


