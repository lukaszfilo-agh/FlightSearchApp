import constants as c
import requests

from urllib.parse import urlencode, urlunparse

from datetime import datetime, timedelta

# Credits to gabsbruh at https://github.com/gabsbruh/Mini-projects/tree/main/39.flight-deals-alert
# Ryanair API needs IATA code for airport not city.


class FlightSearch:
    def __init__(self) -> None:
        self.api_key = c.AMADEUS_API_KEY
        self.secret_key = c.AMADEUS_API_SECRET
        self.url_token = c.AMADEUS_TOKEN
        self.url_iata_codes = c.AMADEUS_URL_IATA_CODE
        self.url_flights_amadeus = c.AMADEUS_URL_FLIGHTS
        self.url_flights_ryanair = c.RYANAIR_URL_FLIGHTS
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

    def _get_iata_code_amadeus(self, flight_data):
        data1 = {
            "keyword": flight_data['origin'],
            "max": 1,
            "include": "AIRPORTS",
        }
        response = requests.get(url=self.url_iata_codes,
                                params=data1, headers=self.api_header)
        # print(response.text)
        # print(response.url)
        try:
            flight_data['originLocationCode'].append(response.json()[
                "data"][0]['iataCode'])
        except (KeyError, IndexError):
            return "Not Found."

        for dest in flight_data['destination']:
            data2 = {
                "keyword": dest,
                "max": 1,
                "include": "AIRPORTS",
            }
            response = requests.get(
                url=self.url_iata_codes, params=data2, headers=self.api_header)
            # print(response.text)
            try:
                flight_data['destinationLocationCode'].append(
                    response.json()["data"][0]['iataCode'])
                return None
            except (KeyError, IndexError):
                return "Not Found."

    def _get_iata_code_ryanair(self, flight_data):
        data1 = {
            "keyword": flight_data['origin'],
            "max": 1,
            "include": "AIRPORTS",
        }
        response = requests.get(url=self.url_iata_codes,
                                params=data1, headers=self.api_header)
        try:
            for rel in response.json()["data"][0]["relationships"]:
                if rel["type"] == "Airport":
                    flight_data['originLocationCode'].append(rel["id"])
        except (KeyError, IndexError):
            return "Not Found."

        if flight_data['destination'] != []:
            for dest in flight_data['destination']:
                data2 = {
                    "keyword": dest,
                    "max": 1,
                    "include": "AIRPORTS",
                }
                response = requests.get(
                    url=self.url_iata_codes, params=data2, headers=self.api_header)
                try:
                    for rel in response.json()["data"][0]["relationships"]:
                        if rel["type"] == "Airport":
                            flight_data['destinationLocationCode'].append(
                                rel["id"])
                except (KeyError, IndexError):
                    return "Not Found."

    def flight_search_amadeus(self, flight_data):
        self._get_iata_code_amadeus(flight_data)

        query_params = {
            'originLocationCode': flight_data['originLocationCode'][0],
            'destinationLocationCode': flight_data['destinationLocationCode'][0],
            'departureDate': flight_data['departureDate'],
            'returnDate': flight_data['returnDate'],
            'adults': flight_data['adults'],
            'nonStop': 'true',
            'currencyCode': flight_data['currencyCode'],
            'max': flight_data['max']
        }

        response = requests.get(
            url=self.url_flights_amadeus, params=query_params, headers=self.api_header)
        # print(response.text)

        self.search_result = response.json()

        return

    def flight_search_ryanair(self, flight_data):
        self._get_iata_code_ryanair(flight_data)
        departure_from = datetime.fromisoformat(flight_data['departureDate'])
        arrival_to = datetime.fromisoformat(flight_data['returnDate'])
        outbound_date = departure_from
        inbound_date = outbound_date + \
            timedelta(flight_data['durationOfStay'] - 1)
        self.search_result = dict()
        while outbound_date != arrival_to - timedelta(flight_data['durationOfStay']-2):
            query_params = {
                'departureAirportIataCode': flight_data['originLocationCode'],
                'outboundDepartureDateFrom': outbound_date.strftime('%Y-%m-%d'),
                'outboundDepartureDateTo': outbound_date.strftime('%Y-%m-%d'),
                'inboundDepartureDateFrom': inbound_date.strftime('%Y-%m-%d'),
                'inboundDepartureDateTo': inbound_date.strftime('%Y-%m-%d'),
                'adults': flight_data['adults'],
                'currencyCode': flight_data['currencyCode'],
                'max': flight_data['max']
            }
            if flight_data['destinationLocationCode'] != []:

                for idx, dest in enumerate(flight_data['destinationLocationCode']):
                    query_params['arrivalAirportIataCode'] = dest,
                    response = requests.get(
                        url=self.url_flights_ryanair, params=query_params)
                    if self.search_result == {}:
                        self.search_result = response.json()
                    else:
                        self.search_result['fares'].extend(
                            response.json()['fares'])
                    # self.search_result.update(response.json())
                    # print(response.text)
            else:
                response = requests.get(
                    url=self.url_flights_ryanair, params=query_params)
                if self.search_result == {}:

                    self.search_result = response.json()
                else:
                    self.search_result['fares'].extend(
                        response.json()['fares'])
            # print(self.search_result)
            outbound_date = outbound_date + timedelta(1)
            inbound_date = outbound_date + \
                timedelta(flight_data['durationOfStay'] - 1)
        # print(response.url)

        # print(self.search_result)
