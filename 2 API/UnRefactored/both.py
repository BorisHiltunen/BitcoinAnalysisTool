from flask import Flask
from datetime import datetime
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

app2 = Flask(__name__)

@app2.route('/')
def main():
    return "working"
    #return redirect(url_for('/get/getDownTrend/<dates>'))
    #return redirect(url_for('/get/HighestTradingVolume/<dates>'))
    #return redirect(url_for('/get/BuyAndSellDates/<dates>'))

@app2.route('/get/')
def getOptions():
    return "1. DownTrend 2. HighestTradingVolume 3. BuyAndSellDates"

@app2.route('/get/DownTrend/')
def getDownTrend():
    return str(getDownwardTrend1("25-11-2021|30-11-2021"))

@app2.route('/get/HighestTradingVolume/')
def getHighestTradingVolume():
    return str(getHighestTradingVolume1("25-11-2021|30-11-2021"))

@app2.route('/get/BuyAndSellDates/')
def getBuyAndSellDates():
    print(whenToBuyAndSell1("25-11-2021|30-11-2021"))
    return str(whenToBuyAndSell1("25-11-2021|30-11-2021"))

@app2.route('/get/DownTrend/<dates>/')
def getDownTrendWithUrl(dates):
    return str(getDownwardTrend1(dates))

@app2.route('/get/HighestTradingVolume/<dates>/')
def getHighestTradingVolumeWithUrl(dates):
    return str(getDownwardTrend1(dates))

@app2.route('/get/BuyAndSellDates/<string:dates>/')
def getBuyAndSellDatesWithUrl(dates):
    print(dates)
    #return dates
    return str(whenToBuyAndSell1(dates))

#Think how to implement this
def getData1(self, start: str, finish: str):

    prices = []
    total_volumes = []
    count = 0
    self.data = []

    date1 = self.correctFormForCrypto2(start)
    date2 = self.correctFormForCrypto2(finish)
    now = datetime.now()

    if date2 != now.strftime("%d-%b-%Y (%H:%M:%S.%f)"):
        date2 += 3600

    data = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='eur', from_timestamp=date1, to_timestamp=date2)

    for price in data["prices"]:
        prices.append(price[1])
    for price in data["total_volumes"]:
        total_volumes.append(price[1])

    while count < len(prices):
        self.data.append(tuple((date1, prices[count], total_volumes[count])))
        date1 += 3600
        count += 1

def getData2(self, year1, month1, day1, year2, month2, day2):
    pass

#Think how to implement this
def getData3(self, timestamp1: int, timestamp2: int):

    prices = []
    total_volumes = []
    count = 0
    returnable_data = []

    now = datetime.now()

    if timestamp2 != now.strftime("%d-%b-%Y (%H:%M:%S.%f)"):
        timestamp2 += 3600

    data = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='eur', from_timestamp=timestamp1, to_timestamp=timestamp2)

    for price in data["prices"]:
        prices.append(price[1])
    for price in data["total_volumes"]:
        total_volumes.append(price[1])

    while count < len(prices):
        returnable_data.append(tuple((timestamp1, prices[count], total_volumes[count])))
        timestamp1 += 3600
        count += 1

    return returnable_data

def correctFormForCrypto1(self, day, month, year):
    date_in_correct_form = f"{day}/{month}/{year}"
    timestamp = datetime.strptime(date_in_correct_form, "%d/%m/%Y").timestamp()
    return timestamp

def correctFormForCrypto2(self, date):
    year = f"{date[6]}{date[7]}{date[8]}{date[9]}"
    month = f"{date[3]}{date[4]}"
    day = f"{date[0]}{date[1]}"

    date_in_correct_form = f"{day}/{month}/{year}"
    timestamp = datetime.strptime(date_in_correct_form, "%d/%m/%Y").timestamp()
    return timestamp

#"25-11-2021|30-11-2021"
def getDates(self, date: str):
    year1 = f"{date[6]}{date[7]}{date[8]}{date[9]}"
    month1 = f"{date[3]}{date[4]}"
    day1 = f"{date[0]}{date[1]}"

    year2 = f"{date[17]}{date[18]}{date[19]}{date[20]}"
    month2 = f"{date[14]}{date[15]}"
    day2 = f"{date[11]}{date[12]}"

    date_in_correct_form1 = f"{day1}/{month1}/{year1}"
    date_in_correct_form2 = f"{day2}/{month2}/{year2}"
    timestamp1 = datetime.strptime(date_in_correct_form1, "%d/%m/%Y").timestamp()
    timestamp2 = datetime.strptime(date_in_correct_form2, "%d/%m/%Y").timestamp()
    return timestamp1, timestamp2

def convertTimestampToDate(self, timestamp):
    date = datetime.fromtimestamp(timestamp)
    return date

def rekursion(self, start, finish):
    pass

#Downward trend
def getDownwardTrend1(self, dates: str):

    all_prices = []
    chosen_prices = []
    chosen_price_quantities = []
    count = 0
    most = 0

    date1 = self.getDates(dates)[0]
    date2 = self.getDates(dates)[1]
    data = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='eur', from_timestamp=date1, to_timestamp=date2)

    for price in data["prices"]:
        all_prices.append(price[1])

    while count < len(all_prices):
        if count == len(all_prices)-1:
            if all_prices[count-1] > all_prices[count]:
                chosen_prices.append(all_prices[count])
            else:
                chosen_price_quantities.append(len(chosen_prices))
                chosen_prices = []
        else:
            if all_prices[count] > all_prices[count+1]:
                if all_prices[count] not in chosen_prices:
                    chosen_prices.append(all_prices[count])
                chosen_prices.append(all_prices[count+1])
            else:
                chosen_price_quantities.append(len(chosen_prices))
                chosen_prices = []
        count += 1

    for quantity in chosen_price_quantities:
        if quantity > most:
            most = quantity
    return most

