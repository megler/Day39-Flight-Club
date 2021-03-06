# Flight Club

Query Kiwi.com for flight info using cities saved in Google Sheet. Sheety
API used to add/update info on Google Sheet. Python Bootcamp Day 39-40


## Usage

For the application to run as written, you will need to set up a Google sheet
with 2 tabs:

1.  Tab 1 is named "prices" (no quotes) with 3 columns:
	- City
    - IATA Code
    - Lowest Price
2.  Tab 2 is named "users" (no quotes) with 3 columns:
    - First Name
    - Last Name
    - Email

The sheet itself can be named whatever you want. You'll be prompted by Sheety for
its name and link.

See comments on main.py. Application allows you to acquire new customers and add
their info to a tab on a Google Sheet.

Also, using the [Kiwi API](kiwi.com) you can get flight info (times, prices, etc)
as well as update the Google Sheet with IATA codes for new cities you may add.

You will need API Credentials for:

[Kiwi](https://partners.kiwi.com/our-solutions/tequila/)

[Sheety](https://sheety.co/)

[Twilio](https://www.twilio.com/docs/sms)

All have free trials to test the code. I would recommend using an email API such
as SendGrid (also Twilio) to send email vs raw Python code. You'll have a better
send rate. However, for testing the SMTP module should work fine.

Email code in the Notification Manager is currently set to send through Gmail.
You'll have to change the SMTP if you have a different email host.

All environmental variables are saved in .env file. See requirements.txt to install
all modules including python-dotenv which will access and run your env variables.

## License
[MIT](https://choosealicense.com/licenses/mit/)