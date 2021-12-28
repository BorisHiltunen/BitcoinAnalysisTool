"""price_iterator.py: Contains one helper function."""

import __init__


def get_highest_prices(timestamp):
    """Helper function that returns the highest prices as a list."""

    highest = (__init__.data[0][0], 0.0)
    prices = []
    count = 0

    for price in __init__.data:
        if price[0] - timestamp == 86400:
            prices.append(highest)
            highest = (__init__.data[count][0], 0.0)
            timestamp = price[0]
        else:
            if price[1] > highest[1]:
                highest = (price[0], price[1])
        count += 1

    return prices
