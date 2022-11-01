"""Functions for exporting rasters."""


import urllib

from scripts.constants import *
import scripts.color as color
import scripts.utils as utils


# Global variables
raster_size = 512


def set_size(size):
    """Defines the size of the future rasters to be exported.

    Maximum dimensions of the images to render, in pixels. If only one
    number is passed, it is used as the maximum, and the other dimension
    is computed by proportional scaling.

    Args:
        size (int or str): A number or pair of numbers in format WIDTHxHEIGHT.
    """

    global raster_size
    raster_size = size


def save_rasters(reduced_images):
    """Generates images from the reduced dataset and saves them.

    Asks the Earth Engine API to generate png images, which are handed
    over via an url. The images are retrieved from the url and saved.

    Args:
        reduced_images (list of 12 ee.Image): Output from
            scripts.compute.compute_reduced_images.
    """

    for i in range(12):
        image = reduced_images[i]
        filename = utils.get_raster_filename(i + 1)

        if len(image.bandNames().getInfo()) == 0: # no data
            system(f"rm {filename} 2> /dev/null") # quiet rm

        else:
            print(f"{i}/12", end="\r")
            url = image.getThumbURL({
                'min': COLOR_MIN,
                'max': COLOR_MAX,
                'palette': color.palette,
                'dimensions': raster_size,
                'format': "png"
            })
            urllib.request.urlretrieve(url, filename)

    print("Done.")

