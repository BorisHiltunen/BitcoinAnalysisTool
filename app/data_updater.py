"""data_updater.py: Contains function that updates application's data."""

from datetime import datetime, timezone
from app.helpers import time_engine
from app import data_bank

timeform = time_engine.TimeForm()


def update_data(dates: str):
    """Function for getting data with input's start and finish dates."""

    data_bank.data = []
    data_bank.buy_date_indices = []
    data_bank.sums = []
    prices = []
    total_volumes = []
    count = 0
    reducer = 0

    data_bank.incorrect_input = False
    data_bank.one_day = False
    data_bank.under_90_days = False
    data_bank.over_90_days = False

    now = datetime.now(timezone.utc)
    now_time = now.replace(tzinfo=timezone.utc)
    now_timestamp = now_time.timestamp()

    future_condition1 = now.replace(tzinfo=None) - \
        timeform.get_date_from_input(dates)[0].replace(tzinfo=None)
    future_condition2 = now.replace(tzinfo=None) - \
        timeform.get_date_from_input(dates)[1].replace(tzinfo=None)

    if dates[2] == "-" or str(future_condition1)[0] == "-" or \
            str(future_condition2)[0] == "-":
        data_bank.incorrect_input = True
        data_bank.data.append(dates)
        return

    date1 = timeform.get_timestamps_from_input(dates)[0]
    date2 = timeform.get_timestamps_from_input(dates)[1]

    if date1 > date2 or date1 < 1364428800.0:
        data_bank.incorrect_input = True
        data_bank.data.append(dates)
        return

    if date2 != now_timestamp:
        date2 += 3600
        reducer += 3600

    data = data_bank.cg.get_coin_market_chart_range_by_id(id='bitcoin',
        vs_currency='eur',
        from_timestamp=date1,
        to_timestamp=date2
        )

    for price in data["prices"]:
        prices.append((price[0], price[1]))
    for volume in data["total_volumes"]:
        total_volumes.append((volume[0], volume[1]))

    count = 0

    if now_timestamp-date2 > 113666279.31145096:
        if (date2-reducer)-date1 <= 86400:
            data_bank.one_day = True
        elif (date2-reducer)-date1 <= 7862400:
            data_bank.under_90_days = True
        else:
            data_bank.over_90_days = True
        while count < len(total_volumes):
            data_bank.data.append(
                tuple((
                    total_volumes[count][0],
                    prices[count][1],
                    total_volumes[count][1],
                    dates
                ))
            )
            count += 1
    else:
        if (date2-reducer)-date1 <= 86400:
            data_bank.one_day = True
            while count < len(total_volumes):
                data_bank.data.append(
                    tuple((
                        total_volumes[count][0],
                        prices[count][1],
                        total_volumes[count][1],
                        dates
                    ))
                )
                count += 1

        elif (date2-reducer)-date1 <= 7862400:
            data_bank.under_90_days = True
            while count < len(total_volumes):
                data_bank.data.append(
                    tuple((
                        total_volumes[count][0],
                        prices[count][1],
                        total_volumes[count][1],
                        dates
                    ))
                )
                count += 1
        else:
            data_bank.over_90_days = True
            while count < len(total_volumes):
                data_bank.data.append(
                    tuple((
                        total_volumes[count][0],
                        prices[count][1],
                        total_volumes[count][1],
                        dates
                    ))
                )
                count += 1
