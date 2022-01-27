"""
main.py:
Contains the whole application except Flask side of the project.
"""

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

        now = datetime.now(timezone.utc)
        now_time = now.replace(tzinfo=timezone.utc)
        now_timestamp = now_time.timestamp()

        future_condition1 = now.replace(tzinfo=None) - \
            self.get_date_from_input(dates)[0].replace(tzinfo=None)
        future_condition2 = now.replace(tzinfo=None) - \
            self.get_date_from_input(dates)[1].replace(tzinfo=None)

        if dates[2] == "-" or str(future_condition1)[0] == "-" or \
                str(future_condition2)[0] == "-":
            self.incorrect_input = True
            self.data.append(dates)
            return

        date1 = self.get_timestamps_from_input(dates)[0]
        date2 = self.get_timestamps_from_input(dates)[1]

        if date1 > date2 or date1 < 1364428800.0:
            self.incorrect_input = True
            self.data.append(dates)
            return

        if date2 != now_timestamp:
            date2 += 3600
            reducer += 3600

        data = cg.get_coin_market_chart_range_by_id(id='bitcoin',
                                                    vs_currency='eur',
                                                    from_timestamp=date1,
                                                    to_timestamp=date2)

        for price in data["prices"]:
            prices.append((price[0], price[1]))
        for volume in data["total_volumes"]:
            total_volumes.append((volume[0], volume[1]))

        count = 0

        if now_timestamp-date2 > 113666279.31145096:
            if (date2-reducer)-date1 <= 86400:
                self.one_day = True
            elif (date2-reducer)-date1 <= 7862400:
                self.under_90_days = True
            else:
                self.over_90_days = True
            while count < len(total_volumes):
                self.data.append(
                    tuple((
                        total_volumes[count][0],
                        prices[count][1],
                        total_volumes[count][1],
                        dates
                    ))
                )
                count += 1
        else:
            if (date2-reducer)-date1 <= 86400:
                self.one_day = True
                while count < len(total_volumes):
                    self.data.append(
                        tuple((
                            total_volumes[count][0],
                            prices[count][1],
                            total_volumes[count][1],
                            dates
                        ))
                    )
                    count += 1

            elif (date2-reducer)-date1 <= 7862400:
                self.under_90_days = True
                while count < len(total_volumes):
                    self.data.append(
                        tuple((
                            total_volumes[count][0],
                            prices[count][1],
                            total_volumes[count][1],
                            dates
                        ))
                    )
                    count += 1
            else:
                self.over_90_days = True
                while count < len(total_volumes):
                    self.data.append(
                        tuple((
                            total_volumes[count][0],
                            prices[count][1],
                            total_volumes[count][1],
                            dates
                        ))
                    )
                    count += 1

    def get_timestamps_from_input(self, dates: str):
        """Helper function that returns tuple containing two timestamps."""

        string_to_date1 = datetime.fromisoformat(dates[:10])
        string_to_date2 = datetime.fromisoformat(dates[11:])

        utc_time1 = string_to_date1.replace(tzinfo=timezone.utc)
        utc_time2 = string_to_date2.replace(tzinfo=timezone.utc)

        utc_timestamp1 = utc_time1.timestamp()
        utc_timestamp2 = utc_time2.timestamp()

        return (utc_timestamp1, utc_timestamp2)

    def get_date_from_timestamp(self, timestamp):
        """Helper function that converts timestamp into a date."""

        date = datetime.fromtimestamp(timestamp / 1e3)
        return date

    def get_date_from_input(self, dates: str):
        """Helper function that converts input to datetime."""

        string_to_date1 = datetime.fromisoformat(dates[:10])
        string_to_date2 = datetime.fromisoformat(dates[11:])

        return (string_to_date1, string_to_date2)

    def datetime_object_from_timestamp(self, timestamp):
        """Helper function that converts timestamp into a datetime_object."""

        compare_date = self.get_date_from_timestamp(
            timestamp).strftime("%Y-%m-%d, %H:%M:%S")
        year = compare_date[:4]
        month = compare_date[5:7]
        day = compare_date[8:10]

        datetime_object = datetime(int(year), int(month), int(day))

        return datetime_object

    def get_highest_prices(self, timestamp):
        """Helper function that returns the highest prices as a list"""

        highest = (self.data[0][0], 0.0)
        prices = []
        count = 0

        for price in self.data:

            date = self.datetime_object_from_timestamp(timestamp)
            compare_date = self.datetime_object_from_timestamp(price[0])

            difference = compare_date - date

            if str(difference)[0] == "1":
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
        else:
            highest_prices = self.get_highest_prices(start)

            if self.one_day:
                text = ("0 days since we are only looking at 1 day "
                        "thus we can't compare day's highest prices")

                return self.incorrect_input_for_downward_trend_to_json_form(
                    tuple((
                        text,
                        self.data[0][3]
                    ))
                )
            elif self.under_90_days:
                for count, value in enumerate(highest_prices):
                    if count == len(highest_prices)-1:
                        if end_timestamp == 0:
                            end_timestamp = value[0]
                        chosen_price_quantities.append((start_timestamp,
                                                        end_timestamp,
                                                        len(chosen_prices)))
                        start_timestamp = 0
                        chosen_prices = []
                    else:
                        if value[1] > highest_prices[count+1][1]:
                            if start_timestamp == 0:
                                start_timestamp = value[0]
                            if value[1] not in chosen_prices:
                                chosen_prices.append(value[1])
                            chosen_prices.append(highest_prices[count+1][1])
                            end_timestamp = 0
                        else:
                            if end_timestamp == 0:
                                end_timestamp = value[0]
                            chosen_price_quantities.append((start_timestamp,
                                                            end_timestamp,
                                                            len(chosen_prices)
                                                            ))
                            start_timestamp = 0
                            chosen_prices = []
                    count += 1
            elif self.over_90_days:
                for count, value in enumerate(self.data):
                    if count == len(self.data)-1:
                        if end_timestamp == 0:
                            end_timestamp = value[0]
                        chosen_price_quantities.append((start_timestamp,
                                                        end_timestamp,
                                                        len(chosen_prices)))
                        start_timestamp = 0
                        chosen_prices = []
                    else:
                        if value[1] > self.data[count+1][1]:
                            if start_timestamp == 0:
                                start_timestamp = value[0]
                            if value[1] not in chosen_prices:
                                chosen_prices.append(value[1])
                            chosen_prices.append(self.data[count+1][1])
                            end_timestamp = 0
                        else:
                            if end_timestamp == 0:
                                end_timestamp = value[0]
                            chosen_price_quantities.append((start_timestamp,
                                                            end_timestamp,
                                                            len(chosen_prices)
                                                            ))
                            start_timestamp = 0
                            chosen_prices = []
                    count += 1

        for quantity in chosen_price_quantities:
            if quantity[2] > most[2]:
                most = quantity

        date1 = self.get_date_from_timestamp(most[0]).strftime("%Y-%m-%d")
        date2 = self.get_date_from_timestamp(most[1]).strftime("%Y-%m-%d")

        text = (
                f"In bitcoin’s historical data from CoinGecko, "
                f"the price decreased {most[2]} days in a row "
                f"from {date1} "
                f"to {date2}"
                ).replace("\u2019", "'")

        return self.downward_trend_to_json_form(
            tuple((
                text,
                self.data[0][3],
                self.data[0][3][:10],
                self.data[0][3][11:],
                date1,
                date2,
                most[2]
            ))
        )

    def get_highest_trading_volume(self):
        """
        Function that returns highest trading volume
        from the given dates.
        """

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

        date = self.get_date_from_timestamp(
            highest[0]).strftime("%Y-%m-%d %H:%M:%S")

        text = (f"Highest trading volume date: "
                f"{date}, "
                f"Highest trading volume: {highest[1]}")

        return self.highest_trading_volume_to_json_form(
            tuple((
                text,
                self.data[0][3],
                self.data[0][3][:10],
                self.data[0][3][11:],
                date[:10],
                date[11:],
                highest[1]
            ))
        )

    def get_sum_differences(self):
        """
        Helper function that returns sum differences
        for buy_and_sell_dates.py.
        """

        both = {
            "buy_price": (0.0, 1000000000.0),
            "sell_price": (0.0, -1000000000.0),
            "profit": -1000000000.0
            }
        self.sums = []
        count = 0

        while count < len(self.data):
            if count == len(self.data)-1 and \
                    both["sell_price"][0] > both["buy_price"][0]:
                if self.data[count][1] > both["sell_price"][1]:
                    both["sell_price"] = (
                        self.data[count][0],
                        self.data[count][1]
                        )
                    both["profit"] = both["sell_price"][1] - \
                        both["buy_price"][1]
                    self.sums.append(both)
                else:
                    both["profit"] = both["sell_price"][1] - \
                        both["buy_price"][1]
                    self.sums.append(both)
            else:
                if self.data[count][1] < both["buy_price"][1]:
                    if count > 0:
                        both["profit"] = both["sell_price"][1] - \
                            both["buy_price"][1]
                        self.sums.append(both)
                        both = {
                            "buy_price": (0.0, 1000000000.0),
                            "sell_price": (0.0, -1000000000.0),
                            "profit": -1000000000.0
                            }
                        both["buy_price"] = (
                            self.data[count][0],
                            self.data[count][1]
                            )
                    else:
                        both["buy_price"] = (
                            self.data[count][0],
                            self.data[count][1]
                            )
                if self.data[count][1] > both["sell_price"][1] and \
                        self.data[count][0] >= both["buy_price"][0]:
                    both["sell_price"] = (
                        self.data[count][0],
                        self.data[count][1]
                        )
            count += 1

        return self.sums

    def get_best_days_to_buy_and_sell(self):
        """Function for getting the best days to buy and sell bitcoin."""

        both = {
            "buy_price": (0.0, 1000000000.0),
            "sell_price": (0.0, -1000000000.0),
            "profit": -1000000000.0
            }
        buy_timestamp = 0.0
        sell_timestamp = 0.0

        if self.incorrect_input:
            text = "Incorrect input"

            return self.incorrect_input_to_json_form(
                tuple((
                    text,
                    self.data
                ))
            )

        for difference in self.get_sum_differences():
            if difference["profit"] > both["profit"]:
                both = difference

        buy_timestamp = both["buy_price"][0]
        sell_timestamp = both["sell_price"][0]

        date = self.get_date_from_timestamp(
            buy_timestamp).strftime("%Y-%m-%d %H:%M:%S")
        date2 = self.get_date_from_timestamp(
            sell_timestamp).strftime("%Y-%m-%d %H:%M:%S")

        if buy_timestamp == 0.0:
            text = "Something went wrong"

            return self.incorrect_input_to_json_form(
                tuple((
                    text,
                    [self.data[0][3]]
                ))
            )

        elif both["profit"] <= 0:
            text = "Don't buy"

            return self.buy_and_sell_dates_to_json_form(
                tuple((
                    text,
                    self.data[0][3],
                    self.data[0][3][:10],
                    self.data[0][3][11:],
                    date[:10],
                    date2[:10],
                    date[11:],
                    date2[11:],
                    both["buy_price"][1],
                    both["sell_price"][1],
                    both["profit"]
                ))
            )

        elif self.one_day:
            text = ("Don't buy unless you want to sell on the same day")

            return self.buy_and_sell_dates_to_json_form(
                tuple((
                    text,
                    self.data[0][3],
                    self.data[0][3][:10],
                    self.data[0][3][11:],
                    date[:10],
                    date2[:10],
                    date[11:],
                    date2[11:],
                    both["buy_price"][1],
                    both["sell_price"][1],
                    both["profit"]
                ))
            )
        else:
            text = (f"Buy date: "
                    f"{date[:10]}, "
                    f"Sell date: "
                    f"{date2[:10]}")

            return self.buy_and_sell_dates_to_json_form(
                tuple((
                    text,
                    self.data[0][3],
                    self.data[0][3][:10],
                    self.data[0][3][11:],
                    date[:10],
                    date2[:10],
                    date[11:],
                    date2[11:],
                    both["buy_price"][1],
                    both["sell_price"][1],
                    both["profit"]
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

    #application.update_data("2021-11-26|2021-11-27")

    #application.update_data("2021-09-01|2021-11-27")
    #application.update_data("2021-10-01|2021-11-27")
    #application.update_data("2021-11-01|2021-11-27")

    #application.update_data("2020-11-26|2021-11-27")
    #application.update_data("2013-04-28|2021-12-29")
    # Wrong input test
    #application.update_data("2013-04-28|2013-04-28")
    #application.update_data("25-11-2021|24-11-2021")
    #application.update_data("2021-11-25|2021-11-24")

    #application.update_data("2022-01-10|2022-01-11")

    application.update_data("2014-11-25|2021-11-30")

    print("1.")
    print(application.get_downward_trend())
    print("2.")
    print(application.get_highest_trading_volume())
    print("3.")
    print(application.get_best_days_to_buy_and_sell())

    #print("")

    # print("")

    # Funktions used in the application
    # ----------------------------------------------------
    # print("A")
    #print(application.get_timestamps_from_input2("26-11-2021|28-11-2021"))
    #print(application.get_timestamps_from_input("2021-11-26|2021-11-28"))
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
