import hashlib
from datetime import datetime
import logging
from file_handler import FileHandler
from product import Product
from receipt import Receipt


class Manager:
    file_handler_users = FileHandler("users.csv")
    file_handler_products = FileHandler("malls.csv")
    file_handler_receipts = FileHandler("receipt.csv")
    role = "manager"

    def __init__(self, username, password, mall):
        """create a new object when manager signs in or logs in"""
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.mall = mall
        self.print_warnings()
        self.manager_interface()

    def to_dict(self):
        return {"role": self.role, "username": self.username, "password": self.password}

    @staticmethod
    def display_manager_menu():
        """
        Display a menu for manager role
        """
        print("******* MANAGER MENU ******")
        print("1.Add product")
        print("2.Remove product")
        print("3.List of available products")
        print("4.List of all receipts.")
        print("5.Search receipts.")
        print("6.Block a customer.")
        print("7.Logout")

    def manager_interface(self):
        choices = {"1": self.add_products, "2": self.remove_product, "3": self.available_products,
                   "4": self.print_all_receipts, "5": self.filter_receipts, "6": self.block_customer}
        while True:
            try:
                self.display_manager_menu()
                choice = input("Please enter your choice : ")
                if choice == "7":
                    # if mall exists in file the mall must removed and then add a new mall
                    self.mall.update_file()
                    break
                action = choices.get(choice)
                if action:
                    action()
                else:
                    raise ValueError(f"{choice} is not a valid choice. Try again")
            except ValueError as e:
                logging.error(e)
                print(e)

    def add_products(self):
        n = input("Enter the number of products need to be added: ")
        if n is None or not n.isnumeric():
            raise ValueError("number of products must be an integer.")
        for i in range(int(n)):
            print("**** NEW PRODUCT ****")
            barcode = self.validate_barcode(input("Barcode: "))
            name = input("Name: ")
            brand = input("Brand: ")
            available = self.validate_available(input("Available : "))
            price = self.validate_price(input("Price : "))
            exp_date = self.validate_date(input("Expiration date: "))
            # todo: edit this function the way that can get kwargs
            product = Product(barcode, price, brand, name, available, exp_date)
            self.mall.add_product(product)
            logging.info("New product added.")
        print("Products added successfully.")

    def remove_product(self):
        barcode = int(input("Enter the barcode of product need to be remove: "))
        self.mall.remove_product(barcode)

    def available_products(self):
        self.print_warnings()
        available_products = self.mall.get_available_products()
        if available_products:
            print("***** List of available products *****")
            self.mall.display_products(self.username, available_products)
        else:
            print("No product is added yet.")

    def print_warnings(self):
        finished_products = self.mall.get_finished_products()
        if finished_products:
            logging.warning("ran of put of some products.")
            print("******* ATTENTION ********")
            print("We ran out of these products:")
            self.mall.display_products(self.username, finished_products)

    @staticmethod
    def display_receipts(list_receipts):
        """ print all the receipts in list_receipts """
        for receipt in list_receipts:
            receipt_obj = Receipt(receipt["mall"], receipt["customer"], receipt["date"], receipt["hour"],
                                  receipt["purchased_products"])
            receipt_obj.display()

    def list_all_receipts(self):
        """ return a list of receipts related to this mall """
        related_receipts = []
        for customer in self.file_handler_receipts.read_file():
            customer["all_receipts"] = eval(customer["all_receipts"])
            for receipt in customer["all_receipts"]:
                if receipt["mall"] == self.mall.name:
                    related_receipts.append(receipt)
        return related_receipts

    def print_all_receipts(self):
        self.display_receipts(self.list_all_receipts())

    def filter_receipts(self):
        filter_parameter = input("Search by date, customer or both (date customer): ").lower()
        all_receipts = self.list_all_receipts()
        filtered = [r for r in all_receipts if filter_parameter in f"{r['date']} {r['customer']}"]
        if filtered:
            self.display_receipts(filtered)
        else:
            raise ValueError("Your search did not match any receipts.")

    def block_customer(self):
        username = input("Enter the customer's username: ")
        if username in self.mall.blocked_customers:
            raise ValueError(f"This username ({username} already exists in block list.)")
        self.get_customer(username)  # if this customer not exists, get_customer() raise error
        self.mall.blocked_customers.append(username)
        print(f"Customer ({username}) is blocked now.")
        print(f"List of blocked customers: {self.mall.blocked_customers}")

    def get_customer(self, username):
        user_dict = self.file_handler_users.find_row("username", username)
        if user_dict and user_dict["role"] == "customer":
            return user_dict
        else:
            raise ValueError(f"There is no customer associated with this username ({username})")

    def validate_barcode(self, barcode):
        if not barcode.isnumeric():
            raise ValueError("A barcode must be an integer.")
        if self.mall.get_product(barcode):
            raise ValueError("Barcode must be unique.")
        return barcode

    @staticmethod
    def validate_available(number):
        if number.isnumeric():
            return int(number)
        raise ValueError("Available quantity of product must be an integer.")

    @staticmethod
    def validate_price(price):
        try:
            return float(price)
        except ValueError:
            raise ValueError("Invalid price format.")

    @staticmethod
    def validate_date(date_string):
        try:
            datetime.strptime(date_string, '%Y/%m/%d')
            return date_string
        except Exception:
            raise ValueError(f"{date_string} does not match format %Y/%m/%d")
