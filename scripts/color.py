"""Provides functions regarding colormaps and palettes."""


import matplotlib as mpl
import matplotlib.pyplot as plt

from scripts.constants import *


# Global variables
colormap = None
palette  = []


def set_colormap(mpl_name):
    """Sets a colormap and a palette in memory.

    The colormap serves the creation of the color palette used in the
    generation of rasters and the interactive plot.
    The chosen colormap is shown and saved in the output directory.

    Args:
        mpl_name (str): Name of the colormap from the Matplotlib list:
            https://matplotlib.org/stable/tutorials/colors/colormaps.html.
    """

    global colormap, palette
    colormap = mpl.cm.get_cmap(mpl_name, COLOR_MAX - COLOR_MIN + 1)
    palette = [mpl.colors.rgb2hex(colormap(i)) for i in range(colormap.N)]
    preview_colormap()


def preview_colormap():
    """Shows and saves the chosen colormap."""

    plt.figure(figsize=(5,1))
    plt.gca().set_visible(False)

    create_dummy_for_colorbar()
    ax = plt.axes([0.1, 0.5, 0.8, 0.3])
    plt.colorbar(orientation="horizontal", label="Rainy days", cax=ax)

    plt.savefig(f"{SAVE_DIR}colormap.png", bbox_inches="tight")
    plt.show()


def create_dummy_for_colorbar():
    """Creates an invisible plot to attach a colorbar."""

    dummy = plt.imshow([[COLOR_MIN - 0.5, COLOR_MAX + 0.5]], cmap=colormap)
    dummy.set_visible(False)

