"""application_data.py: Initializes and returns the needed attributes"""

from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

data = []
buy_date_indices = []
sums = []
incorrect_input = False
one_day = False
under_90_days = False
over_90_days = False


class ApplicationData:
    """
    Function that initializes
    and returns the needed attributes for other classes.
    """

    def __init__(self):
        self.data = []
        self.buy_date_indices = []
        self.sums = []
        self.incorrect_input = False
        self.one_day = False
        self.under_90_days = False
        self.over_90_days = False

    def get_application_data(self):
        """Function that returns application's data for other classes."""

        return self.data

    def get_application_buy_date_indices(self):
        """
        Function that returns application's buy_date_indices
        for other classes.
        """

        return self.buy_date_indices

    def get_application_sums(self):
        """
        Function that returns application's buy and sell date price sums
        for other classes.
        """

        return self.sums

    def get_application_incorrect_input(self):
        """
        Function that returns application's
        incorrect_input boolean for other classes.

        The boolean shows whether the input is correct or not.
        """

        return self.incorrect_input

    def get_application_one_day(self):
        """
        Function that returns application's
        one_day boolean for other classes.

        The boolean shows whether the input's day difference is one or not.
        """

        return self.one_day

    def get_application_under_90_days(self):
        """
        Function that returns application's
        one_day boolean for other classes.

        The boolean shows whether the input's day difference
        is under 90 or not.
        """

        return self.under_90_days

    def get_application_over_90_days(self):
        """
        Function that returns application's
        one_day boolean for other classes.

        The boolean shows whether the input's day difference
        is over 90 or not.
        """

        return self.over_90_days
