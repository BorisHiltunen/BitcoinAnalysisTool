#information about the code here

from flask import Flask, jsonify
from main import Application

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
application = Application()


@app.route('/')
def main():
    """
    Function for the home page that returns text
    that says the page is working if it is.
    """

    return "working"


@app.route('/get/')
def get_options():
    """function for the info page that returns URL options."""

    return "1. downward_trend 2. highest_trading_volume 3. buy_and_sell_dates"


@app.route('/get/downward_trend/<dates>/')
def get_downward_trend_with_url(dates):
    """
    function for the downward_trend page
    that displays downward trend data.
    """

    application.update_data(dates)
    return jsonify(application.get_downward_trend()), 200


@app.route('/get/highest_trading_volume/<dates>/')
def get_highest_trading_volume_with_url(dates):
    """
    function for the highest_trading_volume page
    that displays highest trading volume data.
    """

    application.update_data(dates)
    return jsonify(application.get_highest_trading_volume()), 200


@app.route('/get/buy_and_sell_dates/<string:dates>/')
def get_buy_and_sell_dates_with_url(dates):
    """
    function for the get_buy_and_sell_dates page
    that displays get buy and sell dates data.
    """

    application.update_data(dates)
    return jsonify(application.get_best_days_to_buy_and_sell()), 200


if __name__ == "__main__":
    app.run()
