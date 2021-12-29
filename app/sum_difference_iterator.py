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

    if data_bank.under_90_days or data_bank.one_day:
        count = 0

        lowest = ("buy", data_bank.data[0][0], 1000000000, 0)

        while count < len(data_bank.data):
            if count in data_bank.buy_date_indices:
                count += 1
                continue
            else:
                if data_bank.data[count][1] < lowest[2]:
                    lowest = (
                        "buy",
                        data_bank.data[count][0],
                        data_bank.data[count][1],
                        count
                        )
            count += 1

        data_bank.buy_date_indices.append(lowest[3])

        count = 0
        highest = ("sell", lowest[1], 0)

        while count < len(data_bank.data):
            if count < lowest[3]:
                count += 1
                continue
            else:
                if data_bank.data[count][1] > highest[2]:
                    highest = (
                        "sell",
                        data_bank.data[count][0],
                        data_bank.data[count][1]
                        )
            count += 1

        if len(data_bank.sums) == len(data_bank.data):
            return data_bank.sums
        else:
            total = highest[2]-lowest[2]
            data_bank.sums.append((lowest, highest, total))
            return get_sum_differences()
    elif data_bank.over_90_days:
        count = 0
        index = 0

        while count < len(data_bank.data):
            lowest = ("buy", data_bank.data[0][0], 1000000000, 0)
            if count in data_bank.buy_date_indices:
                count += 1
                continue
            else:
                while index < len(data_bank.data):
                    if data_bank.data[index][1] < lowest[2]:
                        lowest = (
                            "buy",
                            data_bank.data[index][0],
                            data_bank.data[index][1],
                            index
                            )
                    index += 1

                index = 0
                highest = ("sell", lowest[1], 0)

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
            count += 1
            total = highest[2]-lowest[2]
            data_bank.sums.append((lowest, highest, total))

        return data_bank.sums
