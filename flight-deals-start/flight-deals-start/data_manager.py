import requests
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from pprint import pprint

#load env vars from .env file
load_dotenv()

class DataManager:
    #This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self._user = os.environ["SHEETY_USER"],
        self._password = os.environ["SHEETY_PASS"],
        self.prices_endpoint = os.environ["SHEETY_PRICES_ENDPOINT"]
        self.users_endpoint = os.environ["SHEETY_USERS_ENDPOINT"]
        self.authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        response = requests.get(url=self.prices_endpoint, auth=self.authorization)
        result = response.json()
        self.destination_data = result["prices"]
        return self.destination_data

    def update_codes(self):
        for row in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": row["iataCode"]
                }
            }
            response = requests.put(url=f"{self.prices_endpoint}/{row['id']}", json=new_data, auth=self.authorization)
            print(response.text)

    def get_customer_emails(self):
        response = requests.get(url=self.users_endpoint, auth=self.authorization)
        result = response.json()
        self.customer_data = result["users"]
        return self.customer_data