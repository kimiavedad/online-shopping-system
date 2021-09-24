import sys
from sign_in import SignIn
from login import Login


class Menu:
    def __init__(self):
        self.choices = {"1": SignIn, "2": Login, "3": self.exit}

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

    def exit(self):
        sys.exit(0)

    @staticmethod
    def display_menu():

        print("""****** MAIN MENU *********
1. Sign in
2. Login
3. Exit""")


menu = Menu()
menu.run()
