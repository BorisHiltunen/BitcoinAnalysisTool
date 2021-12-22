#Virtual environment is needed for the module to work
#----------------------------------------------------------------------------- 79 character line
from pycoingecko import CoinGeckoAPI
from datetime import datetime, timezone

cg = CoinGeckoAPI()

class Application:
    def __init__(self):
        self.data = []
        self.buy_date_indices = []
        self.sums = []
        self.amount = 0
        self.incorrect_input = False

#----------------------------------------------------------------------------- 79 character line

    # 1 Getting data
    # Function for getting data with start and finish dates
    def update_data(self, dates: str):

        self.data = []
        self.buy_date_indices = []
        self.sums = []
        prices = []
        total_volumes = []
        self.amount = 0
        count = 0
        self.incorrect_input = False

        date1 = self.get_timestamps_from_dates(dates)[0]
        date2 = self.get_timestamps_from_dates(dates)[1]

        if date1 > date2:
            self.incorrect_input = True
            self.data.append(dates)
            return 

        now = datetime.now()

        if date2 != now.strftime("%d-%b-%Y (%H:%M:%S.%f)"):
            date2 += 3600

        data = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='eur', from_timestamp=date1, to_timestamp=date2)

        for price in data["prices"]:
            prices.append(price[1])
        for price in data["total_volumes"]:
            total_volumes.append(price[1])

        # here is something wrong
        # date2-date1 isn't 86400 when we are looking at 1 day difference?
        if date2-date1 == 86400:
            while count < len(prices):
                self.data.append(tuple((date1, prices[count], total_volumes[count], dates)))
                date1 += 300
                count += 1
        elif date2-date1 < 7862400:
            while count < len(prices):
                self.data.append(tuple((date1, prices[count], total_volumes[count], dates)))
                date1 += 3600
                count += 1
        else:
            while count < len(prices):
                self.data.append(tuple((date1, prices[count], total_volumes[count], dates)))
                date1 += 86400
                count += 1

#----------------------------------------------------------------------------- 79 character line

    # IMPORTANT THIS FUNCTION ADDS 2 HOURS FOR SOME REASON!
    # Function that changes string containing two dates into tuple that contains two timestamps
    def get_timestamps_from_dates(self, dates: str):
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

#----------------------------------------------------------------------------- 79 character line

    # Function that converts timestamp into a date
    def convert_timestamp_to_date(self, timestamp):
        date = datetime.fromtimestamp(timestamp)
        return date

#----------------------------------------------------------------------------- 79 character line

    # Downward trend
    # Function that returns biggest downward trend from the given dates
    def get_downward_trend(self):

        chosen_prices = []
        chosen_price_quantities = []
        count = 0
        most = 0

        if self.incorrect_input == True:
            text = "Incorrect input"
            return self.incorrect_input_to_json_form(tuple((text, self.data)))

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

#----------------------------------------------------------------------------- 79 character line

    # HighestTradingVolume
    # Function that returns HighestTradingVolume from the given dates
    def get_highest_trading_volume(self):

        if self.incorrect_input == True:
            text = "Incorrect input"
            return self.incorrect_input_to_json_form(tuple((text, self.data)))

        highest = "", 0.0

        for volume in self.data:
            if volume[2] > highest[1]:
                highest = volume[0], volume[2]

        # Think about how to express this
        text = f"{str(self.convert_timestamp_to_date(highest[0]))[:10]}, {highest[1]}"

        return self.highest_trading_volume_to_json_form(tuple((text, self.data[0][3], self.data[0][3][:10], 
        self.data[0][3][11:], str(self.convert_timestamp_to_date(highest[0]))[:10], highest[1])))

#----------------------------------------------------------------------------- 79 character line

    # 2 getting price differences
    def get_price_differences(self):

        count = 0

        lowest = "buy", self.data[0][0], 1000000000, 0

        while count < len(self.data):
            if count in self.buy_date_indices:
                count += 1
                continue
            else:
                if self.data[count][1] < lowest[2]:
                    lowest = "buy", self.data[count][0], self.data[count][1], count
            count += 1

        self.buy_date_indices.append(lowest[3])

        count = 0
        highest = "sell", lowest[1], 0

        while count < len(self.data):
            if count < lowest[3]:
                count += 1
                continue
            else:
                if self.data[count][1] > highest[2]:
                    highest = "sell", self.data[count][0], self.data[count][1]
            count += 1

        if len(self.sums) == len(self.data):
            #return len(self.sums), self.sums, self.sums[2], self.convert_timestamp_to_date(self.sums[2][0][1]), self.convert_timestamp_to_date(self.sums[2][1][1])
            return self.sums
        else:
            sum = highest[2]-lowest[2]
            self.sums.append((lowest, highest, sum))
            return self.get_price_differences()

