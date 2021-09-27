import sys
from sign_up import SignUp
from login import Login
import logging


class Menu:
    logging.basicConfig(filename='app.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    def __init__(self):
        self.choices = {"1": SignUp, "2": Login, "3": self.exit}

    def run(self):
        """Display the menu and respond to choices."""
        while True:
            Menu.display_menu()
            choice = input("Choose a number from 1-3: ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print(f"{choice} is not a valid choice. Try again")

    @staticmethod
    def exit():
        sys.exit(0)

    @staticmethod
    def display_menu():

        print("""****** MAIN MENU *********
1. Sign up
2. Login
3. Exit""")
