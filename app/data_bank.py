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
