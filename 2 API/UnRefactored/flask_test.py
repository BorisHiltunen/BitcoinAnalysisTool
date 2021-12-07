from flask import Flask, jsonify
from App import Application

app2 = Flask(__name__)
app = Application()

@app2.route('/')
def main():
    return "working"
    #return redirect(url_for('/get/getDownTrend/<dates>'))
    #return redirect(url_for('/get/HighestTradingVolume/<dates>'))
    #return redirect(url_for('/get/BuyAndSellDates/<dates>'))

@app2.route('/get/')
def getOptions():
    return "1. DownTrend 2. HighestTradingVolume 3. BuyAndSellDates"

#Get data by writing dates in the code
@app2.route('/get/DownTrend/')
def getDownTrend():
    return str(app.getDownwardTrend("25-11-2021|30-11-2021"))

@app2.route('/get/HighestTradingVolume/')
def getHighestTradingVolume():
    return str(app.getHighestTradingVolume("25-11-2021|30-11-2021"))

@app2.route('/get/BuyAndSellDates/')
def getBuyAndSellDates():
    return str(app.whenToBuyAndSell("25-11-2021|30-11-2021"))

#Get data by writing dates in the url
@app2.route('/get/DownTrend/<dates>/')
def getDownTrendWithUrl(dates):
    return str(app.getDownwardTrend(dates))

@app2.route('/get/HighestTradingVolume/<dates>/')
def getHighestTradingVolumeWithUrl(dates):
    return str(app.getDownwardTrend(dates))

@app2.route('/get/BuyAndSellDates/<string:dates>/')
def getBuyAndSellDatesWithUrl(dates):
    return str(app.whenToBuyAndSell(dates))

if __name__ == "__main__":
    app2.run()