# Imports
import glob
import time
from pathlib import Path

from osgeo import gdal
import geopandas as gpd
import rasterio

import geometry as g

# Reprojection warning handling
gdal.PushErrorHandler('CPLQuietErrorHandler')
gdal.UseExceptions()

# Working directories
shapefile_folder = r"D:\LiDAR\Development\building_height_main_2020\out_2020\Total\shp"  # shapefile

# Virtual raster input
vrt_dsm = r"D:\LiDAR\Development\building_height_main_2020\out_2020\Total\madal_2020.vrt"
vrt_dem = r"D:\LiDAR\Development\building_height_main\out_2021\Total\dem_full_2021.vrt"

# Finding shapefiles
working_shp = [shp for shp in glob.glob(fr"{shapefile_folder}\*.shp")]
print(f"Shapefile count: {len(working_shp)}")

# TODO fixi puuuduva kõrgusmudeli kohal (-9999)
# Going over each shp
for ws in working_shp:
    start_time = time.time()
    # Getting filename (map sheet)
    ms = Path(ws).stem
    print(f"Started: {ms}")

    # Reading -> cleaning -> buffering -> centroid
    try:
        gdf = gpd.read_file(ws).pipe(g.drop_nan_percent).pipe(g.generate_buffer).pipe(g.filter_none_geometry).pipe(
            g.get_buf_max, vrt_dsm).pipe(
            g.add_geometry_attributes)
    except ValueError as ve:
        print(f"{ve} - {ms}")
        print("-" * 5)
        continue

    working_coordinates = g.centroid_coordinates(gdf)
    # Dem calculation
    with rasterio.open(vrt_dem) as src:
        gdf['dem_value'] = [x[0] for x in src.sample(working_coordinates)]
    print("\tDone with DEM")

    gdf = g.calculate_building_h(gdf)
    g.write_to_geopackage(gdf, path=r"D:\LiDAR\Development\building_height_main_2020\out_2020\Total\gpkg", file_name=ms)
    print("\tGeopackage written")

    end_time = time.time()
    print(f"Done: {ms} | Time: {end_time - start_time}")
    print("-" * 5)

print("All files done")
