"""Contains various functions used in diverse places."""


from scripts.constants import *

def get_raster_filename(month, extension="png"):
    """Generates the file path of the requested raster."""

    return SAVE_DIR + "{:02d}.".format(month) + extension

