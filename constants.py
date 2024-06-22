import os

# Amadeus API Key's
AMADEUS_API_KEY = os.environ.get("AMADEUS_API_KEY")
AMADEUS_API_SECRET = os.environ.get("AMADEUS_API_SECRET")
AMADEUS_TOKEN = 'https://test.api.amadeus.com/v1/security/oauth2/token'
AMADEUS_URL_IATA_CODE = 'https://test.api.amadeus.com/v1/reference-data/locations/cities'
AMADEUS_URL_FLIGHTS = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
RYANAIR_URL_FLIGHTS = 'https://services-api.ryanair.com/farfnd/v4/roundTripFares'

