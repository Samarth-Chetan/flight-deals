# ✈ Flight Deal Tracker

## 📌 Overview
This project is a **Flight Deal Tracker** that automatically searches for cheap flights from a fixed origin city (Boston by default) to a list of destinations stored in a Google Sheet.  
If it finds a price lower than your target price, it sends **WhatsApp** and **email alerts** to all subscribed users.

The system integrates with:
- **Google Sheets** via the Sheety API (to store destinations, target prices, and customer emails)
- **Amadeus API** (to search for flights)
- **Twilio API** (to send WhatsApp messages)
- **SMTP** (to send email notifications)

---

## ⚙ Features
- Fetch destination data and target prices from a Google Sheet.
- Automatically update missing IATA airport codes.
- Search for flights within a given date range (direct and indirect).
- Find the **cheapest available flight** for each destination.
- Send alerts to customers via:
  - **WhatsApp** (Twilio)
  - **Email** (SMTP)

---

## 📂 Project Structure
- main.py # Orchestrates the whole process
- data_manager.py # Manages data from Google Sheets
- flight_search.py # Handles API calls to Amadeus for flights and IATA codes
- flight_data.py # Finds and structures the cheapest flight
- notification_manager.py # Sends notifications via WhatsApp and email
- .env # Stores sensitive environment variables (not committed)

## 🛠 Requirements
- Python 3.8+
- [Amadeus API](https://developers.amadeus.com/)
- [Twilio API](https://www.twilio.com/)
- [Sheety API](https://sheety.co/)
- SMTP server access (e.g., Gmail)
