from flask import Flask, jsonify
from main import Application
import json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
application = Application()

#home page
@app.route('/')
def main():
    return "working"
    #return redirect(url_for('/get/downward_trend/<dates>'))
    #return redirect(url_for('/get/highest_trading_volume/<dates>'))
    #return redirect(url_for('/get/buy_and_sell_dates/<dates>'))

#get options 
@app.route('/get/')
def get_options():
    return "1. downward_trend 2. highest_trading_volume 3. buy_and_sell_dates"

#Get data by writing dates in the url

# Jsonify (main.py needs to return dictionary)
@app.route('/get/downward_trend/<dates>/')
def get_downward_trend_with_url(dates):
    return jsonify(application.get_downward_trend(dates)), 200

@app.route('/get/highest_trading_volume/<dates>/')
def get_highest_trading_volume_with_url(dates):
    return jsonify(application.get_highest_trading_volume(dates)), 200

@app.route('/get/buy_and_sell_dates/<string:dates>/')
def get_buy_and_sell_dates_with_url(dates):
    return jsonify(application.get_buy_and_sell_dates(dates)), 200

# Json.dumps
"""@app.route('/get/downward_trend/<dates>/')
def get_downward_trend_with_url(dates):
    return json.dumps(application.get_downward_trend(dates), sort_keys=False, indent=4), 200

@app.route('/get/highest_trading_volume/<dates>/')
def get_highest_trading_volume_with_url(dates):
    return json.dumps(application.get_highest_trading_volume(dates), sort_keys=False, indent=4), 200

@app.route('/get/buy_and_sell_dates/<string:dates>/')
def get_buy_and_sell_dates_with_url(dates):
    return json.dumps(application.get_buy_and_sell_dates(dates), sort_keys=False, indent=4), 200"""

if __name__ == "__main__":
    app.run()