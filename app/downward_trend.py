"""
downward_trend.py:
Contains function that returns biggest downward trend's start and end day.
"""

from app import price_iterator
from app.helpers import time_engine
from app.json_formatters import incorrect_input_json_formatter
from app.json_formatters import downward_trend_json_formatter
from app import data_bank

timeform = time_engine.TimeForm()
trend_formatter = downward_trend_json_formatter.DownwardTrendFormatter()


def get_downward_trend():
    """
    Function that returns biggest downward trend's
    start and end day.
    """

    chosen_prices = []
    chosen_price_quantities = []
    count = 0
    most = (0, 0, 0)
    start_timestamp = 0
    end_timestamp = 0
    start = data_bank.data[0][0]

    if data_bank.incorrect_input:
        text = "Incorrect input"
        return incorrect_input_json_formatter.incorrect_input_to_json_form(
            tuple((
                text,
                data_bank.data
            ))
        )
    else:
        highest_prices = price_iterator.get_highest_prices(start)

        if data_bank.one_day:
            text = ("0 days since we are only looking at 1 day "
                    "thus we can't compare day's highest prices")

            return trend_formatter.incorrect_downward_trend_to_json_form(
                tuple((
                    text,
                    data_bank.data[0][3]
                ))
            )
        elif data_bank.under_90_days:
            for count, value in enumerate(highest_prices):
                if count == len(highest_prices)-1:
                    if end_timestamp == 0:
                        end_timestamp = value[0]
                    chosen_price_quantities.append((start_timestamp,
                                                    end_timestamp,
                                                    len(chosen_prices)))
                    start_timestamp = 0
                    chosen_prices = []
                else:
                    if value[1] > highest_prices[count+1][1]:
                        if start_timestamp == 0:
                            start_timestamp = value[0]
                        if value[1] not in chosen_prices:
                            chosen_prices.append(value[1])
                        chosen_prices.append(highest_prices[count+1][1])
                        end_timestamp = 0
                    else:
                        if end_timestamp == 0:
                            end_timestamp = value[0]
                        chosen_price_quantities.append((start_timestamp,
                                                        end_timestamp,
                                                        len(chosen_prices)
                                                        ))
                        start_timestamp = 0
                        chosen_prices = []
                count += 1
        elif data_bank.over_90_days:
            for count, value in enumerate(data_bank.data):
                if count == len(data_bank.data)-1:
                    if end_timestamp == 0:
                        end_timestamp = value[0]
                    chosen_price_quantities.append((start_timestamp,
                                                    end_timestamp,
                                                    len(chosen_prices)))
                    start_timestamp = 0
                    chosen_prices = []
                else:
                    if value[1] > data_bank.data[count+1][1]:
                        if start_timestamp == 0:
                            start_timestamp = value[0]
                        if value[1] not in chosen_prices:
                            chosen_prices.append(value[1])
                        chosen_prices.append(data_bank.data[count+1][1])
                        end_timestamp = 0
                    else:
                        if end_timestamp == 0:
                            end_timestamp = value[0]
                        chosen_price_quantities.append((start_timestamp,
                                                        end_timestamp,
                                                        len(chosen_prices)
                                                        ))
                        start_timestamp = 0
                        chosen_prices = []
                count += 1

    for quantity in chosen_price_quantities:
        if quantity[2] > most[2]:
            most = quantity

    date1 = timeform.get_date_from_timestamp(most[0]).strftime("%Y-%m-%d")
    date2 = timeform.get_date_from_timestamp(most[1]).strftime("%Y-%m-%d")

    text = (
            f"In bitcoin’s historical data from CoinGecko, "
            f"the price decreased {most[2]} days in a row "
            f"from {date1} "
            f"to {date2}"
            ).replace("\u2019", "'")

    return trend_formatter.downward_trend_to_json_form(
        tuple((
            text,
            data_bank.data[0][3],
            data_bank.data[0][3][:10],
            data_bank.data[0][3][11:],
            date1,
            date2,
            most[2]
        ))
    )
