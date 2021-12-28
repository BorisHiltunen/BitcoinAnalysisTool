"""trading_volume_json_formatter.py: Contains one helper function."""


def highest_trading_volume_to_json_form(data):
    """
    Helper function for highest_trading_volume.py.

    This function returns highest trading volume data in json form.
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
