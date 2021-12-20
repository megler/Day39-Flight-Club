from data_manager import DataManager


class Customer:
    def __init__(self) -> None:
        """Class that handles customer acquisition"""
        self.data_manager = DataManager()

    def add_customer(self) -> None:
        """Receives input of new customer name and email"""
        print("Welcome to Flight Club!")
        print("We find the best flight deals and email you.")
        first_name = input("What is your first name?\n")
        last_name = input("What is your last name?\n")
        email_test = False

        while email_test == False:
            email = input("What is your email address?\n")
            confirm_email = input(
                "Please enter your email address again."
                "(Email addresses must match).\n"
            )
            if email == confirm_email:
                email_test = True
            else:
                print("Email addresses must match. Please try again.")
        self.add_customer_to_sheet(first_name, last_name, email)

    def add_customer_to_sheet(
        self, first_name: str, last_name: str, email: str
    ):
        """Adds new customer to Google Sheet"""
        params = {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
            }
        }
        self.data_manager.new_row(params, "users")
        print("You're in the club!")
