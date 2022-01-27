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

    both = {
        "buy_price": (0.0, 1000000000.0),
        "sell_price": (0.0, -1000000000.0),
        "profit": -1000000000.0
        }
    data_bank.sums = []
    count = 0

    while count < len(data_bank.data):
        if count == len(data_bank.data)-1 and \
                both["sell_price"][0] > both["buy_price"][0]:
            if data_bank.data[count][1] > both["sell_price"][1]:
                both["sell_price"] = (
                    data_bank.data[count][0],
                    data_bank.data[count][1]
                    )
                both["profit"] = both["sell_price"][1] - \
                    both["buy_price"][1]
                data_bank.sums.append(both)
            else:
                both["profit"] = both["sell_price"][1] - \
                    both["buy_price"][1]
                data_bank.sums.append(both)
        else:
            if data_bank.data[count][1] < both["buy_price"][1]:
                if count > 0:
                    both["profit"] = both["sell_price"][1] - \
                        both["buy_price"][1]
                    data_bank.sums.append(both)
                    both = {
                        "buy_price": (0.0, 1000000000.0),
                        "sell_price": (0.0, -1000000000.0),
                        "profit": -1000000000.0
                        }
                    both["buy_price"] = (
                        data_bank.data[count][0],
                        data_bank.data[count][1]
                        )
                else:
                    both["buy_price"] = (
                        data_bank.data[count][0],
                        data_bank.data[count][1]
                        )
            if data_bank.data[count][1] > both["sell_price"][1] and \
                    data_bank.data[count][0] >= both["buy_price"][0]:
                both["sell_price"] = (
                    data_bank.data[count][0],
                    data_bank.data[count][1]
                    )
        count += 1

    return data_bank.sums
