# Rainy Days
## Introduction
This app creates renders of the average number of rainy days per month in a given area of interest and over several years of choice. It is based on the [Google Earth Engine](https://earthengine.google.com/) Python API and the [CHIRPS dataset](https://www.chc.ucsb.edu/data/chirps).

## Installation
There are several ways to run this app. They are listed below.

### Online instance of JupyterHub
The simplest way to run this app is to open an online session of Jupyter notebook or JupyterLab and clone this repository in it. For a quick setup and demonstration, follow [this link](https://noto.epfl.ch/hub/user-redirect/git-pull?repo=https://github.com/Soni-Sona/rainy_days.git&urlpath=lab/tree/rainy_days.git/main.ipynb&branch=main).

### Setup a virtualenv (Linux or WSL)
This method can be performed on your local computer and will not affect your current Python installation. Clone this repository
```
$ git clone ...
$ cd rainy-days
```
and initialize a virtual Python environment.
```
$ virtualenv env
$ source env/bin/activate
```
Then, install the required packages with Pip.
```
(env) $ pip install -r requirements.txt
```
Launch an instance of JupyterLab
```
(env) $ jupyter lab
```
and navigate to the file `main.ipynb` to start the app.
If you want to run the app at a later time, do not forget to `source` the virtual environment.

### Install locally
If you do not care about polluting your local Python installation, just make sure to have the following Python packages installed:
- jupyterlab
- earthengine-api
- pyshp
- matplotlib
- ipympl

Clone the repository as usual, spawn a JupyterLab instance and navigate to the `main.ipynb` file. Otherwise, you can also call directly the app functions in a regular Python script (see next section).

## Running
### Typical run
Either launch the `main.ipynb` notebook or run the following lines in a Python script or interpreter:
```
import scripts.app as app

app.load_area_of_interest()
app.check_output_dir()
app.compute_reduced_images(year_start=2017, year_end=2022)
app.generate_rasters(scale=1000)

app.color.set_colormap("Blues")
app.generate_previews(size=512)
```

### Detailed run
The _area of interest_ can be provided as binary shapefiles, that should be placed inside the `data` directory.
12 GeoTIFF rasters can be computed and downloaded to the `rasters` directory:
```
app.compute_reduced_images(year_start, year_end)
app.generate_rasters(scale)
```
where `scale` is given in meters/pixel. A custom reduction algorithm can be written, making use of `app.dataset` and `app.region`, and setting the resulting list of images in `app.reduced_images`.

Preview images can be generated by first defining a colormap via a [Matplotlib name](https://matplotlib.org/stable/tutorials/colors/colormaps.html) using
```
app.color.set_colormap(mpl_name)
```
then calling
```
app.generate_previews(size)
```
where the `size` in pixels is either an integer or a string formated as `"WIDTHxHEIGHT"`.
Finally, the twelve previews can be displayed interactively in a notebook using
```
app.show_interactive_plot()
```

## Troubleshooting
When using a notebook, it is possible that the interactive plot fails to show up. In this case, try to install the `jupyter-matplotlib` extension, either from the Extension Manager interface or using the terminal.

