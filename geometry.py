from geopandas.geodataframe import GeoDataFrame
from rasterstats import zonal_stats
import numpy as np


def drop_nan_percent(gdf: GeoDataFrame) -> GeoDataFrame:
    """ Dropping nan Protsent values (cannot be used for analysis)

    :param gdf: working df
    :return: modified gdf (percent removed)
    """
    gdf = gdf.drop(gdf[gdf['Protsent'].isnull()].index)
    gdf.reset_index(drop=True, inplace=True)
    print("\tPercent dropped")

    return gdf


def add_geometry_attributes(gdf: GeoDataFrame) -> GeoDataFrame:
    """ Adding geometry attributes to building dataframe

    :param gdf: gdf to use
    :return: modified gdf (geometry added)
    """
    # Adding geometry attributes
    representative_point = gdf.representative_point()  # representative point

    # Adding columns to dataframe
    gdf['X'] = representative_point.x
    gdf['Y'] = representative_point.y
    print("\tGeometry attributes added")

    return gdf


def centroid_coordinates(gdf: GeoDataFrame) -> list[tuple[float, float]]:
    """ Detecting centroid coordinates to a workable data structure

    :param gdf: working gdf
    """
    # Flipping coordinates due
    coord_list = [(x, y) for x, y in zip(gdf['X'], gdf['Y'])]
    print("\tCentroid coordinate list done")
    return coord_list


def calculate_building_h(gdf: GeoDataFrame) -> GeoDataFrame:
    """ Calculating building h

    :param gdf: working gdf
    :return: modified gdf (building h added)
    """
    # Rounding an converting to int
    gdf['building_h'] = gdf['dsm_value'] - gdf['dem_value']
    print("\tBuilding H calculated")
    return gdf


def write_to_geopackage(gdf: GeoDataFrame, path: str, file_name: str) -> None:
    """ Writing file to geopackage, won't use layer name

    :param gdf: working gdf
    :param path: directory path for output
    :param file_name: output name for file
    """
    gdf.to_file(fr"{path}\{file_name}.gpkg", driver="GPKG")
    print("\tWrite to gpkg done")


def generate_buffer(gdf: GeoDataFrame) -> GeoDataFrame:
    """ Generating negative buffer around building

    :param gdf: working gdf
    :return: gdf with geometry modified
    """
    gdf['geometry'] = gdf.geometry.buffer(-0.75)
    print("\tGeometry calculated")
    return gdf


def filter_none_geometry(gdf: GeoDataFrame) -> GeoDataFrame:
    """ Removing empty geometries due to buffer creation (weird elongated shapes)

    :param gdf: empty geometries gdf
    :return: gdf with geometry modified
    """
    gdf = gdf[~gdf.is_empty]
    print("\tNone geometries removed")
    return gdf


def get_buf_max(gdf: GeoDataFrame, working_tif: str) -> GeoDataFrame:
    """ Calculating zonal stats (max) for buildings in map sheet

    :param gdf: working gdf
    :param working_tif: corresponding raster file
    :return: modified gdf
    """
    zs_rslt = zonal_stats(gdf, working_tif, stats="max", band=1)
    zs_rslt = [mz['max'] for mz in zs_rslt]
    gdf['dsm_value'] = zs_rslt
    print("\tMaximum z value within buffer done")
    return gdf


def get_eave_height(gdf: GeoDataFrame) -> GeoDataFrame:
    gdf['abs_eave_h'] = (gdf['geometry'].apply(lambda geom: np.max([coord[2] for coord in geom.coords])))
    return gdf