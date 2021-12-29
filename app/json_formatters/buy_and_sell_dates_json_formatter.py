"""
buy_and_sell_dates_json_formatter.py:
Contains a helper class for buy_and_sell_dates.py.
"""


class TradingFormatter:
    """
    Class that contains three helper functions
    for buy_and_sell_dates.py.
    """

    def trading_on_the_same_day_to_json_form(self, data):
        """
        Helper function for buy_and_sell_dates.py.

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

    def bad_time_to_buy_to_json_form(self, data):
        """
        Helper function for buy_and_sell_dates.py.

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

    def buy_and_sell_dates_to_json_form(self, data):
        """
        Helper function for buy_and_sell_dates.py.

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
