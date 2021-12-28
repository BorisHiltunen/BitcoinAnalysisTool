"""
highest_trading_volume.py:
Contains function that returns highest trading volume and its date.
"""

import incorrect_input_json_formatter
from timestamp_engine import TimeForm
import trading_volume_json_formatter
import __init__

timeform = TimeForm()


def get_highest_trading_volume():
    """Function that returns highest trading volume and its date."""

    highest = ("", 0.0)

    if __init__.incorrect_input:
        text = "Incorrect input"
        return incorrect_input_json_formatter.incorrect_input_to_json_form(
            tuple((
                text,
                __init__.data
            ))
        )

    for volume in __init__.data:
        if volume[2] > highest[1]:
            highest = (volume[0], volume[2])

    text = (f"Highest trading volume date: "
            f"{timeform.get_date_from_timestamp(highest[0])[11:]}, "
            f"Highest trading volume: {highest[1]}")

    return trading_volume_json_formatter.highest_trading_volume_to_json_form(
        tuple((
            text,
            __init__.data[0][3],
            __init__.data[0][3][:10],
            __init__.data[0][3][11:],
            str(timeform.get_date_from_timestamp(highest[0]))[:10],
            str(timeform.get_date_from_timestamp(highest[0]))[11:],
            highest[1]
        ))
    )
