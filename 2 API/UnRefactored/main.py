#information about the code here

from datetime import datetime, timezone
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()


class Application:
    def __init__(self):
        self.data = []
        self.buy_date_indices = []
        self.sums = []
        self.amount = 0
        self.incorrect_input = False

    def update_data(self, dates: str):
        """Function for getting data by day with start and finish dates."""

        self.data = []
        self.buy_date_indices = []
        self.sums = []
        prices = []
        total_volumes = []
        self.amount = 0
        count = 0
        reducer = 0
        seconds = 0

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
            reducer += 3600

        data = cg.get_coin_market_chart_range_by_id(id='bitcoin',
                                                    vs_currency='eur',
                                                    from_timestamp=date1,
                                                    to_timestamp=date2)

        for price in data["prices"]:
            prices.append(price[1])
        for price in data["total_volumes"]:
            total_volumes.append(price[1])

        if (date2-reducer)-date1 < 7862400:
            while count < len(prices):
                if seconds == 0 or seconds == 86400:
                    self.data.append(
                        tuple((
                            date1,
                            prices[count],
                            total_volumes[count],
                            dates
                        ))
                    )
                    date1 += 86400
                    seconds = 0
                count += 1
                seconds += 3600
        else:
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

    def get_timestamps_from_dates(self, dates: str):
        """Helper function that returns tuple containing two timestamps."""

        year1 = f"{dates[6]}{dates[7]}{dates[8]}{dates[9]}"
        month1 = f"{dates[3]}{dates[4]}"
        day1 = f"{dates[0]}{dates[1]}"

        year2 = f"{dates[17]}{dates[18]}{dates[19]}{dates[20]}"
        month2 = f"{dates[14]}{dates[15]}"
        day2 = f"{dates[11]}{dates[12]}"

        date1_in_correct_form = f"{year1}-{month1}-{day1}"
        date2_in_correct_form = f"{year2}-{month2}-{day2}"

        string_to_date1 = datetime.fromisoformat(date1_in_correct_form)
        string_to_date2 = datetime.fromisoformat(date2_in_correct_form)

        utc_time1 = string_to_date1.replace(tzinfo=timezone.utc)
        utc_time2 = string_to_date2.replace(tzinfo=timezone.utc)

        utc_timestamp1 = utc_time1.timestamp()
        utc_timestamp2 = utc_time2.timestamp()

        return (utc_timestamp1, utc_timestamp2)

    def get_timestamp_from_date(self, timestamp):
        """helper function that converts timestamp into a date."""

        date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
        return date

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

        if self.incorrect_input:
            text = "Incorrect input"
            return self.incorrect_input_to_json_form(
                tuple((
                    text,
                    self.data
                ))
            )

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

        text = (f"In bitcoin’s historical data from CoinGecko, "
                f"the price decreased {most[2]} days in a row "
                f"from {self.data[0][3][:10]} "
                f"to {self.data[0][3][11:]}".replace("\u2019", "'"))

        return self.downward_trend_to_json_form(
            tuple((
                text,
                self.data[0][3],
                self.data[0][3][:10],
                self.data[0][3][11:],
                str(self.get_timestamp_from_date(most[0])),
                str(self.get_timestamp_from_date(most[1])),
                most[2]
            ))
        )

    def get_highest_trading_volume(self):
        """Function that returns HighestTradingVolume from the given dates."""

        if self.incorrect_input:
            text = "Incorrect input"
            return self.incorrect_input_to_json_form(
                tuple((
                    text,
                    self.data
                ))
            )

        highest = ("", 0.0)

        for volume in self.data:
            if volume[2] > highest[1]:
                highest = (volume[0], volume[2])

        # Think about how to express this
        text = (f"{str(self.get_timestamp_from_date(highest[0]))[:10]}, "
                f"{highest[1]}")

        return self.highest_trading_volume_to_json_form(
            tuple((
                text,
                self.data[0][3],
                self.data[0][3][:10],
                self.data[0][3][11:],
                str(self.get_timestamp_from_date(highest[0]))[:10],
                str(self.get_timestamp_from_date(highest[0]))[11:],
                highest[1]
            ))
        )

    def get_price_differences(self):
        """
        helper function that returns price differences
        for get_best_days_to_buy_and_sell().
        """

        count = 0

        lowest = ("buy", self.data[0][0], 1000000000, 0)

        while count < len(self.data):
            if count in self.buy_date_indices:
                count += 1
                continue
            else:
                if self.data[count][1] < lowest[2]:
                    lowest = (
                        "buy",
                        self.data[count][0],
                        self.data[count][1],
                        count
                        )
            count += 1

        self.buy_date_indices.append(lowest[3])

        count = 0
        highest = ("sell", lowest[1], 0)

        while count < len(self.data):
            if count < lowest[3]:
                count += 1
                continue
            else:
                if self.data[count][1] > highest[2]:
                    highest = (
                        "sell",
                        self.data[count][0],
                        self.data[count][1]
                        )
            count += 1

        if len(self.sums) == len(self.data):
            return self.sums
        else:
            sum = highest[2]-lowest[2]
            self.sums.append((lowest, highest, sum))
            return self.get_price_differences()

    def get_best_days_to_buy_and_sell(self):
        """Function for getting the best days to buy and sell bitcoin."""

        if self.incorrect_input:
            text = "Incorrect input"

            return self.incorrect_input_to_json_form(
                tuple((
                    text,
                    self.data
                ))
            )

        both = (
            ('buy', 1637971200.0, 1000000000.0, 24),
            ('sell', 1637971200.0, 0.0),
            0.0
            )

        for difference in self.get_price_differences():
            if difference[2] > both[2]:
                both = difference

        if both[2] <= 0:
            # Think about how to express this
            text = "Don't buy"

            return self.buy_and_sell_dates_to_json_form(
                tuple((
                    text,
                    self.data[0][3],
                    self.data[0][3][:10],
                    self.data[0][3][11:],
                    str(self.get_timestamp_from_date(both[0][1]))[:10],
                    str(self.get_timestamp_from_date(both[1][1]))[:10],
                    int(both[0][2]),
                    int(both[1][2]),
                    both[2]
                ))
            )
        else:
            # Think about how to express this
            text = (f"{str(self.get_timestamp_from_date(both[0][1]))[:10]}, "
                    f"{str(self.get_timestamp_from_date(both[1][1]))[:10]}")

            return self.buy_and_sell_dates_to_json_form(
                tuple((
                    text,
                    self.data[0][3],
                    self.data[0][3][:10],
                    self.data[0][3][11:],
                    str(self.get_timestamp_from_date(both[0][1]))[:10],
                    str(self.get_timestamp_from_date(both[1][1]))[:10],
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
            "highest_trading_volume_date", "highest_trading_volume", "data"
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
                            case "highest_trading_volume":
                                dictionary2[copy] = data[5]
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
            "sell_date", "buy_price", "sell_price", "profit", "data"
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
                            case "buy_price":
                                dictionary2[copy] = data[6]
                            case "sell_price":
                                dictionary2[copy] = data[7]
                            case "profit":
                                dictionary2[copy] = data[8]
                    dictionary[option] = dictionary2

        return dictionary


if __name__ == "__main__":
    application = Application()

    # application.update_data("26-11-2020|27-11-2021")
    # application.update_data("01-11-2021|27-11-2021")
    application.update_data("01-11-2020|27-11-2021")
    print("first 1.")
    print(application.get_downward_trend())
    print("2.")
    print(application.get_highest_trading_volume())
    print("3.")
    print(application.get_best_days_to_buy_and_sell())

    print("")

    # Funktions used in the application
    # ----------------------------------------------------
    # print("A")
    # print(application.get_timestamps_from_dates("26-11-2021|28-11-2021"))
    # print("C")
    # print(application.get_timestamp_from_date(1257326176))
    # print("")
    # ----------------------------------------------------

    # application.update_data("25-11-2021|30-11-2021")

    # A) mission Funktions (DownWardTrend)
    # print("Downward")
    # print(application.get_downward_trend())

    # print("")

    # B) mission Funktions (HighestTradingVolume)
    # print("HighestTradingVolume")
    # print(application.get_highest_trading_volume())

    # print("")

    # C) mission Funktions (TimeMachine)

    # Buy and sell test
    # print("whenToBuyAndSell")
    # print(application.get_best_days_to_buy_and_sell())

    # print("")

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