#----------------------------------------------------------------------------- 79 character line

    # 3 getting the best time to buy and sell
    # Function for getting the best days to buy and sell bitcoin
    def get_best_days_to_buy_and_sell(self):

        if self.incorrect_input == True:
            text = "Incorrect input"

            return self.incorrect_input_to_json_form(tuple((text, self.data)))

        both = (('buy', 1637971200.0, 1000000000.0, 24), ('sell', 1637971200.0, 0.0), 0.0)

        for difference in self.get_price_differences():
            if difference[2] > both[2]:
                both = difference

        if both[2] <= 0:
            # Think about how to express this
            text = f"Don't buy"

            return self.buy_and_sell_dates_to_json_form(tuple((text, self.data[0][3], self.data[0][3][:10],
            self.data[0][3][11:], str(self.convert_timestamp_to_date(both[0][1]))[:10], str(self.convert_timestamp_to_date(both[1][1]))[:10],
            str(self.convert_timestamp_to_date(both[0][1]))[11:], str(self.convert_timestamp_to_date(both[1][1]))[11:], 
            int(both[0][2]), int(both[1][2]), both[2])))
        else:
            # Think about how to express this
            text = f"{self.convert_timestamp_to_date(both[0][1])}, {self.convert_timestamp_to_date(both[1][1])}"

            return self.buy_and_sell_dates_to_json_form(tuple((text, self.data[0][3], self.data[0][3][:10],
            self.data[0][3][11:], str(self.convert_timestamp_to_date(both[0][1]))[:10], str(self.convert_timestamp_to_date(both[1][1]))[:10], 
            str(self.convert_timestamp_to_date(both[0][1]))[11:], str(self.convert_timestamp_to_date(both[1][1]))[11:],
            int(both[0][2]), int(both[1][2]), both[2])))

#----------------------------------------------------------------------------- 79 character line

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
                                dictionary2[copy] = data[1][0]
                            case "first_date":
                                dictionary2[copy] = data[1][0][:10]
                            case "second_date":
                                dictionary2[copy] = data[1][0][11:]
                    dictionary[option] = dictionary2

        return dictionary

#----------------------------------------------------------------------------- 79 character line

    # Function that returns data in JSON form from input that didn't have a good time to buy bitcoin thus neither sell it
    def bad_time_to_buy_to_json_form(self, data):
        dictionary = {}
        dictionary2 = {}
        options = ["text", "input", "first_date", "second_date", "buy_date", "sell_date", "buy_time", 
        "sell_time", "buy_price", "sell_price", "profit", "data"]

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
                            case "buy_date":
                                dictionary2[copy] = data[4]
                            case "sell_date":
                                dictionary2[copy] = data[5]
                            case "buy_time":
                                dictionary2[copy] = data[6]
                            case "sell_time":
                                dictionary2[copy] = data[7]
                            case "buy_price":
                                dictionary2[copy] = data[8]
                            case "sell_price":
                                dictionary2[copy] = data[9]
                            case "profit":
                                dictionary2[copy] = data[10]
                    dictionary[option] = dictionary2

        return dictionary

#----------------------------------------------------------------------------- 79 character line

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

#----------------------------------------------------------------------------- 79 character line

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
                                dictionary2[copy] = data[4]
                            case "highest_trading_volume":
                                dictionary2[copy] = data[5]
                    dictionary[option] = dictionary2

        return dictionary
    
#----------------------------------------------------------------------------- 79 character line

    # Function that returns buy and sell date data in json form
    def buy_and_sell_dates_to_json_form(self, data):
        dictionary = {}
        dictionary2 = {}
        options = ["text", "input", "first_date", "second_date", "buy_date", "sell_date", "buy_time", 
        "sell_time", "buy_price", "sell_price", "profit", "data"]

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
                            case "buy_date":
                                dictionary2[copy] = data[4]
                            case "sell_date":
                                dictionary2[copy] = data[5]
                            case "buy_time":
                                dictionary2[copy] = data[6]
                            case "sell_time":
                                dictionary2[copy] = data[7]
                            case "buy_price":
                                dictionary2[copy] = data[8]
                            case "sell_price":
                                dictionary2[copy] = data[9]
                            case "profit":
                                dictionary2[copy] = data[10]
                    dictionary[option] = dictionary2

        return dictionary

#----------------------------------------------------------------------------- 79 character line

if __name__ == "__main__":
    application = Application()

    application.update_data("26-11-2020|27-11-2021")
    print("first 1.")
    print(application.get_downward_trend())
    print("2.")
    print(application.get_highest_trading_volume())
    print("3.")
    print(application.get_best_days_to_buy_and_sell())

    print("")

    application.update_data("25-11-2021|26-11-2021")
    print("second 1.")
    print(application.get_downward_trend())
    print("2.")
    print(application.get_highest_trading_volume())
    print("3.")
    print(application.get_best_days_to_buy_and_sell())

    print("")

    application.update_data("01-11-2021|26-11-2021")
    print("second 1.")
    print(application.get_downward_trend())
    print("2.")
    print(application.get_highest_trading_volume())
    print("3.")
    print(application.get_best_days_to_buy_and_sell())

    print("")

    #Funktions used in the application
    #----------------------------------------------------
    #print("A")
    #print(application.get_timestamps_from_dates("26-11-2021|28-11-2021"))
    #print("C")
    #print(application.convert_timestamp_to_date(1257326176)) 
    #print("")
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

    #application.update_data("25-11-2021|30-11-2021")

    #A) mission Funktions (DownWardTrend)
    #print("Downward")
    #print(application.get_downward_trend())

    #print("")

    #B) mission Funktions (HighestTradingVolume)
    #print("HighestTradingVolume")
    #print(application.get_highest_trading_volume())

    #print("")

    #C) mission Funktions (TimeMachine)

    #Buy and sell test
    #print("whenToBuyAndSell")
    #print(application.get_best_days_to_buy_and_sell())

    #print("")

    #Don't buy test
    #application.update_data("26-11-2021|30-11-2021")
    #print("don't buy")
    #print(application.get_best_days_to_buy_and_sell())

    print("")

    """#Wrong input test
    application.update_data("25-11-2021|24-11-2021")
    print("Wrong input")
    print("1.")
    print(application.get_downward_trend())
    print("2.")
    print(application.get_highest_trading_volume())
    print("3.")
    print(application.get_best_days_to_buy_and_sell())"""