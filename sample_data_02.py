# Imports
import glob
from pathlib import Path

from osgeo import gdal
import geopandas as gpd
import rasterio


import geometry as g

# TODO kui arendus valmis saab, siis pipeda
# TODO kas on vaja geom ka ümber arvutada
# TODO ilmselt on vaja luua ka virtual raster tiffide põhjal
# TODO peaksid ilmselt uurima anari skripti, et selgitada välja kuidas originaalset demi kätte saada
# TODO proovi Protsent=0 ja tühi vms
# TODO inside buffer ja seejärel küsida maja kõrgus? (ühesõnaga vältida võimalust, et ta satub piiri peale?

# Reprojection warning handling
gdal.PushErrorHandler('CPLQuietErrorHandler')
gdal.UseExceptions()

# Working directories
shapefile_folder = r"D:\LiDAR\Development\building_height_main\out_2021\Total\shp_3"  # shapefile
tif_folder = r"D:\LiDAR\Development\building_height_main\out_2021\Total\tif"  # dsm

# Virtual raster input
vrt_dsm = r"D:\LiDAR\Development\building_height_main\out_2021\Total\madal_2021.vrt"
# vrt_dsm = r"D:\LiDAR\Development\building_height_main\out_2021\Total\foo.vrt"
vrt_dem = r"D:\LiDAR\Development\building_height_main\out_2021\Total\dem_full_2021.vrt"

# Finding shapefiles
working_shp = [shp for shp in glob.glob(fr"{shapefile_folder}\*.shp")]
print(f"Shapefile count: {len(working_shp)}")

# Going over each shp
for ws in working_shp:
    # Getting filename (map sheet)
    ms = Path(ws).stem
    print(f"Started: {ms}")

    # Reading -> cleaning -> buffering -> centroid
    gdf = gpd.read_file(ws).pipe(g.drop_nan_percent).pipe(g.generate_buffer).pipe(g.get_buf_max, vrt_dsm).pipe(
        g.add_geometry_attributes)
    working_coordinates = g.centroid_coordinates(gdf)
    # Dem calculation
    with rasterio.open(vrt_dem) as src:
        gdf['dem_value'] = [x[0] for x in src.sample(working_coordinates)]
    print("\tDone with DEM")

    gdf = g.calculate_building_h(gdf)
    g.write_to_geopackage(gdf, ms)
    print("\tGeopackage written")

    print(f"Done: {ms}")
    print("-" * 5)

print("All files done")


