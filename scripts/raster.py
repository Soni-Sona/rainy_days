"""Functions for exporting rasters."""


import urllib

from scripts.constants import *
import scripts.color as color
import scripts.utils as utils


def generate_png(reduced_images, size):
    """Generates previews from the reduced dataset and saves them.

    Asks the Earth Engine API to generate png images, which are handed
    over via an url. The images are retrieved from the url and saved.
    As the generation of previews takes time, the current progression is
    printed.

    Args:
        reduced_images (list of 12 ee.Image): Output from
            scripts.compute.compute_reduced_images.
        size (int or str): One number or pair of numbers in format
            WIDTHxHEIGHT, in pixels.
    """

    generate_image_template(
        reduced_images,
        "png",
        lambda image:
            image.getThumbURL({
                'min': COLOR_MIN,
                'max': COLOR_MAX,
                'palette': color.palette,
                'dimensions': size,
                'format': "png"
            })
    )


def generate_tif(reduced_images, scale):
    """Generates GeoTIFFs from the reduced dataset and saves them.

    Asks the Earth Engine API to generate GeoTIFFs rasters, which are
    handed over via an url. The images are retrieved from the url and
    saved. As the generation of rasters takes time, the current
    progression is printed.

    Args:
        reduced_images (list of 12 ee.Image): Output from
            scripts.compute.compute_reduced_images.
        scale (float): Scale in meters/pixel.
    """

    generate_image_template(
        reduced_images,
        "tif",
        lambda image:
            image.getDownloadURL({
                'scale': scale,
                'format': "GEO_TIFF"
            })
    )


def generate_image_template(reduced_images, extension, get_url_func):
    """Template function for generate_png and generate_tif.

    Args:
        reduced_images (list of 12 ee.Image): Output from
            scripts.compute.compute_reduced_images.
        extension (str): Extension for saving, ex: "png"
        get_url_func (function): Gives url from ee.Image.
    """

    for i in range(12):
        image = reduced_images[i]
        filename = utils.get_raster_filename(i + 1, extension)

        print(f"{i}/12", end="\r")
        url = get_url_func(image)
        urllib.request.urlretrieve(url, filename)

    print("Done.")

