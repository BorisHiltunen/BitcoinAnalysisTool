"""price_iterator.py: Contains one helper function."""

from app import data_bank


def get_highest_prices(timestamp):
    """Helper function that returns the highest prices as a list."""

    highest = (data_bank.data[0][0], 0.0)
    prices = []
    count = 0

    for price in data_bank.data:
        if price[0] - timestamp == 86400:
            prices.append(highest)
            highest = (data_bank.data[count][0], 0.0)
            timestamp = price[0]
        else:
            if price[1] > highest[1]:
                highest = (price[0], price[1])
        count += 1

    return prices
