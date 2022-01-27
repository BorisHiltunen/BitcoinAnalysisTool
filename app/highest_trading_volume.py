"""
highest_trading_volume.py:
Contains function that returns highest trading volume and its date.
"""

from app.json_formatters import incorrect_input_json_formatter
from app.helpers import time_engine
from app.json_formatters import trading_volume_json_formatter
from app import data_bank

timeform = time_engine.TimeForm()


def get_highest_trading_volume():
    """Function that returns Highest trading volume from the given dates."""

    highest = ("", 0.0)

    if data_bank.incorrect_input:
        text = "Incorrect input"
        return incorrect_input_json_formatter.incorrect_input_to_json_form(
            tuple((
                text,
                data_bank.data
            ))
        )

    for volume in data_bank.data:
        if volume[2] > highest[1]:
            highest = (volume[0], volume[2])

    date = timeform.get_date_from_timestamp(
        highest[0]).strftime("%Y-%m-%d %H:%M:%S")

    text = (f"Highest trading volume date: "
            f"{date}, "
            f"Highest trading volume: {highest[1]}")

    return trading_volume_json_formatter.highest_trading_volume_to_json_form(
        tuple((
            text,
            data_bank.data[0][3],
            data_bank.data[0][3][:10],
            data_bank.data[0][3][11:],
            date[:10],
            date[11:],
            highest[1]
        ))
    )
