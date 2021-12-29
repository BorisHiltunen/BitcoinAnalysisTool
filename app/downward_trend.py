"""
downward_trend.py:
Contains function that returns biggest downward trend's start and end day.
"""

from app import price_iterator
from app.helpers import timestamp_engine
from app.json_formatters import incorrect_input_json_formatter
from app.json_formatters import downward_trend_json_formatter
from app import data_bank

timeform = timestamp_engine.TimeForm()
trend_formatter = downward_trend_json_formatter.DownwardTrendFormatter()


def get_downward_trend():
    """
    Function that returns biggest downward trend's start and end day.
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
    elif data_bank.one_day:
        text = ("0 days since we are only looking at 1 day "
                "thus we can't compare day's highest prices")

        return trend_formatter.incorrect_downward_trend_to_json_form(
            tuple((
                text,
                data_bank.data[0][3]
            ))
        )
    elif data_bank.under_90_days:
        while count < len(price_iterator.get_highest_prices(start)):
            if count == len(price_iterator.get_highest_prices(start))-1:
                if end_timestamp == 0:
                    end_timestamp = price_iterator.get_highest_prices(
                        start)[count][0]
                chosen_price_quantities.append((start_timestamp,
                                                end_timestamp,
                                                len(chosen_prices)))
                start_timestamp = 0
                chosen_prices = []
            else:
                if (price_iterator.get_highest_prices(start)[count][1] >
                        price_iterator.get_highest_prices(start)[count+1][1]):
                    if start_timestamp == 0:
                        start_timestamp = price_iterator.get_highest_prices(
                            start)[count][0]
                    if price_iterator.get_highest_prices(
                            start)[count][1] not in chosen_prices:
                        chosen_prices.append(
                            price_iterator.get_highest_prices(start)[count][1])
                    chosen_prices.append(price_iterator.get_highest_prices(
                        start)[count+1][1])
                    end_timestamp = 0
                else:
                    if end_timestamp == 0:
                        end_timestamp = price_iterator.get_highest_prices(
                            start)[count][0]
                    chosen_price_quantities.append((start_timestamp,
                                                    end_timestamp,
                                                    len(chosen_prices)))
                    start_timestamp = 0
                    chosen_prices = []
            count += 1
    elif data_bank.over_90_days:
        while count < len(data_bank.data):
            if count == len(data_bank.data)-1:
                if end_timestamp == 0:
                    end_timestamp = data_bank.data[count][0]
                chosen_price_quantities.append((start_timestamp,
                                                end_timestamp,
                                                len(chosen_prices)))
                start_timestamp = 0
                chosen_prices = []
            else:
                if data_bank.data[count][1] > data_bank.data[count+1][1]:
                    if start_timestamp == 0:
                        start_timestamp = data_bank.data[count][0]
                    if data_bank.data[count][1] not in chosen_prices:
                        chosen_prices.append(data_bank.data[count][1])
                    chosen_prices.append(data_bank.data[count+1][1])
                    end_timestamp = 0
                else:
                    if end_timestamp == 0:
                        end_timestamp = data_bank.data[count][0]
                    chosen_price_quantities.append((start_timestamp,
                                                    end_timestamp,
                                                    len(chosen_prices)))
                    start_timestamp = 0
                    chosen_prices = []
            count += 1

    for quantity in chosen_price_quantities:
        if quantity[2] > most[2]:
            most = quantity

    text = (
            f"In bitcoin’s historical data from CoinGecko, "
            f"the price decreased {most[2]} days in a row "
            f"from {timeform.get_date_from_timestamp(most[0])[:10]} "
            f"to {timeform.get_date_from_timestamp(most[1])[:10]}"
            ).replace("\u2019", "'")

    return trend_formatter.downward_trend_to_json_form(
        tuple((
            text,
            data_bank.data[0][3],
            data_bank.data[0][3][:10],
            data_bank.data[0][3][11:],
            str(timeform.get_date_from_timestamp(most[0]))[:10],
            str(timeform.get_date_from_timestamp(most[1]))[:10],
            most[2]
        ))
    )