#HighestTradingVolume
def getHighestTradingVolume1(self, dates: str):

    date1 = self.getDates(dates)[0]
    date2 = self.getDates(dates)[1]
    data = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='eur', from_timestamp=date1, to_timestamp=date2)
    highest = 0

    for volume in data["total_volumes"]:
        if volume[1] > highest:
            highest = volume[1]
    return highest

#TimeMachine
#if more than 6 days +1 hour
def whenToBuyAndSell1(self, dates: str):

    all_prices = []
    chosen_prices = []
    count = 0

    date1 = self.getDates(dates)[0]
    date2 = self.getDates(dates)[1]
    now = datetime.now()

    if date2 != now.strftime("%d-%b-%Y (%H:%M:%S.%f)"):
        date2 += 3600

    data = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='eur', from_timestamp=date1, to_timestamp=date2)

    for price in data["prices"]:
        all_prices.append(price[1])

    lowest = "buy", date1, 1000000000

    while count < len(all_prices):
        if all_prices[count] < lowest[2]:
            lowest = "buy", date1, all_prices[count]
        date1 += 3600
        count += 1

    data2 = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='eur', from_timestamp=lowest[1], to_timestamp=date2)
    
    for price in data2["prices"]:
        chosen_prices.append(price[1])
    
    count = 0
    date1 = lowest[1]
    highest = "sell", date1, 0

    while count < len(chosen_prices):
        if chosen_prices[count] > highest[2]:
            highest = "sell", date1, chosen_prices[count]
        date1 += 3600
        count += 1

    if highest[2] < lowest[2]:
        return "Don't buy"
    else:
        answer = (lowest[0], self.convertTimestampToDate(lowest[1]), lowest[2], highest[0], self.convertTimestampToDate(highest[1]), highest[2])

        return answer

#TimeMachine
#remember to add 1 hour to the to_timestamp
#Think how to make this more simple
def whenToBuyAndSell3(self, dates: str):

    chosen_prices = []
    count = 0

    date1 = self.getDates(dates)[0]
    date2 = self.getDates(dates)[1]

    lowest = "buy", date1, 1000000000

    while count < len(self.data):
        if self.data[count][1] < lowest[2]:
            lowest = "buy", self.data[count][0], self.data[count][1]
        count += 1

    data2 = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='eur', from_timestamp=lowest[1], to_timestamp=date2)
    
    for price in data2["prices"]:
        chosen_prices.append(price[1])
    
    count = 0
    date1 = lowest[1]
    highest = "sell", date1, 0

    while count < len(chosen_prices):
        if chosen_prices[count] > highest[2]:
            highest = "sell", date1, chosen_prices[count]
        date1 += 3600
        count += 1

    if highest[2] < lowest[2]:
        return "Don't buy"
    else:
        answer = (lowest[0], self.convertTimestampToDate(lowest[1]), int(lowest[2]), highest[0], self.convertTimestampToDate(highest[1]), int(highest[2]))

        return answer

if __name__ == "__main__":
    app2.run()

    #Funktions used in the app
    #----------------------------------------------------
    #getData1("25-11-2021", "30-11-2021")

    #getData2(2012, 1, 1, 2012, 2, 1)

    #print(getData3(1257326176, 1257326176))

    #print(correctFormForCrypto1(25, 11, 2021))

    #print(correctFormForCrypto2("25-11-2021"))

    #print(convertTimestampToDate(1257326176))
    #----------------------------------------------------

    #IMPORTANT
    #----------------------------------------------------
    #if stime = "30/10/2021"
    # and stime2 = "30/11/2021"
    #data shows 747 hours 
    #Meaning there are 3 too many
    #and now its 21 a clock so does that matter?

    #btw it seems that every week there is one hour more
    #why?
    #----------------------------------------------------

    #A) mission Funktions (DownWardTrend)
    #print(getDownwardTrend1("25-11-2021", "30-11-2021"))
    #print(getDownwardTrend2(2021, 11, 25, 2021, 11, 30))

    #B) mission Funktions (HighestTradingVolume)
    #print(getHighestTradingVolume1("25-11-2021", "30-11-2021"))
    #print(getHighestTradingVolume2(2021, 11, 25, 2021, 11, 30))

    #C) mission Funktions (TimeMachine)

    #Buy ans sell test
    #print(whenToBuyAndSell1("25-11-2021", "30-11-2021"))
    #print(whenToBuyAndSell2(2021, 11, 25, 2021, 11, 30))
    #print(whenToBuyAndSell3("25-11-2021|30-11-2021"))

    #Don't buy test
    #print(app.whenToBuyAndSell1("12-06-2021", "20-05-2021"))
    #print(app.whenToBuyAndSell2(2021, 6, 12, 2021, 5, 20))
    #print(whenToBuyAndSell3("12-06-2021|20-05-2021"))