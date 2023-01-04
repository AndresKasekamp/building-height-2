# Building VRT for DSM
import glob
from osgeo import gdal

# Reprojection warning handling
gdal.PushErrorHandler('CPLQuietErrorHandler')
gdal.UseExceptions()

# Folder read in
tif_folder = r"D:\LiDAR\Development\building_height_main_2019\out_2019\Total\work_tif"

# Output name
vrt_out = r"D:\LiDAR\Development\building_height_main_2019\out_2019\Total\madal_2019.vrt"

# Finding tif
working_tif = [tif for tif in glob.glob(fr"{tif_folder}\*.tif")]
print(f"Tif count: {len(working_tif)}")

# Building VRT
gdal.BuildVRT(vrt_out, working_tif)
print("VRT is built")
