from flight_search import FlightSearch




flight_data = {
    'origin': 'London',
    'originLocationCode': None,
    'destinations': ['New York'],
    'destinationsLocationCodes': [],
    'departureDate' : '2024-08-20',
    'returnDate': '2024-08-30',
    'durationOfStay': 5,
    'adults': 2,
    'currencyCode': 'PLN',
    'max': 50
}

fs = FlightSearch()
fs.flight_search(flight_data)

print(fs.url_flights)
