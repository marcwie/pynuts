from .dataio import load_nuts_table, load_lau_table, load_correspondence_table
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
    
    for i, region in regions_dataframe.iterrows():
        geometry = region.geometry
        if geometry.contains(shapely_point):
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


class LauFinder():

    def __init__(self, country_code):

        self._lau = load_lau_table(country_code=country_code)
        
        print("Loading fine and coarse NUTS data for hierarchical search.")

        self._nuts_fine = load_nuts_table(country_code=country_code, 
                                          spatial_resolution=1,
                                          level=3)
        self._nuts_coarse = load_nuts_table(country_code=country_code,
                                            spatial_resolution=60,
                                            level=3)

        correspondences = load_correspondence_table(country_code=country_code) 
        correspondences = correspondences[["NUTS 3 CODE", "LAU CODE"]]
        correspondences.rename(columns={"LAU CODE": "LAU_ID", "NUTS 3 CODE": "NUTS3_CODE"}, inplace=True)
       
        self._lau = self._lau.merge(correspondences, on="LAU_ID")


    def find(self, lat, lon):

        # Create a point object
        point = Point(lon, lat)

        # Find the nuts region of the point in coarse resolution or use the 
        # fine resolution if nothing is found
        nuts_region = _find(point, self._nuts_coarse)
        if nuts_region is None:
            nuts_region = _find(point, self._nuts_fine)

        # If the point is still not in any nuts region we stop here
        if nuts_region is None:
            return

        # Otherwise we try to find the lau region of the point within the 
        # detected nuts region
        nuts_id = nuts_region.NUTS_ID
        lau_region_candidates=self._lau[self._lau.NUTS3_CODE==nuts_id]
        lau_region = _find(point, lau_region_candidates)

        # If the point is in any of the nuts regions we return that region
        if lau_region is not None:
            return lau_region

        # Otherwise we try to find the right lau regions again with a fine 
        # resolution
        nuts_region = _find(point, self._nuts_fine)

        # Again, if the point is not in any nuts region we stop here for good
        if nuts_region is None:
            return

        nuts_id = nuts_region.NUTS_ID
        lau_region_candidates=self._lau[self._lau.NUTS3_CODE==nuts_id]
        lau_region = _find(point, lau_region_candidates)

        return lau_region
