# pynuts

Easy access to NUTS and LAU codes for a given location. 

The package provides a quick way to find NUTS and LAU codes (and some additional information) for a given point (latitude, longitude) on the surface. The package automatically downloads the necessary input tables and shapefiles from Eurostat's servers. 

The package uses NUTS codes from 2021 and LAU codes from 2020 which is currently the most recent data. Future versions will enable users to select specific years for which updates to NUTS and LAU are available.

**Note:** This package has been developed and tested using Linux. Your mileage on Windows and MacOS may vary.

# Usage

## Installation
Clone this repository and do `python setup.py install`.

## Load data
You can load the LAU and NUTS tables like so:
```python
from pynuts import dataio

lau = dataio.load_lau_table(country_code="FR")
nuts = dataio.load_nuts_table(country_code="FR", spatial_resolution=10, level=2)
```
Please see the docstrings for more info on allowed parameter settings.
