from flight_search import FlightSearch

from datetime import datetime, timedelta
from ryanair import Ryanair

api = Ryanair(currency="EUR")  # Euro currency, so could also be GBP etc. also
tomorrow = datetime.today().date() + timedelta(days=1)
tomorrow_1 = tomorrow + timedelta(days=1)

trips = api.get_cheapest_return_flights("DUB", tomorrow, tomorrow, tomorrow_1, tomorrow_1)

