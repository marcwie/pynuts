import os
from pathlib import Path
import zipfile
import geopandas
import wget

HOME = os.path.expanduser("~")
DATA_DIRECTORY = HOME + "/.pynuts/"
Path(DATA_DIRECTORY).mkdir(parents=True, exist_ok=True) 

SERVER = "https://gisco-services.ec.europa.eu/distribution/v2/"

def load_lau_table(country_code):
   
    print("Loading LAU data from 2020") 
    
    # TODO: Let users choose year and version in the future
    path = "lau/download/"
    file_name = "ref-lau-2020-01m.shp.zip"
    shapefile = "LAU_RG_01M_2020_4326.shp.zip"

    if not os.path.exists(DATA_DIRECTORY+file_name):                              
        wget.download(SERVER+path+file_name, DATA_DIRECTORY+file_name)
   
    if not os.path.exists(DATA_DIRECTORY+file_name[:-4]):
        with zipfile.ZipFile(DATA_DIRECTORY+file_name, 'r') as zip_ref:
            zip_ref.extractall(DATA_DIRECTORY+file_name[:-4])
    
    lau = geopandas.read_file(DATA_DIRECTORY+file_name[:-4]+"/"+shapefile)
    lau = lau[lau["CNTR_CODE"] == country_code]

    return lau
