# This time Scrooge has his eyes on cryptocurrency — bitcoin to be exact — and he needs a tool to
#analyze its market value for a given date range.

#Your mission, should you choose to accept it, is to create an application that meets Scrooge’s needs.
#You are free to use any technology of your choosing. The resulting application can be for example a web
#page, an API backend, a mobile application, or anything else you deem suitable.

#Additional information:
#● Both start and end dates should be included in a date range.
#● A day’s price means the price at 00:00 UTC time (use price data from as close to midnight as
#possible as the day’s price, if you don’t have a datapoint from exactly midnight).
#● Allow the user of your application to pass the start and end dates of the date range in some way,
#e.g. via input fields in a UI or as parameters to an API.

#A. How many days is the longest bearish (downward) trend within a given date range?
#● Definition of a downward trend shall be: “Price of day N is lower than price of day N-1”
#● Expected output: The maximum amount of days bitcoin’s price was decreasing in a row.
#Example: In bitcoin’s historical data from CoinGecko, the price decreased 3 days in a row for the
#inputs from 2020-01-19 and to 2020-01-21, and the price decreased for 5 days in a row for the
#inputs from 2020-03-01 and to 2021-08-01.

#B. Which date within a given date range had the highest trading volume?
#● Expected output: The date with the highest trading volume and the volume on that day in
#euros.

#C. Scrooge has access to Gyro Gearloose’s newest invention, a time machine. Scrooge
#wants to use the time machine to profit from bitcoin. The application should be able to tell
#for a given date range, the best day for buying bitcoin, and the best day for selling the
#bought bitcoin to maximize profits. If the price only decreases in the date range, your
#output should indicate that one should not buy (nor sell) bitcoin on any of the days. You
#don't have to consider any side effects of time travel or how Scrooge's massive purchases
#would affect the price history.
#● Expected output: A pair of days: The day to buy and the day to sell. In the case when one
#should neither buy nor sell, return an indicative output of your choice.

#Use CoinGecko’s public API to get the needed data
#https://www.coingecko.com/en/api/documentation

#You will only need to use the /coins/{id}/market_chart/range endpoint. Read its
#documentation to understand how it works. Note that the API returns data with different granularity
#depending on the date range's length. Tip: You should add 1 hour to the `to` input to make sure
#that you always get data for the end date as well. Scrooge’s Money Bin only holds euros, so that is
#the only fiat currency you need to consider.

#For example, the following URL can be used to fetch bitcoin’s price, market cap and volume information
#in euros (€) from January 1, 2020 to December 31, 2020:
#https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_c
#urrency=eur&from=1577836800&to=1609376400

#The answer must be returned as:
#● A link to a public Git repo in a hosting service of your choice (GitHub, GitLab etc.)
#OR
#● A Git bundle (You can create a bundle file from your repo by running: git bundle create
#myreponame.bundle --all)

#What we value:
#● Clean code
#● Ease of use — Either host your solution somewhere where it can be used immediately, or include
#clear directions (e.g. in a README file) for running your solution.
#● Simplicity — Minimize the use of external libraries and dependencies. We want to see how you
#manage with a programming language of your choice, not how many packages you are able to
#import. You are of course highly encouraged to use any conveniences or standard library utilities
#that ship with your chosen language. It's also fine to build your solution around a single 3rd party
#library or framework, if that adds value to your solution.
#● Extensibility — Scrooge only wants these three features for now, but very likely wants to hire us
#to add capabilities to the application after it has proved its value to him.

#Vincit will review the code, and we like readable and maintainable code that follows good coding
#conventions. You may ask if you have any questions. Have fun coding!

#Code starts here!

#Venv is needed for the module to work

#How to get the data:
from datetime import datetime
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

#missions
#1. downward trend
#2. Highest trading volume
#3. Time machine

#IMPORTANT
#1 day from query time = 5 minute interval data
#1 - 90 days from query time = hourly data
#above 90 days from query time = daily data (00:00 UTC)

#1 hour = 3600
#day = 86400
#week = 604800
#month = 2629743

