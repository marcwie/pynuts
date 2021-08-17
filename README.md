# pynuts
Easy access to NUTS and LAU codes for a given location. 

The main purpose of this package is to provide a simple way to find NUTS and LAU codes as well as the corresponding shapefile for a given point (latitude, longitude) on the surface. The package automatically downloads the necessary input tables and shapefiles from Eurostat's servers. 

For now the packages uses NUTS codes from 2021 and LAU codes from 2020 which is the most recent data at the time of developing this package. In future versions users will be able to select specific years for which updates to NUTS and LAU were made available.

# Installation
Clone this repository and do `python setup.py install`.

# Usage
## Load data
You can load the LAU and NUTS tables like so:
```python
from pynuts import dataio

lau = dataio.load_lau_table(country_code="FR")
nuts = dataio.load_nuts_table(country_code="FR", spatial_resolution=10, level=2)
```
Please see the docstrings for more info on allowed parameter settings.
