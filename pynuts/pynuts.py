from .dataio import load_nuts_table 
from shapely.geometry import Point


def _find(shapely_point, regions_dataframe):
    """
    Find the regions that contains a Point.

    Args:
        shapely_point: A shapely.geometry.Point instance that holds the
        position in longitude and latitude
        regions_dataframe: pandas.DataFrame containing a NUTS or LAU table.
    
    Returns:
        The row of the dataframe of the region that contains the point. None if
        no region is found.
    """
    
    for i, region in regions.iterrows():
        poly = region.geometry
        if poly.contains(point):
            return region
    else:
        return None


class NutsFinder():

    def __init__(self, country_code, level=3, spatial_resolution=60):

        self._nuts = load_nuts_table(country_code=country_code,
                                     spatial_resolution=spatial_resolution,
                                     level=level)

    def find(self, lat, lon):

        point = Point(lon, lat)
        region = _find(point, self._nuts)
        
        if region is None:
            print(f"No NUTS id found for lat={lat}, lon={lon}")

        return region
