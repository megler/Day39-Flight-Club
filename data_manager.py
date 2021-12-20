import json
import os
from dotenv import load_dotenv
import requests
from flight_data import FlightData

load_dotenv()


class DataManager:
    """This class is responsible for talking to the Google Sheet"""

    def __init__(self) -> None:
        self.sheety_endpoint = os.getenv("SHEETY_ENDPOINT")
        self.sheety_api = os.getenv("SHEETY_API_KEY")
        self.sheety_header = {
            "Authorization": self.sheety_api,
            "Content-Type": "application/json",
        }

    def update_sheet(self, params: json, rowid: int, sheet_tab: str):
        """Given a set of params, update Google Sheet"""
        requests.put(
            url=f"{self.sheety_endpoint}/{sheet_tab}/{rowid}",
            headers=self.sheety_header,
            json=params,
        )

    def new_row(self, params: json, sheet_tab: str):
        """Given a set of params, add a new row to a Google Sheet."""
        requests.post(
            url=f"{self.sheety_endpoint}/{sheet_tab}",
            headers=self.sheety_header,
            json=params,
        )

    def get_sheety_data(self, sheet_tab: str) -> dict:
        """Query the Google Sheet and return all data as a JSON object"""
        sheety_info = requests.get(
            url=f"{self.sheety_endpoint}/{sheet_tab}/",
            headers=self.sheety_header,
        )
        sheety_info.raise_for_status()
        sheety_data = sheety_info.json()
        return sheety_data

    def get_kiwi_city_iata_code(self, query: str) -> str:
        """Provide a city name as argument (query) and return IATA code"""
        flight_data = FlightData()
        params = {"term": query}
        kiwi_city_search = requests.get(
            url=flight_data.kiwi_locations,
            headers=flight_data.kiwi_header,
            params=params,
        )
        kiwi_city_search.raise_for_status()
        kiwi_cities = kiwi_city_search.json()
        return kiwi_cities["locations"][0]["code"]

    def check_city_codes(self) -> None:
        """If no IATA code present in Google Sheet, run get_kiwi_city_iata_code(city_name) and fill cell with code.
        WARNING: ANY NEW CITY ADDED TO THE SHEET NEEDS THE PRICE SET TO AN INTEGER (DEFAULT 0) OR CITY WILL NOT FILL"""
        check_sheety_cities = self.get_sheety_data("prices")["prices"]
        rowid = 2
        for i, city in enumerate(check_sheety_cities):
            city_name = check_sheety_cities[i]["city"]
            if len(check_sheety_cities[i]["iataCode"]) == 0:
                get_city = self.get_kiwi_city_iata_code(city_name)
                params = {
                    "price": {
                        "iataCode": get_city,
                    }
                }
                self.update_sheet(params, rowid, "prices")
                rowid += 1
                print(f"{city_name} has been updated with an IATA code.")
            else:
                rowid += 1
                print(
                    f"City code for {city_name} present. Did not need to update."
                )

    def get_saved_price_from_sheet(self) -> dict:
        """Returns a dictionary of current prices by city saved in Google Sheet."""
        get_saved_price = self.get_sheety_data("prices")["prices"]
        city_price_dict = {"saved_price": []}
        for i, v in enumerate(get_saved_price):
            city = get_saved_price[i]["iataCode"]
            saved_price = get_saved_price[i]["lowestPrice"]
            city_price_dict["saved_price"].append(
                {
                    "city": city,
                    "price": saved_price,
                }
            )
        return city_price_dict
