"""
sum_difference_iterator.py:
Contains helper function for buy_and_sell_dates.py.
"""

from app import data_bank


def get_sum_differences():
    """
    Helper function that returns sum differences
    for buy_and_sell_dates.py.
    """

    count = 0
    index = 0

    while count < len(data_bank.data):
        lowest = ("buy", data_bank.data[0][0], 1000000000, 0)

        while index < len(data_bank.data):
            if index in data_bank.buy_date_indices:
                index += 1
                continue
            else:
                if data_bank.data[index][1] < lowest[2]:
                    lowest = (
                        "buy",
                        data_bank.data[index][0],
                        data_bank.data[index][1],
                        index
                        )
            index += 1

        index = 0
        highest = ("sell", lowest[1], -1000000000)

        while index < len(data_bank.data):
            if index < lowest[3]:
                index += 1
                continue
            else:
                if data_bank.data[index][1] > highest[2]:
                    highest = (
                        "sell",
                        data_bank.data[index][0],
                        data_bank.data[index][1]
                        )
            index += 1
        data_bank.buy_date_indices.append(count)
        index = 0
        count += 1
        total = highest[2]-lowest[2]
        data_bank.sums.append((lowest, highest, total))

    return data_bank.sums
