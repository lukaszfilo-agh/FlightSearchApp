import constants as c
import requests

from urllib.parse import urlencode, urlunparse

# Credits to gabsbruh at https://github.com/gabsbruh/Mini-projects/tree/main/39.flight-deals-alert


class FlightSearch:
    def __init__(self) -> None:
        self.api_key = c.AMADEUS_API_KEY
        self.secret_key = c.AMADEUS_API_SECRET
        self.url_token = c.AMADEUS_TOKEN
        self.url_iata_codes = c.AMADEUS_URL_IATA_CODE
        self.url_flights = None
        self.api_header = self._get_new_token()
        self.search_result = None

    def _get_new_token(self):
        head = {
            "content-type": 'application/x-www-form-urlencoded',
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key,
        }
        try:
            response = requests.post(
                url=self.url_token, data=data, headers=head)
        except:
            raise Exception(
                "You have reached the allowed number of API calls for today.")
        response = response.json()
        token = f"{response['token_type']} {response['access_token']}"
        updated_header = {"Authorization": token}

        return updated_header

    def _get_iata_code(self, flight_data):
        data1 = {
            "keyword": flight_data['origin'],
            "max": 1,
            "include": "AIRPORTS",
        }
        response = requests.get(url=self.url_iata_codes,
                                params=data1, headers=self.api_header)
        # print(response.text)
        try:
            flight_data['originLocationCode'] = response.json()[
                "data"][0]['iataCode']
        except (KeyError, IndexError):
            return "Not Found."

        for dest in flight_data['destinations']:
            data2 = {
                "keyword": dest,
                "max": 1,
                "include": "AIRPORTS",
            }
            response = requests.get(
                url=self.url_iata_codes, params=data2, headers=self.api_header)
            # print(response.text)
            try:
                flight_data['destinationsLocationCodes'].append(
                    response.json()["data"][0]['iataCode'])
                return None
            except (KeyError, IndexError):
                return "Not Found."

    def _parse_url_request(self, flight_data):
        # Base URL components
        scheme = 'https'
        netloc = 'test.api.amadeus.com'
        path = '/v2/shopping/flight-offers'
        params = ''
        fragment = ''

        # Query parameters
        query_params = {
            'originLocationCode': flight_data['originLocationCode'],
            'destinationLocationCode': flight_data['destinationsLocationCodes'][0],
            'departureDate': flight_data['departureDate'],
            'returnDate': flight_data['returnDate'],
            'adults': flight_data['adults'],
            'nonStop': 'false',
            'currencyCode': flight_data['currencyCode'],
            'max': flight_data['max']
        }

        # Encode the query parameters
        query_string = urlencode(query_params)
        # print("Encoded Query String:", query_string)

        # Build the complete URL
        self.url_flights = urlunparse(
            (scheme, netloc, path, params, query_string, fragment))
        # print("Complete URL:", self.url_flights)

    def flight_search(self, flight_data):
        self._get_iata_code(flight_data)
        self._parse_url_request(flight_data)

        response = requests.get(url=self.url_flights, headers=self.api_header)
        print(response.text)

        self.search_result = response

        pass
