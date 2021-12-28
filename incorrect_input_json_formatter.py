"""incorrect_input_to_json_form.py: Contains one helper function."""


def incorrect_input_to_json_form(data):
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
