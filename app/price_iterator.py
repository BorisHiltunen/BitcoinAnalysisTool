"""price_iterator.py: Contains one helper function."""

from app.helpers import time_engine
from app import data_bank

timeform = time_engine.TimeForm()


def get_highest_prices(timestamp):
    """Helper function that returns the highest prices as a list"""

    highest = (data_bank.data[0][0], 0.0)
    prices = []
    count = 0

    for price in data_bank.data:

        date = timeform.datetime_object_from_timestamp(timestamp)
        compare_date = timeform.datetime_object_from_timestamp(price[0])

        difference = compare_date - date

        if str(difference)[0] == "1":
            prices.append(highest)
            highest = (data_bank.data[count][0], 0.0)
            timestamp = price[0]
        else:
            if price[1] > highest[1]:
                highest = (price[0], price[1])
        count += 1

    return prices
