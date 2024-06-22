from flight_search import FlightSearch
from datetime import datetime
import pprint 
pp = pprint.PrettyPrinter(indent=4)

flight_data = {
    'origin': 'Krakow',
    'originLocationCode': [],
    'destination': ['London'],
    'destinationLocationCode': [],
    'departureDate' : '2024-08-21',
    'returnDate': '2024-08-31',
    'durationOfStay': 5,
    'adults': 2,
    'currencyCode': 'PLN',
    'max': 50
}

fs = FlightSearch()
fs.flight_search_ryanair(flight_data)

dict = fs.search_result
pp.pprint(dict['fares'])

# for row, fare in enumerate(dict['fares']):
#     pp.pprint(fare)
#     print(fare['outbound']['departureAirport']['name'])
#     dep_date = datetime.fromisoformat(fare['outbound']['departureDate'])
#     print(dep_date)
#     print(fare['outbound']['arrivalAirport']['name'])
#     arr_date = datetime.fromisoformat(fare['outbound']['arrivalDate'])
#     print(arr_date)
#     print(fare['outbound']['flightNumber'])
#     print(fare['inbound']['departureAirport']['name'])
#     dep_date = datetime.fromisoformat(fare['inbound']['departureDate'])
#     print(dep_date)
#     print(fare['inbound']['arrivalAirport']['name'])
#     arr_date = datetime.fromisoformat(fare['inbound']['arrivalDate'])
#     print(arr_date)
#     print(fare['inbound']['flightNumber'])
#     print(fare['summary']['price']['value'])
#     print(fare['summary']['price']['currencyCode'])
#     print(row)

    
