from flask import Flask

app = Flask(__name__)

@app.route('/')
def main(self):
    pass

@app.route('/')
def getDownTrend(user_id):
    pass

@app.route('/')
def getHighestTradingVolume(user_id):
    pass

@app.route('/user/<int:user_id>/')
def getBuyAndSellDates(user_id):
    pass