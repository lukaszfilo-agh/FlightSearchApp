import constants as c
import requests

from datetime import datetime, timedelta

# Credits to gabsbruh at https://github.com/gabsbruh/Mini-projects/tree/main/39.flight-deals-alert


class FlightSearch:
    """
    Class responsible for requests to Amadeus and Ryanair API
    """

    def __init__(self) -> None:
        self.url_iata_codes = c.RYANAIR_URL_IATA_CODE
        self.url_flights_ryanair = c.RYANAIR_URL_FLIGHTS
        self.search_result = None

    def _get_iata_code(self, flight_data):
        # Ryanair API needs IATA code for airport not city.
        """
        Getting IATA codes for all airport avaible at origin or destination selected in flight_data dictionary
        """
        response = requests.get(url=self.url_iata_codes)
        origin = flight_data["origin"]
        destination = flight_data["destination"]

        origin_code = self._parse_iata_code(response, origin)
        flight_data['originLocationCode'] = origin_code

        if flight_data['destination'] != []:
            dest_code = self._parse_iata_code(response, destination)
            flight_data['destinationLocationCode'] = dest_code

    def _parse_iata_code(self, response: requests.Response, city: str):
        """
        Getting iata code from provided city
        """
        result = []
        try:
            for rel in response.json():
                if rel["city"]["name"] in city:
                    result.append(rel["code"])
                elif "macCity" in rel.keys():
                    if rel["macCity"]["name"] != rel["city"]["name"]:
                        if rel["macCity"]["name"] in city:
                            result.append(rel["code"])
            return result
        except:
            print('EXC')

    def flight_search(self, flight_data):
        """
        Filtering flights in Ryanair according to parameters in flight_data dictionary
        """
        self._get_iata_code(flight_data)
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
                    query_params['arrivalAirportIataCode'] = dest
                    response = requests.get(
                        url=self.url_flights_ryanair, params=query_params)
                    if self.search_result == {}:
                        self.search_result = response.json()
                    else:
                        self.search_result['fares'].extend(
                            response.json()['fares'])
            else:
                response = requests.get(
                    url=self.url_flights_ryanair, params=query_params)
                if self.search_result == {}:
                    self.search_result = response.json()
                else:
                    self.search_result['fares'].extend(
                        response.json()['fares'])
            outbound_date = outbound_date + timedelta(1)
            inbound_date = outbound_date + \
                timedelta(flight_data['durationOfStay'] - 1)
