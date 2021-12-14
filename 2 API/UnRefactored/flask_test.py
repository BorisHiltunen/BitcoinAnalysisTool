from flask import Flask
from main import Application

app = Flask(__name__)
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
@app.route('/get/downward_trend/<dates>/')
def get_downward_trend_with_url(dates):
    return str(application.get_downward_trend(dates))

@app.route('/get/highest_trading_volume/<dates>/')
def get_highest_trading_volume_with_url(dates):
    return str(application.get_highest_trading_volume(dates))

@app.route('/get/buy_and_sell_dates/<string:dates>/')
def get_buy_and_sell_dates_with_url(dates):
    return str(application.get_buy_and_sell_dates(dates))

if __name__ == "__main__":
    app.run()