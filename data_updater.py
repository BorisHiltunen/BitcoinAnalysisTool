"""data_updater.py: Contains function that updates application's data."""

from datetime import datetime
from timestamp_engine import TimeForm
import __init__

timeform = TimeForm()


def update_data(dates: str):
    """Function for getting data with input's start and finish dates."""

    __init__.data = []
    __init__.buy_date_indices = []
    __init__.sums = []
    prices = []
    total_volumes = []
    count = 0
    reducer = 0

    __init__.incorrect_input = False
    __init__.one_day = False
    __init__.under_90_days = False
    __init__.over_90_days = False

    date1 = timeform.get_timestamps_from_input(dates)[0]
    date2 = timeform.get_timestamps_from_input(dates)[1]

    if date1 > date2:
        __init__.incorrect_input = True
        __init__.data.append(dates)
        return

    now = datetime.now()

    if date2 != now.strftime("%d-%b-%Y (%H:%M:%S.%f)"):
        date2 += 3600
        reducer += 3600

    data = __init__.cg.get_coin_market_chart_range_by_id(
        id='bitcoin',
        vs_currency='eur',
        from_timestamp=date1,
        to_timestamp=date2
        )

    for price in data["prices"]:
        prices.append(price[1])
    for volume in data["total_volumes"]:
        total_volumes.append(volume[1])

    if (date2-reducer)-date1 <= 86400:
        __init__.one_day = True
        while count < len(prices):
            __init__.data.append(
                tuple((
                    date1,
                    prices[count],
                    total_volumes[count],
                    dates
                ))
            )
            date1 += 3600
            count += 1

    elif (date2-reducer)-date1 <= 7862400:
        __init__.under_90_days = True
        while count < len(prices):
            __init__.data.append(
                tuple((
                    date1,
                    prices[count],
                    total_volumes[count],
                    dates
                ))
            )
            date1 += 3600
            count += 1
    else:
        __init__.over_90_days = True
        while count < len(prices):
            __init__.data.append(
                tuple((
                    date1,
                    prices[count],
                    total_volumes[count],
                    dates
                ))
            )
            date1 += 86400
            count += 1
