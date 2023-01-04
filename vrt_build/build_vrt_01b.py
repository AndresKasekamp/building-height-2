# Building VRT for DEM
import glob
from osgeo import gdal

# Reprojection warning handling
gdal.PushErrorHandler('CPLQuietErrorHandler')
gdal.UseExceptions()

# Dem folder
dem_folder = r"Z:\Töögrupid\Levi\Reljeef\DEM\2017-2021\DEM_1m_GeoTIFF"  # 1 meter tif

# Output name
vrt_out = r"D:\LiDAR\Development\building_height_main\out_2021\Total\dem_full_2021.vrt"

# Finding tif
working_tif = [tif for tif in glob.glob(fr"{dem_folder}\*.tif")]
print(f"Tif count: {len(working_tif)}")

# Building VRT
gdal.BuildVRT(vrt_out, working_tif)
print("VRT is built")
