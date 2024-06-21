from flight_search import FlightSearch

flight_data = {
    'origin': 'Krakow',
    'originLocationCode': 'KRK',
    'destinations': ['London'],
    'destinationsLocationCodes': ['STN'],
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
print(dict)
