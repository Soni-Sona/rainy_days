import urllib

from scripts.constants import *
import scripts.color as color
import scripts.utils as utils


# Global variables
raster_size = 512


def set_size(size):
    global raster_size
    raster_size = size


def save_rasters(reduced_images):
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

