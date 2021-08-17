import os
from pathlib import Path
import zipfile
import geopandas
import wget
import pandas as pd

# Create data directory in user home
HOME = os.path.expanduser("~")
DATA_DIRECTORY = HOME + "/.pynuts/"
Path(DATA_DIRECTORY).mkdir(parents=True, exist_ok=True) 

# Path to the server that holds the LAU and NUTS shapefiles
SERVER = "https://gisco-services.ec.europa.eu/distribution/v2/"

# Path to the correspondence table on the server
CORRESPONDENCE_TABLE = "https://ec.europa.eu/eurostat/documents/345175/501971/EU-27-LAU-2020-NUTS-2021-NUTS-2016.xlsx"


def load_lau_table(country_code):
    """
    Load a pandas data frame of LAU codes.

    Args:
        country_code: A two digit country code (str)

    Returns:
        Pandas data frame with all LAU districts in the specified country.

    Loads the data from the Eurostat server into pynuts' config folder and
    stores it there for later use.
    """
    print(f"Loading LAU data from 2020 for {country_code}") 
    
    # TODO: Let users choose year and version in the future
    path = "lau/download/"
    file_name = "ref-lau-2020-01m.shp.zip"
    shapefile = "LAU_RG_01M_2020_4326.shp.zip"

    # Download the data
    if not os.path.exists(DATA_DIRECTORY+file_name):                              
        wget.download(SERVER+path+file_name, DATA_DIRECTORY+file_name)
  
    # Unzip the data
    if not os.path.exists(DATA_DIRECTORY+file_name[:-4]):
        with zipfile.ZipFile(DATA_DIRECTORY+file_name, 'r') as zip_ref:
            zip_ref.extractall(DATA_DIRECTORY+file_name[:-4])
   
    # Load data into pandas dataframe and filter for specified country
    df = geopandas.read_file(DATA_DIRECTORY+file_name[:-4]+"/"+shapefile)
    df = df[df["CNTR_CODE"] == country_code]

    return df


def load_nuts_table(country_code, spatial_resolution, level):
    """
    Load a pandas data frame of nuts codes.

    Args:
        country_code: A two digit country code (str)
        spatial_resolution: The accuracy of the shapefiles (int)
        level: The nuts level (int)

    Returns:
        Pandas data frame with all NUTS regions in the specified country.

    Loads the data from the Eurostat server into pynuts' config folder and
    stores it there for later use.

    The spatial resolution can either of five values: 1, 3, 10, 20 or 60.
    Higher values mean coarser resolution.

    The level can take either of three valuess: 1,2 or 3. They translate into
    - NUTS 1: major socio-economic regions
    - NUTS 2: basic regions for the application of regional policies
    - NUTS 3: small regions for specific diagnoses
    """
    print(f"Loading LEVEL{level} NUTS data from 2021 for {country_code} at " \
          f"{spatial_resolution}m spatial resolution") 
    
    if spatial_resolution not in [1, 3, 10, 20, 60]:
        print("spatial_resolution must be either 1, 3, 10, 20 or 60.")
        return

    if level not in [1, 2, 3]:
        print("level must be either 1, 2 or 3.")
        return

    spatial_resolution = str(spatial_resolution).zfill(2)

    # TODO: Let users choose year and version in the future
    path = "nuts/download/"
    file_name = f"ref-nuts-2021-{spatial_resolution}m.shp.zip"
    shapefile = f"NUTS_RG_{spatial_resolution}M_2021_4326_LEVL_{level}.shp.zip"

    # Download the data
    if not os.path.exists(DATA_DIRECTORY+file_name):                              
        wget.download(SERVER+path+file_name, DATA_DIRECTORY+file_name)
  
    # Unzip the data
    if not os.path.exists(DATA_DIRECTORY+file_name[:-4]):
        with zipfile.ZipFile(DATA_DIRECTORY+file_name, 'r') as zip_ref:
            zip_ref.extractall(DATA_DIRECTORY+file_name[:-4])
   
    # Load data into pandas dataframe and filter for specified country
    df = geopandas.read_file(DATA_DIRECTORY+file_name[:-4]+"/"+shapefile)
    df = df[df["CNTR_CODE"] == country_code]

    return df


def load_correspondence_table(country_code):
    """
    Load the correspondence table that provides a mapping between NUTS and LAU.

    Args:
        country_code: The two digit country code (str)

    Returns:
        pandas.DataFrame containing the correspondence table for the specified
        country.

    Loads the data from the Eurostat server into pynuts' config folder and
    stores it there for later use.
    """
    print(f"Loading correspondence table for {country_code}")
    file_name = CORRESPONDENCE_TABLE.split("/")[-1]

    # Download the data
    if not os.path.exists(DATA_DIRECTORY+file_name):                              
        wget.download(CORRESPONDENCE_TABLE, DATA_DIRECTORY+file_name)
  
    df = pd.read_excel(DATA_DIRECTORY+file_name, sheet_name=country_code, 
                       dtype="object")

    return df
