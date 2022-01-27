"""
buy_and_sell_dates.py:
Contains function that returns the best days to buy and sell bitcoin.
"""

from app.helpers import time_engine
from app import sum_difference_iterator
from app.json_formatters import incorrect_input_json_formatter
from app.json_formatters import buy_and_sell_dates_json_formatter
from app import data_bank

timeform = time_engine.TimeForm()
trading_formatter = buy_and_sell_dates_json_formatter.TradingFormatter()


def get_best_trading_days():
    """Function for getting the best days to buy and sell bitcoin."""

    both = {
        "buy_price": (0.0, 1000000000.0),
        "sell_price": (0.0, -1000000000.0),
        "profit": -1000000000.0
        }
    buy_timestamp = 0.0
    sell_timestamp = 0.0

    if data_bank.incorrect_input:
        text = "Incorrect input"

        return incorrect_input_json_formatter.incorrect_input_to_json_form(
            tuple((
                text,
                data_bank.data
            ))
        )

    for difference in sum_difference_iterator.get_sum_differences():
        if difference["profit"] > both["profit"]:
            both = difference

    buy_timestamp = both["buy_price"][0]
    sell_timestamp = both["sell_price"][0]

    date = timeform.get_date_from_timestamp(
        buy_timestamp).strftime("%Y-%m-%d %H:%M:%S")
    date2 = timeform.get_date_from_timestamp(
        sell_timestamp).strftime("%Y-%m-%d %H:%M:%S")

    if buy_timestamp == 0.0:
        text = "Something went wrong"

        return incorrect_input_json_formatter.incorrect_input_to_json_form(
            tuple((
                text,
                [data_bank.data[0][3]]
            ))
        )

    elif both["profit"] <= 0:
        text = "Don't buy"

        return trading_formatter.buy_and_sell_dates_to_json_form(
            tuple((
                text,
                data_bank.data[0][3],
                data_bank.data[0][3][:10],
                data_bank.data[0][3][11:],
                date[:10],
                date2[:10],
                date[11:],
                date2[11:],
                both["buy_price"][1],
                both["sell_price"][1],
                both["profit"]
            ))
        )

    elif data_bank.one_day:
        text = ("Don't buy unless you want to sell on the same day")

        return trading_formatter.buy_and_sell_dates_to_json_form(
            tuple((
                text,
                data_bank.data[0][3],
                data_bank.data[0][3][:10],
                data_bank.data[0][3][11:],
                date[:10],
                date2[:10],
                date[11:],
                date2[11:],
                both["buy_price"][1],
                both["sell_price"][1],
                both["profit"]
            ))
        )
    else:
        text = (f"Buy date: "
                f"{date[:10]}, "
                f"Sell date: "
                f"{date2[:10]}")

        return trading_formatter.buy_and_sell_dates_to_json_form(
            tuple((
                text,
                data_bank.data[0][3],
                data_bank.data[0][3][:10],
                data_bank.data[0][3][11:],
                date[:10],
                date2[:10],
                date[11:],
                date2[11:],
                both["buy_price"][1],
                both["sell_price"][1],
                both["profit"]
            ))
        )
