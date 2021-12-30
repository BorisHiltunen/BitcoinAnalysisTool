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

    both = {"buy_date": 1000000000, "sell_date": -1000000000, "profit": -1000000000}
    sums = []
    count = 0


    while count < len(data_bank.data):

        if data_bank.data[count][1] < both["buy_date"]:
            both["buy_date"] = data_bank.data[count][1]
            sums.append(both)
            both = {"buy_date": 1000000000, "sell_date": -1000000000, "profit": -1000000000}
        if data_bank.data[count][1] < both["sell_date"]:
            both["buy_date"] = data_bank.data[count][1]

    return data_bank.sums
#Not ready yet