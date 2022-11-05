"""Functions for exporting rasters."""


import urllib

from scripts.constants import *
import scripts.color as color
import scripts.utils as utils


def generate_png(reduced_images, size):
    """Generates images from the reduced dataset and saves them.

    Asks the Earth Engine API to generate png images, which are handed
    over via an url. The images are retrieved from the url and saved.
    As the generation of rasters takes time, the current progression is
    printed.

    Args:
        reduced_images (list of 12 ee.Image): Output from
            scripts.compute.compute_reduced_images.
        size (int or str): One number or pair of numbers in format
            WIDTHxHEIGHT, in pixels.
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
                'dimensions': size,
                'format': "png"
            })
            urllib.request.urlretrieve(url, filename)

    print("Done.")

