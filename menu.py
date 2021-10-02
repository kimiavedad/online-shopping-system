import sys
import logging
from manager import Manager
from customer import Customer


class Menu:
    logging.basicConfig(filename='app.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    def __init__(self):
        self.choices = {"1": Manager.sign_up, "2": Customer.sign_up, "3": Manager.log_in, "4": Customer.log_in}

    def run(self):
        """Display the menu and respond to choices."""
        while True:
            Menu.display_menu()
            choice = input("Choose a number from 1-3: ")
            action = self.choices.get(choice)
            if choice == "5":
                sys.exit(0)
            elif action:
                try:
                    user = action()
                    if isinstance(user, Manager):
                        user.print_warnings()
                    print(type(user))
                    user.interface()
                except ValueError as e:
                    logging.error(e)
                    print(e)
            else:
                print(f"{choice} is not a valid choice. Try again")

    @staticmethod
    def display_menu():
        print("""****** MAIN MENU *********
    1. Sign up as Manager
    2. Sign up as Customer
    3. Login as Manager
    4. Login as Customer
    5. Exit""")
