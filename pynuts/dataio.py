import os
from pathlib import Path
import zipfile
import geopandas
import wget

# Create data directory in user home
HOME = os.path.expanduser("~")
DATA_DIRECTORY = HOME + "/.pynuts/"
Path(DATA_DIRECTORY).mkdir(parents=True, exist_ok=True) 

# Path to the server that holds the LAU and NUTS shapefiles
SERVER = "https://gisco-services.ec.europa.eu/distribution/v2/"

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
    print("Loading LAU data from 2020") 
    
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
    lau = geopandas.read_file(DATA_DIRECTORY+file_name[:-4]+"/"+shapefile)
    lau = lau[lau["CNTR_CODE"] == country_code]

    return lau


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
    print("Loading NUTS data from 2021") 
    
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