class Application:
    def __init__(self):
        pass

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

    def convertTimestampToDate(self, timestamp):
        date = datetime.fromtimestamp(timestamp)
        return date

    #Downward trend
    def getDownwardTrend1(self, start, finish):

        list1 = []
        list2 = []
        list3 = []
        count = 0
        most = 0

        date1 = self.correctFormForCrypto2(start)
        date2 = self.correctFormForCrypto2(finish)
        data = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='eur', from_timestamp=date1, to_timestamp=date2)

        for price in data["prices"]:
            list1.append(price[1])

        while count < len(list1):
            if count == len(list1)-1:
                if list1[count-1] > list1[count]:
                    list2.append(list1[count])
                else:
                    list3.append(len(list2))
                    list2 = []
            else:
                if list1[count] > list1[count+1]:
                    if list1[count] not in list2:
                        list2.append(list1[count])
                    list2.append(list1[count+1])
                else:
                    list3.append(len(list2))
                    list2 = []
            count += 1

        for quantity in list3:
            if quantity > most:
                most = quantity
        return most

    #Downward trend
    def getDownwardTrend2(self, year1, month1, day1, year2, month2, day2):

        list1 = []
        list2 = []
        list3 = []
        count = 0
        most = 0

        date1 = self.correctFormForCrypto1(day1, month1, year1)
        date2 = self.correctFormForCrypto1(day2, month2, year2)
        data = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='eur', from_timestamp=date1, to_timestamp=date2)

        for price in data["prices"]:
            list1.append(price[1])
        
        while count < len(list1):
            if count == len(list1)-1:
                if list1[count-1] > list1[count]:
                    list2.append(list1[count])
                else:
                    list3.append(len(list2))
                    list2 = []
            else:
                if list1[count] > list1[count+1]:
                    if list1[count] not in list2:
                        list2.append(list1[count])
                    list2.append(list1[count+1])
                else:
                    list3.append(len(list2))
                    list2 = []
            count += 1

        for quantity in list3:
            if quantity > most:
                most = quantity
        return most

    #HighestTradingVolume
    def getHighestTradingVolume1(self, start, finish):

        date1 = self.correctFormForCrypto2(start)
        date2 = self.correctFormForCrypto2(finish)
        data = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='eur', from_timestamp=date1, to_timestamp=date2)
        highest = 0

        for volume in data["total_volumes"]:
            if volume[1] > highest:
                highest = volume[1]
        return highest
    #HighestTradingVolume
    def getHighestTradingVolume2(self, year1, month1, day1, year2, month2, day2):

        date1 = self.correctFormForCrypto1(day1, month1, year1)
        date2 = self.correctFormForCrypto1(day2, month2, year2)
        data = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='eur', from_timestamp=date1, to_timestamp=date2)
        highest = 0

        for volume in data["total_volumes"]:
            if volume[1] > highest:
                highest = volume[1]
        return highest

    #TimeMachine
    #remember to add 1 hour to the to_timestamp
    def whenToBuyAndSell1(self, start: str, finish:str):

        list1 = []
        list2 = []
        count = 0

        date1 = self.correctFormForCrypto2(start)
        date2 = self.correctFormForCrypto2(finish)
        now = datetime.now()

        if date2 != now.strftime("%d-%b-%Y (%H:%M:%S.%f)"):
            date2 += 3600

        data = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='eur', from_timestamp=date1, to_timestamp=date2)

        for price in data["prices"]:
            list1.append(price[1])

        lowest = "buy", date1, 1000000000

        while count < len(list1):
            if list1[count] < lowest[2]:
                lowest = "buy", date1, list1[count]
            date1 += 3600
            count += 1

        data2 = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='eur', from_timestamp=lowest[1], to_timestamp=date2)
        
        for price in data2["prices"]:
            list2.append(price[1])
        
        count = 0
        date1 = lowest[1]
        highest = "sell", date1, 0

        while count < len(list2):
            if list2[count] > highest[2]:
                highest = "sell", date1, list2[count]
            date1 += 3600
            count += 1

        if highest[2] < lowest[2]:
            return "Don't buy"
        else:
            answer = (lowest[0], self.convertTimestampToDate(lowest[1]), lowest[2], highest[0], self.convertTimestampToDate(highest[1]), highest[2])

            return answer

    #TimeMachine
    #if more than 6 days +1 hour
    def whenToBuyAndSell2(self, year1, month1, day1, year2, month2, day2):

        list1 = []
        list2 = []
        count = 0

        date1 = self.correctFormForCrypto1(day1, month1, year1)
        date2 = self.correctFormForCrypto1(day2, month2, year2)
        now = datetime.now()

        if date2 != now.strftime("%d-%b-%Y (%H:%M:%S.%f)"):
            date2 += 3600

        data = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='eur', from_timestamp=date1, to_timestamp=date2)

        for price in data["prices"]:
            list1.append(price[1])

        lowest = "buy", date1, 1000000000

        while count < len(list1):
            if list1[count] < lowest[2]:
                lowest = "buy", date1, list1[count]
            date1 += 3600
            count += 1

        data2 = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='eur', from_timestamp=lowest[1], to_timestamp=date2)
        
        for price in data2["prices"]:
            list2.append(price[1])
        
        count = 0
        date1 = lowest[1]
        highest = "sell", date1, 0

        while count < len(list2):
            if list2[count] > highest[2]:
                highest = "sell", date1, list2[count]
            date1 += 3600
            count += 1

        if highest[2] < lowest[2]:
            return "Don't buy"
        else:
            answer = (lowest[0], self.convertTimestampToDate(lowest[1]), lowest[2], highest[0], self.convertTimestampToDate(highest[1]), highest[2])

            return answer

if __name__ == "__main__":
    app = Application()

    #Funktions used in the app
    #----------------------------------------------------
    #print(app.correctFormForCrypto1(25, 11, 2021))

    #print(app.correctFormForCrypto2("25-11-2021"))

    #print(app.convertTimestampToDate(1257326176))
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
    #print(app.getDownwardTrend1("25-11-2021", "30-11-2021"))
    #print(app.getDownwardTrend2(2021, 11, 25, 2021, 11, 30))

    #B) mission Funktions (HighestTradingVolume)
    #print(app.getHighestTradingVolume1("25-11-2021", "30-11-2021"))
    #print(app.getHighestTradingVolume2(2021, 11, 25, 2021, 11, 30))

    #C) mission Funktions (TimeMachine)

    #Buy ans sell test
    #print(app.whenToBuyAndSell1("25-11-2021", "30-11-2021"))
    #print(app.whenToBuyAndSell2(2021, 11, 25, 2021, 11, 30))

    #Don't buy test
    print(app.whenToBuyAndSell1("12-06-2021", "20-05-2021"))
    print(app.whenToBuyAndSell2(2021, 6, 12, 2021, 5, 20))
