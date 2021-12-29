"""main.py: Contains the whole application except Flask side of the project."""

from datetime import datetime, timezone
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()


class Application:
    """
    Class that contains the whole application
    except Flask side of the project.
    """
    def __init__(self):
        self.data = []
        self.buy_date_indices = []
        self.sums = []
        self.incorrect_input = False
        self.one_day = False
        self.under_90_days = False
        self.over_90_days = False

    def update_data(self, dates: str):
        """Function for getting data with start and finish dates."""

        self.data = []
        self.buy_date_indices = []
        self.sums = []
        prices = []
        total_volumes = []
        count = 0
        reducer = 0

        self.incorrect_input = False
        self.one_day = False
        self.under_90_days = False
        self.over_90_days = False

        date1 = self.get_timestamps_from_input(dates)[0]
        date2 = self.get_timestamps_from_input(dates)[1]

        print(self.get_date_from_timestamp(date1))
        print(self.get_date_from_timestamp(date2))

        if date1 > date2:
            self.incorrect_input = True
            self.data.append(dates)
            return

        now = datetime.now()

        if date2 != now.strftime("%d-%b-%Y (%H:%M:%S.%f)"):
            date2 += 3600
            reducer += 3600

        data = cg.get_coin_market_chart_range_by_id(id='bitcoin',
                                                    vs_currency='eur',
                                                    from_timestamp=date1,
                                                    to_timestamp=date2)

        for price in data["prices"]:
            prices.append(price[1])
        for volume in data["total_volumes"]:
            total_volumes.append(volume[1])

        if (date2-reducer)-date1 <= 86400:
            self.one_day = True
            while count < len(prices):
                self.data.append(
                    tuple((
                        date1,
                        prices[count],
                        total_volumes[count],
                        dates
                    ))
                )
                date1 += 3600
                count += 1

        elif (date2-reducer)-date1 <= 7862400:
            self.under_90_days = True
            while count < len(prices):
                self.data.append(
                    tuple((
                        date1,
                        prices[count],
                        total_volumes[count],
                        dates
                    ))
                )
                date1 += 3600
                count += 1
        else:
            self.over_90_days = True
            while count < len(prices):
                self.data.append(
                    tuple((
                        date1,
                        prices[count],
                        total_volumes[count],
                        dates
                    ))
                )
                date1 += 86400
                count += 1

    def get_timestamps_from_input(self, dates: str):
        """Helper function that returns tuple containing two timestamps."""

        count = 0

        year1 = ""
        month1 = ""
        day1 = ""

        year2 = ""
        month2 = ""
        day2 = ""

        while count < len(dates):
            if (count == 2 or count == 5 or count == 10
                    or count == 13 or count == 16):
                count += 1
                continue
            else:
                if count < 2:
                    day1 += dates[count]
                elif count < 5:
                    month1 += dates[count]
                elif count < 11:
                    year1 += dates[count]
                elif count < 13:
                    day2 += dates[count]
                elif count < 16:
                    month2 += dates[count]
                elif count < 21:
                    year2 += dates[count]
            count += 1

        date1_in_correct_form = f"{year1}-{month1}-{day1}"
        date2_in_correct_form = f"{year2}-{month2}-{day2}"

        string_to_date1 = datetime.fromisoformat(date1_in_correct_form)
        string_to_date2 = datetime.fromisoformat(date2_in_correct_form)

        utc_time1 = string_to_date1.replace(tzinfo=timezone.utc)
        utc_time2 = string_to_date2.replace(tzinfo=timezone.utc)

        utc_timestamp1 = utc_time1.timestamp()
        utc_timestamp2 = utc_time2.timestamp()

        return (utc_timestamp1, utc_timestamp2)

    def get_date_from_timestamp(self, timestamp):
        """helper function that converts timestamp into a date."""

        date = datetime.utcfromtimestamp(timestamp).strftime(
            '%Y-%m-%d %H:%M:%S')
        return date

    def get_highest_prices(self, timestamp):
        """Helper function that returns the highest prices as a list"""

        highest = (self.data[0][0], 0.0)
        prices = []
        count = 0

        for price in self.data:
            if price[0] - timestamp == 86400:
                prices.append(highest)
                highest = (self.data[count][0], 0.0)
                timestamp = price[0]
            else:
                if price[1] > highest[1]:
                    highest = (price[0], price[1])
            count += 1

        return prices

    def get_downward_trend(self):
        """
        Function that returns biggest downward trend
        from the given dates.
        """

        chosen_prices = []
        chosen_price_quantities = []
        count = 0
        most = (0, 0, 0)
        start_timestamp = 0
        end_timestamp = 0
        start = self.data[0][0]

        if self.incorrect_input:
            text = "Incorrect input"
            return self.incorrect_input_to_json_form(
                tuple((
                    text,
                    self.data
                ))
            )
        elif self.one_day:
            text = ("0 days since we are only looking at 1 day "
                    "thus we can't compare day's highest prices")

            return self.incorrect_input_for_downward_trend_to_json_form(
                tuple((
                    text,
                    self.data[0][3]
                ))
            )
        elif self.under_90_days:
            while count < len(self.get_highest_prices(start)):
                if count == len(self.get_highest_prices(start))-1:
                    if end_timestamp == 0:
                        end_timestamp = self.get_highest_prices(
                            start)[count][0]
                    chosen_price_quantities.append((start_timestamp,
                                                    end_timestamp,
                                                    len(chosen_prices)))
                    start_timestamp = 0
                    chosen_prices = []
                else:
                    if (self.get_highest_prices(start)[count][1] >
                            self.get_highest_prices(start)[count+1][1]):
                        if start_timestamp == 0:
                            start_timestamp = self.get_highest_prices(
                                start)[count][0]
                        if self.get_highest_prices(
                                start)[count][1] not in chosen_prices:
                            chosen_prices.append(
                                self.get_highest_prices(start)[count][1])
                        chosen_prices.append(self.get_highest_prices(
                            start)[count+1][1])
                        end_timestamp = 0
                    else:
                        if end_timestamp == 0:
                            end_timestamp = self.get_highest_prices(
                                start)[count][0]
                        chosen_price_quantities.append((start_timestamp,
                                                        end_timestamp,
                                                        len(chosen_prices)))
                        start_timestamp = 0
                        chosen_prices = []
                count += 1
        elif self.over_90_days:
            while count < len(self.data):
                if count == len(self.data)-1:
                    if end_timestamp == 0:
                        end_timestamp = self.data[count][0]
                    chosen_price_quantities.append((start_timestamp,
                                                    end_timestamp,
                                                    len(chosen_prices)))
                    start_timestamp = 0
                    chosen_prices = []
                else:
                    if self.data[count][1] > self.data[count+1][1]:
                        if start_timestamp == 0:
                            start_timestamp = self.data[count][0]
                        if self.data[count][1] not in chosen_prices:
                            chosen_prices.append(self.data[count][1])
                        chosen_prices.append(self.data[count+1][1])
                        end_timestamp = 0
                    else:
                        if end_timestamp == 0:
                            end_timestamp = self.data[count][0]
                        chosen_price_quantities.append((start_timestamp,
                                                        end_timestamp,
                                                        len(chosen_prices)))
                        start_timestamp = 0
                        chosen_prices = []
                count += 1

        for quantity in chosen_price_quantities:
            if quantity[2] > most[2]:
                most = quantity

        text = (
                f"In bitcoin’s historical data from CoinGecko, "
                f"the price decreased {most[2]} days in a row "
                f"from {self.get_date_from_timestamp(most[0])[:10]} "
                f"to {self.get_date_from_timestamp(most[1])[:10]}"
                ).replace("\u2019", "'")

        return self.downward_trend_to_json_form(
            tuple((
                text,
                self.data[0][3],
                self.data[0][3][:10],
                self.data[0][3][11:],
                str(self.get_date_from_timestamp(most[0]))[:10],
                str(self.get_date_from_timestamp(most[1]))[:10],
                most[2]
            ))
        )

    def get_highest_trading_volume(self):
        """Function that returns HighestTradingVolume from the given dates."""

        highest = ("", 0.0)

        if self.incorrect_input:
            text = "Incorrect input"
            return self.incorrect_input_to_json_form(
                tuple((
                    text,
                    self.data
                ))
            )

        for volume in self.data:
            if volume[2] > highest[1]:
                highest = (volume[0], volume[2])

        text = (f"Highest trading volume date: "
                f"{self.get_date_from_timestamp(highest[0])[11:]}, "
                f"Highest trading volume: {highest[1]}")

        return self.highest_trading_volume_to_json_form(
            tuple((
                text,
                self.data[0][3],
                self.data[0][3][:10],
                self.data[0][3][11:],
                str(self.get_date_from_timestamp(highest[0]))[:10],
                str(self.get_date_from_timestamp(highest[0]))[11:],
                highest[1]
            ))
        )

    def get_price_differences(self):
        """
        helper function that returns price differences
        for get_best_days_to_buy_and_sell().
        """

        count = 0
        index = 0

        while count < len(self.data):
            lowest = ("buy", self.data[0][0], 1000000000, 0)
            if count in self.buy_date_indices:
                count += 1
                continue
            else:
                while index < len(self.data):
                    if self.data[index][1] < lowest[2]:
                        lowest = (
                            "buy",
                            self.data[index][0],
                            self.data[index][1],
                            index
                            )
                    index += 1

                index = 0
                highest = ("sell", lowest[1], 0)

                while index < len(self.data):
                    if index < lowest[3]:
                        index += 1
                        continue
                    else:
                        if self.data[index][1] > highest[2]:
                            highest = (
                                "sell",
                                self.data[index][0],
                                self.data[index][1]
                                )
                    index += 1
            count += 1
            total = highest[2]-lowest[2]
            self.sums.append((lowest, highest, total))

        return self.sums

    def get_best_days_to_buy_and_sell(self):
        """Function for getting the best days to buy and sell bitcoin."""

        both = (
            ('buy', 1637971200.0, 1000000000.0, 24),
            ('sell', 1637971200.0, 0.0),
            0.0
            )

        if self.incorrect_input:
            text = "Incorrect input"

            return self.incorrect_input_to_json_form(
                tuple((
                    text,
                    self.data
                ))
            )

        for difference in self.get_price_differences():
            if difference[2] > both[2]:
                both = difference

        if self.one_day:
            text = ("Don't buy unless you want to sell on the same day")

            return self.buy_and_sell_dates_to_json_form(
                tuple((
                    text,
                    self.data[0][3],
                    self.data[0][3][:10],
                    self.data[0][3][11:],
                    str(self.get_date_from_timestamp(both[0][1]))[:10],
                    str(self.get_date_from_timestamp(both[1][1]))[:10],
                    str(self.get_date_from_timestamp(both[0][1]))[11:],
                    str(self.get_date_from_timestamp(both[1][1]))[11:],
                    int(both[0][2]),
                    int(both[1][2]),
                    both[2]
                ))
            )

        if both[2] <= 0:
            text = "Don't buy"

            return self.buy_and_sell_dates_to_json_form(
                tuple((
                    text,
                    self.data[0][3],
                    self.data[0][3][:10],
                    self.data[0][3][11:],
                    str(self.get_date_from_timestamp(both[0][1]))[:10],
                    str(self.get_date_from_timestamp(both[1][1]))[:10],
                    str(self.get_date_from_timestamp(both[0][1]))[11:],
                    str(self.get_date_from_timestamp(both[1][1]))[11:],
                    int(both[0][2]),
                    int(both[1][2]),
                    both[2]
                ))
            )
        else:
            text = (f"Buy date: "
                    f"{self.get_date_from_timestamp(both[0][1])[:10]}, "
                    f"Sell date: "
                    f"{self.get_date_from_timestamp(both[1][1])[:10]}")

            return self.buy_and_sell_dates_to_json_form(
                tuple((
                    text,
                    self.data[0][3],
                    self.data[0][3][:10],
                    self.data[0][3][11:],
                    str(self.get_date_from_timestamp(both[0][1]))[:10],
                    str(self.get_date_from_timestamp(both[1][1]))[:10],
                    str(self.get_date_from_timestamp(both[0][1]))[11:],
                    str(self.get_date_from_timestamp(both[1][1]))[11:],
                    int(both[0][2]),
                    int(both[1][2]),
                    both[2]
                ))
            )

    def incorrect_input_to_json_form(self, data):
        """
        Helper function that returns data from incorrect input.

        The data is returned in json form.
        """

        dictionary = {}
        dictionary2 = {}
        options = [
            "text", "input", "first_date", "second_date", "data"
            ]

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

    def incorrect_input_for_downward_trend_to_json_form(self, data):
        """
        Helper function for get_downward_trend().

        This function returns downward trend data in json form
        if the self.data only has data for one day.
        """

        dictionary = {}
        dictionary2 = {}
        options = [
            "text", "input", "first_date", "second_date", "data"
            ]

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
                                dictionary2[copy] = data[1][:10]
                            case "second_date":
                                dictionary2[copy] = data[1][11:]
                    dictionary[option] = dictionary2

        return dictionary

    def downward_trend_to_json_form(self, data):
        """
        Helper function for get_downward_trend().

        This function returns downward trend data in json form.
        """

        dictionary = {}
        dictionary2 = {}
        options = [
            "text", "input", "first_date", "second_date",
            "downward_trend_start_date", "downward_trend_end_date",
            "days", "data"
            ]

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
                            case "downward_trend_start_date":
                                dictionary2[copy] = data[4]
                            case "downward_trend_end_date":
                                dictionary2[copy] = data[5]
                            case "days":
                                dictionary2[copy] = data[6]
                    dictionary[option] = dictionary2

        return dictionary

    def highest_trading_volume_to_json_form(self, data):
        """
        Helper function for get_highest_trading_volume().

        This function returns highest_trading_volume data in json form.
        """

        dictionary = {}
        dictionary2 = {}
        options = [
            "text", "input", "first_date", "second_date",
            "highest_trading_volume_date", "highest_trading_volume_time",
            "highest_trading_volume", "data"
            ]

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
                            case "highest_trading_volume_time":
                                dictionary2[copy] = data[5]
                            case "highest_trading_volume":
                                dictionary2[copy] = data[6]
                    dictionary[option] = dictionary2

        return dictionary

    def bad_time_to_buy_to_json_form(self, data):
        """
        helper function for get_best_days_to_buy_and_sell().

        This function returns data from input dates
        that didn't have a good time to buy bitcoin.
        Thus neither sell it.

        The data is returned in JSON form.
        """

        dictionary = {}
        dictionary2 = {}
        options = [
            "text", "input", "first_date", "second_date", "buy_date",
            "sell_date", "buy_time", "sell_time", "buy_price", "sell_price",
            "profit", "data"
            ]

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

    def incorrect_input_for_buy_and_sell_dates_to_json_form(self, data):
        """
        Helper function for get_best_days_to_buy_and_sell().

        This function returns buy and sell date data
        if the self.data only has data for one day.

        The data is returned in json form.
        """

        dictionary = {}
        dictionary2 = {}
        options = [
            "text", "input", "first_date", "second_date", "buy_date",
            "sell_date", "buy_time", "sell_time", "buy_price", "sell_price",
            "profit", "data"
            ]

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

    def buy_and_sell_dates_to_json_form(self, data):
        """
        Helper function for get_best_days_to_buy_and_sell().

        This function returns buy and sell date data
        from input that has best days to buy and sell bitcoin.

        The data is returned in json form.
        """

        dictionary = {}
        dictionary2 = {}
        options = [
            "text", "input", "first_date", "second_date", "buy_date",
            "sell_date", "buy_time", "sell_time", "buy_price", "sell_price",
            "profit", "data"
            ]

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


