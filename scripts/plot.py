import matplotlib as mpl
import matplotlib.pyplot as plt

from scripts.constants import *
import scripts.color as color
import scripts.utils as utils


# Global variables
plot_map = None


def show_interactive():
    global plot_map
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.25)

    color.create_dummy_for_colorbar()
    plt.colorbar(label="Rainy days", ax=ax)

    ax_slider = fig.add_axes([0.25, 0.1, 0.65, 0.03])
    slider = mpl.widgets.Slider(
        ax=ax_slider,
        label="Month",
        valmin=1,
        valmax=12,
        valstep=list(range(1, 12 + 1)),
        valinit=1,
    )
    slider.on_changed(update)

    plot_map = ax.imshow(load_raster(1), cmap="Greys") # white when empty
    ax.axis("off")
    plt.show()


def load_raster(month):
    try:
        map = plt.imread(utils.get_raster_filename(month))
    except FileNotFoundError:
        map = [[0]]
    return map


def update(month):
    plot_map.set_data(load_raster(month))
    fig.canvas.draw_idle()

