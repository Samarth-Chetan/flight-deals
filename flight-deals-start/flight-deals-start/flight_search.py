import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

AM_ENDPOINT = "https://test.api.amadeus.com/v"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self):
        self._api_key = os.environ["AM_API_KEY"]
        self._api_secret = os.environ["AM_SECRET"]
        self._token = self._get_new_token()
        self.code = ""

    def _get_new_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }
        response = requests.post(url=f"{AM_ENDPOINT}1/security/oauth2/token", headers=header, data=body)

        # New bearer token. Typically expires in 1799 seconds (30min)
        print(f"Your token is {response.json()['access_token']}")
        print(f"Your token expires in {response.json()['expires_in']} seconds")
        return response.json()['access_token']

    def get_code(self, city_name):
        print(f"Using this token to get destination {self._token}")
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS",
        }

        response = requests.get(url=f"{AM_ENDPOINT}1/reference-data/locations/cities", headers=headers, params=query)
        print(f"Status code {response.status_code}. Airport IATA: {response.text}")

        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"

        return code

    def check_flights(self, origin_code, dest_code, out_date, return_date, is_direct=True):
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": origin_code,
            "destinationLocationCode": dest_code,
            "departureDate": out_date.strftime("%Y-%m-%d"),
            "returnDate": return_date.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true" if is_direct else "false",
            "currencyCode": "USD",
            "max": "10",
        }

        response = requests.get(url=f"{AM_ENDPOINT}2/shopping/flight-offers", headers=headers, params=query)

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None

        return response.json()
