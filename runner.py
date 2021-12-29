"""
runner.py: Is in charge of the routes.
Also the application will be run from here.
"""

from flask import Flask, jsonify
from app import data_updater
from app import downward_trend
from app import highest_trading_volume
from app import buy_and_sell_dates

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def main():
    """
    Function for the home page that returns text
    that says the page is working if it is.
    """

    return "working"


@app.route('/get/')
def get_options():
    """Function for the info page that returns URL options."""

    return "1. downward_trend 2. highest_trading_volume 3. buy_and_sell_dates"


@app.route('/get/downward_trend/<dates>/')
def get_downward_trend_with_url(dates):
    """
    Function for the downward trend page
    that displays downward trend data.
    """

    data_updater.update_data(dates)
    return jsonify(downward_trend.get_downward_trend()), 200


@app.route('/get/highest_trading_volume/<dates>/')
def get_highest_trading_volume_with_url(dates):
    """
    Function for the highest trading volume page
    that displays highest trading volume data.
    """

    data_updater.update_data(dates)
    return jsonify(highest_trading_volume.get_highest_trading_volume()), 200


@app.route('/get/buy_and_sell_dates/<string:dates>/')
def get_buy_and_sell_dates_with_url(dates):
    """
    Function for the buy and sell dates page
    that displays data about best dates to buy and sell bitcoin.
    """

    data_updater.update_data(dates)
    return jsonify(buy_and_sell_dates.get_best_days_trading_days()), 200


if __name__ == "__main__":
    app.run()
