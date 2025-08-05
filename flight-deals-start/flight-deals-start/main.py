#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from distutils.sysconfig import customize_compiler

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager
from datetime import datetime, timedelta
import time

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA = "BOS"

#Update codes in Google Sheet
for row in sheet_data:
    if sheet_data[0]["iataCode"] == "":
        row["iataCode"] = flight_search.get_code(row["city"])
        time.sleep(2)
print(f"sheet_data:\n {sheet_data}")

data_manager.destination_data = sheet_data
data_manager.update_codes()

#Get customer data
customer_data = data_manager.get_customer_emails()
customer_emails = [row["Email Address"] for row in customer_data]

#Search for flights
tmrw = datetime.now() + timedelta(days=1)
six_mon = datetime.now() + timedelta(days=(6*30))

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")

    flights = flight_search.check_flights(
        origin_code=ORIGIN_CITY_IATA,
        dest_code=destination['iataCode'],
        out_date=tmrw,
        return_date=six_mon
    )
    cheapest_flight = find_cheapest_flight(flights)

    print(f"{destination['city']}: ${cheapest_flight.price}")
    time.sleep(2)

    #Search for indirect flights
    if cheapest_flight.price == "N/A":
        print(f"No direct flight to {destination['city']}. Looking for indirect flights...")
        stopover_flights = flight_search.check_flights(
            origin_code=ORIGIN_CITY_IATA,
            dest_code=destination["iataCode"],
            out_date=tmrw,
            return_date=six_mon,
            is_direct=False
        )
        cheapest_flight = find_cheapest_flight(stopover_flights)
        print(f"Cheapest indirect flight price is: £{cheapest_flight.price}")

    #Send message for lower price available
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        # Customise the message depending on the number of stops
        if cheapest_flight.stops == 0:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly direct " \
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, " \
                      f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        else:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly " \
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, " \
                      f"with {cheapest_flight.stops} stop(s) " \
                      f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."

        print(f"Check your email. Lower price flight found to {destination['city']}!")

        notification_manager.send_whatsapp(message_body=message)
        notification_manager.send_emails(email_list=customer_emails, email_body=message)

