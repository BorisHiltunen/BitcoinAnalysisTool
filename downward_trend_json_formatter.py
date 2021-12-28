"""
downward_trend_json_formatter.py:
Contains a helper class for downward_trend.py.
"""


class DownwardTrendFormatter:
    """Contains two helper functions for downward_trend.py."""

    def incorrect_downward_trend_to_json_form(self, data):
        """
        Helper function for downward_trend.py.

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
        Helper function for downward_trend.py.

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
