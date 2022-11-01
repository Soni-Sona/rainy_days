import matplotlib as mpl
import matplotlib.pyplot as plt

from scripts.constants import *


# Global variables
colormap = None
palette  = []


def set_colormap(mpl_name):
    global colormap, palette
    # https://matplotlib.org/stable/tutorials/colors/colormaps.html
    colormap = mpl.cm.get_cmap(mpl_name, COLOR_MAX - COLOR_MIN + 1)
    palette = [mpl.colors.rgb2hex(colormap(i)) for i in range(colormap.N)]
    preview_colormap()


def preview_colormap():
    plt.figure(figsize=(5,1))
    plt.gca().set_visible(False)

    #add_colorbar(ax, horizontal=True)
    create_dummy_for_colorbar()
    ax = plt.axes([0.1, 0.5, 0.8, 0.3])
    plt.colorbar(orientation="horizontal", label="Rainy days", cax=ax)

    plt.savefig(f"{SAVE_DIR}colormap.png", bbox_inches="tight")
    plt.show()


def create_dummy_for_colorbar():
    dummy = plt.imshow([[COLOR_MIN - 0.5, COLOR_MAX + 0.5]], cmap=colormap)
    dummy.set_visible(False)

