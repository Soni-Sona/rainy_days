import ee # earthengine-api
import shapefile # pyshp
from os import system, listdir

from scripts.constants import *
import scripts.color   as color
import scripts.compute as compute
import scripts.raster  as raster
import scripts.plot    as plot


# Global variables
dataset = None
region  = None


# Initialize
ee.Authenticate()
ee.Initialize()
dataset = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")


def load_area_of_interest():
    global region
    shape = shapefile.Reader(AREA_OF_INTEREST_PATH)
    # Take first feature of the shapefile
    feature = shape.shapeRecords()[0]
    region = ee.Geometry(feature.shape.__geo_interface__)
    print("Area of interest successfully loaded.")


def check_output_dir():
    system(f"mkdir {SAVE_DIR} 2> /dev/null")
    # quiet: no complain if directory already exists

    current_files = [f for f in listdir(SAVE_DIR) if ".png" in f]
    if len(current_files) > 0:
        print(f"Warning: \"{SAVE_DIR}\" may contain previously rendered "\
              +"rasters. They will be overwritten.")
    else:
        print(f"Output directory \"{SAVE_DIR}\" is ready.")


def set_colormap(mpl_name):
    color.set_colormap(mpl_name)


def set_raster_size(size):
    raster.set_size(size)


def generate_rasters(year):
    reduced_images = compute.compute_reduced_images(dataset, year, region)
    raster.save_rasters(reduced_images)


def show_interactive_plot():
    plot.show_interactive()

