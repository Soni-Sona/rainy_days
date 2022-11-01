"""Contains the data reduction logic."""


import ee # earthengine-api


def compute_reduced_images(dataset, year, region):
    """Computes a set of 12 images for the given parameters.

    For the provided year, this function returns a list of 12 ee.Image,
    one for each month, containing the number of rainy days recorded each
    month.

    Args:
        dataset (ee.ImageCollection): Unfiltered dataset.
        year (int): The year of interest.
        region (ee.geometry): The area of interest. The images are clipped
            to this region.

    Returns:
        A list of 12 ee.Image.
    """

    reduced_images = []

    for month in range(1, 12 + 1):
        date_start = f"{year}-{month}"
        date_end = f"{year + month // 12}-{month % 12 + 1}"
        # format works even if "2022-1" instead of "2022-01"

        # To reduce one month of daily measurements, each daily image
        # is first mapped to an image containing "1"s wherever the recorded
        # rain volume is greater than 0. Then, the images are summed
        # together to obtain the number of rainy day in the month.
        reduced = dataset.filterDate(date_start, date_end)\
                         .map(lambda image: image.gt(0))\
                         .reduce(ee.Reducer.sum())\
                         .clip(region)
        # Note: clipping the entire collection before reducing decreases
        # performance by 10 folds

        reduced_images.append(reduced)

    return reduced_images

