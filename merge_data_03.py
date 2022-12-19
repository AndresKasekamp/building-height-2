# Merging multiple gpkg into one
# Imports
import glob

import pandas as pd
import geopandas as gpd

import geometry as g

# TODO kas arcpy-ga on võimalik natiivselt gpkg lugeda
# Finding GPKG
gpkg_folder = r"D:\LiDAR\Development\building_height_main\out_2021\Total\test_gpkg"

original_shp = r"D:\LiDAR\Development\building_height_main\ETAK_hooned\E_401_hoone_ka.shp"

# Finding gpkg
working_gpkg = [gpkg for gpkg in glob.glob(fr"{gpkg_folder}\*.gpkg")]
# print(f"GPKG count: {len(working_gpkg)}")

etak_gdf = gpd.read_file(original_shp)
print("Etak read in done")

for wg in working_gpkg:
    ms_gdf = gpd.read_file(wg)
    etak_gdf = etak_gdf.merge(ms_gdf, on='etak_id')
    print("Merge done")

g.write_to_geopackage(etak_gdf, path=r"D:\LiDAR\Development\building_height_main_2020\out_2020\Total\gpkg", file_name="etak_merge")

# # Concat code, could be useful
# # Concating shapefiles into singular geodataframe - for about 3000 shapefiles takes about 15 minutes
# gdf = gpd.GeoDataFrame(pd.concat([gpd.read_file(i) for i in working_gpkg],
#                                  ignore_index=True), crs=gpd.read_file(working_gpkg[0]).crs)
#
# g.write_to_geopackage(gdf, "h_merge")

