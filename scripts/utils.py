"""Contains various functions used in diverse places."""


from scripts.constants import *

def get_raster_filename(month):
    """Generates the file path of the requested raster."""

    return SAVE_DIR + "{:02d}.png".format(month)

