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
from datetime import datetime, timezone
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

class Application:
    def __init__(self):
        self.data = []
        self.buy_date_indices = []
        self.sums = []
        self.amount = 0

    # 1 Getting data
    # Function for getting data with start and finish dates
    def update_data(self, dates: str):

        prices = []
        total_volumes = []
        count = 0
        self.data = []

        date1 = self.get_dates(dates)[0]
        date2 = self.get_dates(dates)[1]

        if date1 > date2:
            
            text = "Incorrect input"

            return self.incorrect_input_to_json_form(tuple((text, dates, self.get_dates(dates)[0],
            self.get_dates(dates)[1])))

        now = datetime.now()

        if date2 != now.strftime("%d-%b-%Y (%H:%M:%S.%f)"):
            date2 += 3600

        data = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='eur', from_timestamp=date1, to_timestamp=date2)

        for price in data["prices"]:
            prices.append((date1, price[1]))
        for price in data["total_volumes"]:
            total_volumes.append((date1, price[1]))

        while count < len(prices):
            self.data.append(tuple((date1, prices[count], total_volumes[count], dates)))
            date1 += 3600
            count += 1

    # IMPORTANT THIS FUNCTION ADDS 2 HOURS FOR SOME REASON!
    # Function that changes string containing two dates into tuple that contains two timestamps
    def get_dates(self, dates: str):
        year1 = f"{dates[6]}{dates[7]}{dates[8]}{dates[9]}"
        month1 = f"{dates[3]}{dates[4]}"
        day1 = f"{dates[0]}{dates[1]}"

        year2 = f"{dates[17]}{dates[18]}{dates[19]}{dates[20]}"
        month2 = f"{dates[14]}{dates[15]}"
        day2 = f"{dates[11]}{dates[12]}"

        date1_in_correct_form = f"{year1}-{month1}-{day1} 00:00:00"
        date2_in_correct_form = f"{year2}-{month2}-{day2} 00:00:00"

        string_to_date1 = datetime.fromisoformat(date1_in_correct_form)
        string_to_date2 = datetime.fromisoformat(date2_in_correct_form)

        utc_time1 = string_to_date1.replace(tzinfo=timezone.utc)
        utc_time2 = string_to_date2.replace(tzinfo=timezone.utc)

        utc_timestamp1 = utc_time1.timestamp()
        utc_timestamp2 = utc_time2.timestamp()

        return utc_timestamp1, utc_timestamp2
    
    # Function that changes date into timestamp
    def correct_form_for_crypto(self, date: str):
        year = f"{date[6]}{date[7]}{date[8]}{date[9]}"
        month = f"{date[3]}{date[4]}"
        day = f"{date[0]}{date[1]}"

        date_in_correct_form = f"{year}-{month}-{day} 00:00:00"

        string_to_date = datetime.fromisoformat(date_in_correct_form)

        utc_time = string_to_date.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.timestamp()

        return utc_timestamp

    # Function that converts timestamp into a date
    def convert_timestamp_to_date(self, timestamp):
        date = datetime.fromtimestamp(timestamp)
        return date

    def converted_date_to_correct_form(self, date: str):
        year = f"{date[0]}{date[1]}{date[2]}{date[3]}"
        month = f"{date[5]}{date[6]}"
        day = f"{date[8]}{date[9]}"

        return f"{day}-{month}-{year}"

    # Downward trend
    # Function that returns biggest downward trend from the given dates
    def get_downward_trend(self):

        chosen_prices = []
        chosen_price_quantities = []
        count = 0
        most = 0

        while count < len(self.data):
            if count == len(self.data)-1:
                if self.data[count-1][1] > self.data[count][1]:
                    chosen_prices.append(self.data[count][1])
                else:
                    chosen_price_quantities.append(len(chosen_prices))
                    chosen_prices = []
            else:
                if self.data[count][1] > self.data[count+1][1]:
                    if self.data[count][1] not in chosen_prices:
                        chosen_prices.append(self.data[count][1])
                    chosen_prices.append(self.data[count+1][1])
                else:
                    chosen_price_quantities.append(len(chosen_prices))
                    chosen_prices = []
            count += 1

        for quantity in chosen_price_quantities:
            if quantity > most:
                most = quantity

        text = (f"In bitcoin’s historical data from CoinGecko, the price decreased {most} days in a row" 
        f" from {self.data[0][3][:10]} to {self.data[0][3][11:]}".replace("\u2019", "'"))

        return self.downward_trend_to_json_form(tuple((text, self.data[0][3], self.data[0][3][:10], self.data[0][3][11:], most)))

    # HighestTradingVolume
    # Function that returns HighestTradingVolume from the given dates
    def get_highest_trading_volume(self):

        highest = "", 0.0

        for volume in self.data:
            if volume[2][1] > highest[1]:
                highest = volume[2][0], volume[2][1]

        text = f"{self.convert_timestamp_to_date(highest[0])}:{highest[1]}"

        return self.highest_trading_volume_to_json_form(tuple((text, self.data[0][3], self.data[0][3][:10], 
        self.data[0][3][11:], highest[0], highest[1])))

    # 2 getting price differences
    # Testing recursion
    def get_price_differences(self):

        count = 0

        lowest = "buy", self.data[0][0], 1000000000, 0

        while count < len(self.data):
            if count in self.buy_date_indices:
                count += 1
                continue
            else:
                if self.data[count][1][1] < lowest[2]:
                    lowest = "buy", self.data[count][0], self.data[count][1][1], count
            count += 1

        self.buy_date_indices.append(lowest[3])

        count = 0
        highest = "sell", lowest[1], 0

        while count < len(self.data):
            
            if count < lowest[3]:
                count += 1
                continue
            else:
                if self.data[count][1][1] > highest[2]:
                    highest = "sell", self.data[count][0], self.data[count][1][1]
            count += 1

        #Add dates, buyprice and sellprice
        if len(self.sums) == len(self.data):
            #return len(self.sums), self.sums, self.sums[2], self.convert_timestamp_to_date(self.sums[2][0][1]), self.convert_timestamp_to_date(self.sums[2][1][1])
            #print(len(self.sums), self.sums, self.sums[2], self.convert_timestamp_to_date(self.sums[2][0][1]), self.convert_timestamp_to_date(self.sums[2][1][1]))
            #print(self.sums[0][0])
            return self.sums
        else:
            sum = highest[2]-lowest[2]
            self.sums.append((lowest, highest, sum))
            #return "again"
            return self.get_price_differences()

        """if highest[2] <= lowest[2]:

            text = "Don't buy"

            return self.bad_time_to_buy_to_json_form(tuple((text, dates, self.get_dates(dates)[0],
            self.get_dates(dates)[1], lowest[1], self.get_highest_price(dates)[0], 
            int(lowest[2]), int(self.get_highest_price(dates)[1]))))
        else:

            text = f"{self.convert_timestamp_to_date(lowest[1])}, {self.convert_timestamp_to_date(highest[1])}"

            return self.buy_and_sell_dates_to_json_form(tuple((text, dates, self.get_dates(dates)[0],
            self.get_dates(dates)[1], lowest[1], highest[1], 
            int(lowest[2]), int(highest[2]))))"""

    # 3 getting the best time to buy and sell
    #It is needed to edit this
    # Function for getting the best days to buy and sell bitcoin
    def get_best_days_to_buy_and_sell(self):
        both = (('buy', 1637971200.0, 1000000000.0, 24), ('sell', 1637971200.0, 0.0, 24), 0.0)
        #print(f"here {lowest[0][2]}")

        for difference in self.get_price_differences():
            if difference[2] > both[2]:
                both = difference

        return both
        #return self.buy_and_sell_dates_to_json_form(tuple((text, self.data[0][3], self.data[0][3][:10], 
        #self.data[0][3][11:], highest[0], highest[1])))

    # Function that returns data from incorrect input in json form
    def incorrect_input_to_json_form(self, data):
        dictionary = {}
        dictionary2 = {}
        options = ["text", "input", "first_date", "second_date", "data"]

        for option in options:
            match option:
                case "text":
                    dictionary[option] = data[0]
                case "data":
                    for copy in options:
                        match copy:
                            case "input":
                                dictionary2[copy] = data[1]
                            case "first_date":
                                dictionary2[copy] = self.convert_timestamp_to_date(data[2])
                            case "second_date":
                                dictionary2[copy] = self.convert_timestamp_to_date(data[3])
                    dictionary[option] = dictionary2

        return dictionary

    # Function that returns data in JSON form from input that didn't have a good time to buy bitcoin thus neither sell it
    def bad_time_to_buy_to_json_form(self, data):
        dictionary = {}
        dictionary2 = {}
        options = ["text", "input", "first_date", "second_date", "lowest_price_date", "highest_price_date", "lowest_price", "highest_price", "data"]

        for option in options:
            match option:
                case "text":
                    dictionary[option] = data[0]
                case "data":
                    for copy in options:
                        match copy:
                            case "input":
                                dictionary2[copy] = data[1]
                            case "first_date":
                                dictionary2[copy] = self.convert_timestamp_to_date(data[2])
                            case "second_date":
                                dictionary2[copy] = self.convert_timestamp_to_date(data[3])
                            case "highest_price_date":
                                dictionary2[copy] = self.convert_timestamp_to_date(data[4])
                            case "lowest_price_date":
                                dictionary2[copy] = self.convert_timestamp_to_date(data[5])
                            case "highest_price":
                                dictionary2[copy] = data[6]
                            case "lowest_price":
                                dictionary2[copy] = data[7]
                    dictionary[option] = dictionary2

        return dictionary

    # Function that returns downward trend data in json form
    def downward_trend_to_json_form(self, data):
        dictionary = {}
        dictionary2 = {}
        options = ["text", "input", "first_date", "second_date", "days", "data"]

        for option in options:
            match option:
                case "text":
                    dictionary[option] = data[0]
                case "data":
                    for copy in options:
                        match copy:
                            case "input":
                                dictionary2[copy] = data[1]
                            case "first_date":
                                dictionary2[copy] = data[2]
                            case "second_date":
                                dictionary2[copy] = data[3]
                            case "days":
                                dictionary2[copy] = f"{data[4]} days"
                    dictionary[option] = dictionary2

        return dictionary

    # Function that returns highest trading volume data in json form
    def highest_trading_volume_to_json_form(self, data):
        dictionary = {}
        dictionary2 = {}
        options = ["text", "input", "first_date", "second_date", "highest_trading_volume_date", "highest_trading_volume", "data"]
        
        for option in options:
            match option:
                case "text":
                    dictionary[option] = data[0]
                case "data":
                    for copy in options:
                        match copy:
                            case "input":
                                dictionary2[copy] = data[1]
                            case "first_date":
                                dictionary2[copy] = data[2]
                            case "second_date":
                                dictionary2[copy] = data[3]
                            case "highest_trading_volume_date":
                                dictionary2[copy] = self.convert_timestamp_to_date(data[4])
                            case "highest_trading_volume":
                                dictionary2[copy] = data[5]
                    dictionary[option] = dictionary2

        return dictionary
    
    # Function that returns buy and sell date data in json form
    def buy_and_sell_dates_to_json_form(self, data):
        dictionary = {}
        dictionary2 = {}
        options = ["text", "input", "first_date", "second_date", "buy_date", "sell_date", "buy_price", "sell_price", "data"]

        for option in options:
            match option:
                case "text":
                    dictionary[option] = data[0]
                case "data":
                    for copy in options:
                        match copy:
                            case "input":
                                dictionary2[copy] = data[1]
                            case "first_date":
                                dictionary2[copy] = self.convert_timestamp_to_date(data[2])
                            case "second_date":
                                dictionary2[copy] = self.convert_timestamp_to_date(data[3])
                            case "buy_date":
                                dictionary2[copy] = self.convert_timestamp_to_date(data[4])
                            case "sell_date":
                                dictionary2[copy] = self.convert_timestamp_to_date(data[5])
                            case "buy_price":
                                dictionary2[copy] = data[6]
                            case "sell_price":
                                dictionary2[copy] = data[7]
                    dictionary[option] = dictionary2

        return dictionary

if __name__ == "__main__":
    application = Application()

    application.update_data("26-11-2021|28-11-2021")
    #for now its not needed to use this here too since get_best_days_to_buy_and_sell function calls get price differences function
    #print(application.get_price_differences())
    print("1.")
    print(application.get_downward_trend())
    print("2.")
    print(application.get_highest_trading_volume())
    print("3.")
    print(application.get_best_days_to_buy_and_sell())

    #Funktions used in the application
    #----------------------------------------------------
    print(1)
    print(application.correct_form_for_crypto("25-11-2021"))
    print(2)
    print(application.convert_timestamp_to_date(1257326176)) 
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

    application.update_data("25-11-2021|30-11-2021")

    #A) mission Funktions (DownWardTrend)
    print("Downward")
    print(application.get_downward_trend())

    #B) mission Funktions (HighestTradingVolume)
    print("HighestTradingVolume")
    print(application.get_highest_trading_volume())

    #C) mission Funktions (TimeMachine)

    #Buy and sell test
    print("whenToBuyAndSell")
    print(application.get_best_days_to_buy_and_sell())

    application.update_data("25-11-2021|24-11-2021")
    print(application.data)
    #Don't buy test
    print("don't buy")
    print(application.get_best_days_to_buy_and_sell())