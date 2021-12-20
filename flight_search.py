import json
import requests
from flight_data import FlightData
from data_manager import DataManager


class FlightSearch:
    """This class is responsible for talking to the KIWI Flight Search API."""

    def __init__(self) -> None:
        self.flight_data = FlightData()
        self.sheety_data = DataManager()

    def kiwi_query(self, city: str, stop_overs=0) -> json:
        """Given a destination city as argument, returns json object containing
        price and other relevant data"""
        kiwi_query = {
            "fly_from": "ORL",
            "fly_to": city,
            "date_from": self.flight_data.tomorrow,
            "date_to": self.flight_data.six_months,
            "nights_in_dst_from": 3,
            "nights_in_dst_to": 5,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": stop_overs,
            "vehicle_type": "aircraft",
            "adults": 2,
            "curr": "USD",
        }

        r = requests.get(
            url=self.flight_data.kiwi_flight_search,
            params=kiwi_query,
            headers=self.flight_data.kiwi_header,
        )
        r.raise_for_status()
        flight_data = r.json()
        return flight_data

    def price_check(self) -> dict:
        """Compares saved price against current price and returns dict
        containing relevant data to text customer."""
        sheet_prices = self.sheety_data.get_saved_price_from_sheet()
        rowid = 2
        new_low_price_dict = {"new_price": []}
        stopover_city = ""
        for i, v in enumerate(sheet_prices["saved_price"]):
            city = sheet_prices["saved_price"][i]["city"]
            saved_prices = sheet_prices["saved_price"][i]["price"]
            direct_flight = self.kiwi_query(city)
            layover_flight = self.kiwi_query(city, stop_overs=2)

            if len(direct_flight["data"]) > 0:
                flight_type = direct_flight
            if len(direct_flight["data"]) == 0:
                flight_type = layover_flight
            if (
                len(direct_flight["data"]) == 0
                and len(layover_flight["data"]) == 0
            ):
                rowid += 1
                print("No flights found.")
                continue

            get_current_price = flight_type["data"][0]["price"]
            departure_city = flight_type["data"][0]["cityFrom"]
            departure_iata = flight_type["data"][0]["flyFrom"]
            arrival_city = flight_type["data"][0]["cityTo"]
            arrival_iata = flight_type["data"][0]["cityCodeTo"]
            departure_date = flight_type["data"][0]["route"][0][
                "local_departure"
            ]
            link = flight_type["data"][0]["deep_link"]
            if flight_type == layover_flight:
                stopover = 1
                stopover_city = flight_type["data"][0]["route"][0]["cityTo"]
                return_date = flight_type["data"][0]["route"][2][
                    "local_departure"
                ]
            else:
                stopover = 0
                return_date = flight_type["data"][0]["route"][1][
                    "local_departure"
                ]

            if saved_prices == 0 or get_current_price < saved_prices:
                params = {
                    "price": {
                        "lowestPrice": get_current_price,
                    }
                }
                self.sheety_data.update_sheet(params, rowid, "prices")
                rowid += 1
                new_low_price_dict["new_price"].append(
                    {
                        "departure_city": departure_city,
                        "departure_iata": departure_iata,
                        "arrival_city": arrival_city,
                        "arrival_iata": arrival_iata,
                        "departure_date": departure_date,
                        "return_date": return_date,
                        "price": get_current_price,
                        "stopover": stopover,
                        "stopover_city": stopover_city,
                    }
                )
                print(f"Updated price to {city}")
            else:
                print(f"No new price for {city}.")
                rowid += 1
        return new_low_price_dict
