from dotenv import load_dotenv
import os
from datetime import datetime as dt, timedelta
from dateutil.relativedelta import *

load_dotenv()


class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self) -> None:
        self.KIWI_API = os.getenv("KIWI_API")
        self.kiwi_endpoint = "http://tequila-api.kiwi.com"
        self.kiwi_flight_search = f"{self.kiwi_endpoint}/v2/search/"
        self.kiwi_locations = f"{self.kiwi_endpoint}/locations/query"
        self.kiwi_header = {
            "apikey": self.KIWI_API,
        }
        self.today = dt.now()
        self.tomorrow = (self.today + timedelta(days=1)).strftime("%d/%m/%Y")
        self.six_months = (self.today + relativedelta(months=+6)).strftime(
            "%d/%m/%Y"
        )

    def convert_time(self, timestamp: str) -> tuple:
        """Given a timestamp in this format: 2022-01-29T17:40:00.000Z format into usable string"""
        split_timestamp = timestamp.split(sep="T", maxsplit=-1)
        fly_date = split_timestamp[0]
        fly_time = split_timestamp[1]
        formatted_date = dt.strptime(fly_date, "%Y-%m-%d").strftime("%m/%d/%y")
        formatted_time = dt.strptime(fly_time, "%H:%M:%S.%f%z").strftime(
            "%I:%M%p"
        )
        return (formatted_date, formatted_time)
