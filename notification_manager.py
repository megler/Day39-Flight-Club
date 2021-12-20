import os
from twilio.rest import Client
from flight_data import FlightData
from flight_search import FlightSearch
import smtplib
from dotenv import load_dotenv
from datetime import datetime as dt

load_dotenv()


class NotificationManager:
    """This class is responsible for sending notifications with the deal flight
    details."""

    def __init__(self) -> None:
        self.flight_search = FlightSearch()
        self.flight_data = FlightData()

    def send_email(
        self,
        price: int,
        departure_city: str,
        from_airport: str,
        destination: str,
        destination_airport: str,
        depart_date: str,
        depart_time: str,
        return_date: str,
        return_time: str,
    ) -> None:

        my_email = os.getenv("MY_EMAIL")
        email_password = os.getenv("MY_PASSWORD")
        smtp = os.getenv("SMTP")
        depart_date = dt.strptime(depart_date, "%m/%d/%y").strftime("%y%m%d")
        return_date = dt.strptime(return_date, "%m/%d/%y").strftime("%y%m%d")
        with smtplib.SMTP(smtp, 587) as connection:
            connection.set_debuglevel(1)
            connection.ehlo()
            connection.starttls()
            connection.login(user=my_email, password=email_password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="email@example.email",  # CHANGE TO EMAIL YOU WANT TO SEND TO
                msg=f"From: YOUR NAME <{my_email}>\nSubject: New Low Price Flight\n\nLow price alert! Only ${price} to fly from {departure_city}-{from_airport} to {destination}-{destination_airport}, departing on {depart_date} at {depart_time} and returning on {return_date} at {return_time}.\nhttps://www.skyscanner.com/transport/flights/{from_airport}/{destination_airport}/{depart_date}/{return_date}/?stops=!oneStop,!twoPlusStops",
            )

    def send_notification(self) -> None:
        low_price_dict = self.flight_search.price_check()
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        client = Client(account_sid, auth_token)

        if len(low_price_dict["new_price"]) > 0:
            for i in range(len(low_price_dict["new_price"])):
                price = low_price_dict["new_price"][i]["price"]
                departure_city = low_price_dict["new_price"][i][
                    "departure_city"
                ]
                departure_airport = low_price_dict["new_price"][i][
                    "departure_iata"
                ]
                arrival_city = low_price_dict["new_price"][i]["arrival_city"]
                arrival_airport = low_price_dict["new_price"][i][
                    "arrival_iata"
                ]
                depart_date = self.flight_data.convert_time(
                    low_price_dict["new_price"][i]["departure_date"]
                )[0]
                depart_time = self.flight_data.convert_time(
                    low_price_dict["new_price"][i]["departure_date"]
                )[1]
                return_date = self.flight_data.convert_time(
                    low_price_dict["new_price"][i]["return_date"]
                )[0]
                return_time = self.flight_data.convert_time(
                    low_price_dict["new_price"][i]["return_date"]
                )[1]
                stopover = low_price_dict["new_price"][i]["stopover"]
                stopover_city = low_price_dict["new_price"][i]["stopover_city"]

                if stopover == 0:
                    msg = f"Low price alert! Only ${price} to fly from {departure_city}-{departure_airport} to {arrival_city}-{arrival_airport} departing on {depart_date} at {depart_time} and returning {return_date} at {return_time}."
                else:
                    msg = (
                        msg
                    ) = f"Low price alert! Only ${price} to fly from {departure_city}-{departure_airport} to {arrival_city}-{arrival_airport} departing on {depart_date} at {depart_time} and returning {return_date} at {return_time}. You will have {stopover} stopover at {stopover_city}"
                message = client.messages.create(
                    body=msg,
                    from_="+18506088282",
                    to="+14076171799",
                )

                self.send_email(
                    price,
                    departure_city,
                    departure_airport,
                    arrival_city,
                    arrival_airport,
                    depart_date,
                    depart_time,
                    return_date,
                    return_time,
                )
