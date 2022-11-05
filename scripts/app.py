"""Initializes the app and provides front-end functions.

This module loads the Google Earth Engine API, which asks for an
authentication. Follow the instructions in the provided link when
loading the module. After initialization, the CHIRPS dataset is loaded.
An area of interest must be imported before generating the rasters.
Finally, the rasters can be visualized interactively in a Jupyter notebook.

Example of usage (in jupyterlab):

    import scripts.app as app
    %matplotlib widget

    app.load_area_of_interest()
    app.check_output_dir()
    app.compute_reduced_images(year=2021)
    app.generate_rasters(scale=1000)

    app.color.set_colormap("Blues")
    app.generate_previews(size=512)
    app.show_interactive_plot()
"""


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
reduced_images = []


# Initialize
ee.Authenticate()
ee.Initialize()
dataset = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")


def load_area_of_interest():
    """Loads the binary shapefile in memory.

    The shapefile is loaded from the path contained in
    scripts.constants.AREA_OF_INTEREST_PATH. The resulting Geometry is
    stored in the region variable.
    """

    global region
    shape = shapefile.Reader(AREA_OF_INTEREST_PATH)
    # Take first feature of the shapefile
    feature = shape.shapeRecords()[0]
    region = ee.Geometry(feature.shape.__geo_interface__)
    print("Area of interest successfully loaded.")


def check_output_dir():
    """Checks that the output directory is empty or creates it.

    The output directory path is given by scripts.constants.SAVE_DIR.
    If the directory already contains .png files, a warning is printed.
    """

    system(f"mkdir {SAVE_DIR} 2> /dev/null")
    # quiet: no complain if directory already exists

    current_files = [f for f in listdir(SAVE_DIR) if ".png" in f]
    if len(current_files) > 0:
        print(f"Warning: \"{SAVE_DIR}\" may contain previously rendered "\
              +"rasters. They will be overwritten.")
    else:
        print(f"Output directory \"{SAVE_DIR}\" is ready.")


def set_colormap(mpl_name):
    """Alias for scripts.color.set_colormap."""

    color.set_colormap(mpl_name)


def compute_reduced_images(year_start, year_end):
    """Computes reduced images for the given year."""

    global reduced_images
    reduced_images = compute.compute_reduced_images(dataset, year_start, year_end, region)


def generate_previews(size):
    """Alias for scripts.raster.generate_png."""

    raster.generate_png(reduced_images, size)


def generate_rasters(scale):
    """Alias for scripts.raster.generate_tif."""

    raster.generate_tif(reduced_images, scale)


def show_interactive_plot():
    """Alias for scripts.plot.show_interactive."""

    plot.show_interactive()