if __name__ == "__main__":
    application = Application()

    application.update_data("13-03-2021|13-04-2021")
    #application.update_data("26-11-2021|27-11-2021")
    #application.update_data("01-11-2021|27-11-2021")
    #application.update_data("26-11-2020|27-11-2021")

    #This doesn't work yet
    #application.update_data("01-01-2018|27-11-2021")

    print("1.")
    print(application.get_downward_trend())
    print("2.")
    print(application.get_highest_trading_volume())
    print("3.")
    print(application.get_best_days_to_buy_and_sell())

    print("")

    # Don't buy test
    # application.update_data("26-11-2021|30-11-2021")
    # print("don't buy")
    # print(application.get_best_days_to_buy_and_sell())

    # print("")

    # Wrong input test
    # application.update_data("25-11-2021|24-11-2021")
    # print("Wrong input")
    # print("1.")
    # print(application.get_downward_trend())
    # print("2.")
    # print(application.get_highest_trading_volume())
    # print("3.")
    # print(application.get_best_days_to_buy_and_sell())

    # Funktions used in the application
    # ----------------------------------------------------
    # print("A")
    #print(application.get_timestamps_from_input("26-11-2021|28-11-2021"))
    # print("B")
    #print(application.get_date_from_timestamp(1257326176))
    # print("C")
    #print(application.get_highest_price_of_the_day(1257326176))
    # print("D")
    #print(application.get_lowest_price_of_the_day(1257326176))
    # print("E")
    #print(application.get_highest_prices(1257326176))
    # print("F")
    #print(application.get_lowest_prices(1257326176))
    # print("")
    # ----------------------------------------------------