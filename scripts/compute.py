"""Contains the data reduction logic."""


import ee # earthengine-api


def compute_reduced_images(dataset, year_start, year_end, region):
    """Computes a set of 12 images for the given parameters.

    Returns a list of 12 ee.Image, one for each month, containing the
    average number of rainy days recorded each month between year_start
    (included) and year_end (excluded).

    Args:
        dataset (ee.ImageCollection): Unfiltered dataset.
        year_start (int): Only keep data after the start of this year.
        year_end (int): Only keep data before this year.
        region (ee.geometry): The area of interest. The images are clipped
            to this region.

    Returns:
        A list of 12 ee.Image.
    """

    if year_end <= year_start:
        print("year_end must be greater than year_start." )
        return


    reduced_images = []

    for month in range(1, 12 + 1):
        print(f"{month - 1}/12", end="\r")

        # First, make a list of one image per year containing the number
        # of rainy days for the current month
        yearly_images = [] # for this month

        for year in range(year_start, year_end):
            date_start = f"{year}-{month}"
            date_end = f"{year + month // 12}-{month % 12 + 1}"
            # format works even if "2022-1" instead of "2022-01"

            # To reduce one month of daily measurements, each daily image
            # is first mapped to an image containing "1"s wherever the recorded
            # rain volume is greater than 0. Then, the images are summed
            # together to obtain the number of rainy days in the month.
            one_month = dataset.filterDate(date_start, date_end)\
                               .map(lambda image: image.gt(0))\
                               .reduce(ee.Reducer.sum())

            # Check that data is present
            if len(one_month.bandNames().getInfo()) == 0: # no data
                print("Error: no data for the month " + date_start)
                return []

            yearly_images.append(one_month)

        # The list is then averaged to get a single image for the current
        # month
        collection = ee.ImageCollection(yearly_images)
        reduced = collection.reduce(ee.Reducer.mean())\
                            .round()\
                            .clip(region)

        reduced_images.append(reduced)

    print("Done.")
    return reduced_images

