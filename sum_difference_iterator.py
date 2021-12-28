"""
sum_difference_iterator.py:
Contains helper function for buy_and_sell_dates.py.
"""

import __init__


def get_sum_differences():
    """
    Helper function that returns sum differences
    for buy_and_sell_dates.py.
    """

    if __init__.under_90_days or __init__.one_day:
        count = 0

        lowest = ("buy", __init__.data[0][0], 1000000000, 0)

        while count < len(__init__.data):
            if count in __init__.buy_date_indices:
                count += 1
                continue
            else:
                if __init__.data[count][1] < lowest[2]:
                    lowest = (
                        "buy",
                        __init__.data[count][0],
                        __init__.data[count][1],
                        count
                        )
            count += 1

        __init__.buy_date_indices.append(lowest[3])

        count = 0
        highest = ("sell", lowest[1], 0)

        while count < len(__init__.data):
            if count < lowest[3]:
                count += 1
                continue
            else:
                if __init__.data[count][1] > highest[2]:
                    highest = (
                        "sell",
                        __init__.data[count][0],
                        __init__.data[count][1]
                        )
            count += 1

        if len(__init__.sums) == len(__init__.data):
            return __init__.sums
        else:
            total = highest[2]-lowest[2]
            __init__.sums.append((lowest, highest, total))
            return get_sum_differences()
    elif __init__.over_90_days:
        count = 0
        index = 0

        while count < len(__init__.data):
            lowest = ("buy", __init__.data[0][0], 1000000000, 0)
            if count in __init__.buy_date_indices:
                count += 1
                continue
            else:
                while index < len(__init__.data):
                    if __init__.data[index][1] < lowest[2]:
                        lowest = (
                            "buy",
                            __init__.data[index][0],
                            __init__.data[index][1],
                            index
                            )
                    index += 1

                index = 0
                highest = ("sell", lowest[1], 0)

                while index < len(__init__.data):
                    if index < lowest[3]:
                        index += 1
                        continue
                    else:
                        if __init__.data[index][1] > highest[2]:
                            highest = (
                                "sell",
                                __init__.data[index][0],
                                __init__.data[index][1]
                                )
                    index += 1
            count += 1
            total = highest[2]-lowest[2]
            __init__.sums.append((lowest, highest, total))

        return __init__.sums
