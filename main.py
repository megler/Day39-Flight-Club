# flightClub.py
#
# Python Bootcamp Day 39-40 - Flight Club
# Usage:
#      Query Kiwi.com for flight info using cities saved in Google Sheet. Sheety
# API used to add/update info on Google Sheet.
#
# Marceia Egler December 20, 2021

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from flight_data import FlightData
from customer import Customer

data_manager = DataManager()
flight_search = FlightSearch()
notifications = NotificationManager()
data = FlightData()
customer = Customer()

# If there are new cities in the spreadsheet, run this to add the proper IATA code.
# data_manager.check_city_codes()

# Uncomment this if you want to start allowing customers to register
# customer.add_customer()

# Uncomment this if you want to check all prices on the spreadsheet, but not
# send notifications.
# flight_search.price_check()

# This will check prices and if new price is lower than saved price will text
# and email customer.
notifications.send_notification()
