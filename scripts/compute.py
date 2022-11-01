import ee # earthengine-api


def compute_reduced_images(dataset, year, region):
    reduced_images = []

    for month in range(1, 12 + 1):
        date_start = f"{year}-{month}"
        date_end = f"{year + month // 12}-{month % 12 + 1}"
        # format works even if "2022-1" instead of "2022-01"

        reduced = dataset.filterDate(date_start, date_end)\
                         .map(lambda image: image.gt(0))\
                         .reduce(ee.Reducer.sum())\
                         .clip(region)
        # Note: clipping the entire collection before reducing decreases
        # performance by 10 folds

        reduced_images.append(reduced)

    return reduced_images

