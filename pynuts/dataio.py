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
