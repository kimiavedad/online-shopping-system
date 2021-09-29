from file_handler import FileHandler
from datetime import datetime


class Mall:
    file_handler = FileHandler("malls.csv")

    def __init__(self, manager, name, opening_time, closing_time, all_products=[], blocked_customers=[]):
        self.manager = manager
        self.name = name
        self.opening_time = opening_time
        self.closing_time = closing_time
        # list of dictionaris (product.__dict__ added to this list)
        self.all_products = all_products
        self.blocked_customers = blocked_customers
        self.update_file()

    @classmethod
    def get_mall(cls, manager_username):
        """ create a mall object from file"""
        mall = cls.file_handler.find_row("manager", manager_username)
        mall["all_products"] = eval(mall["all_products"])
        mall["blocked_customers"] = eval(mall["blocked_customers"])
        return Mall(mall["manager"], mall["name"], mall["opening_time"], mall["closing_time"], mall["all_products"],
                    mall["blocked_customers"])

    def get_finished_products(self):
        return [product for product in self.all_products if product['available'] <= 3]

    def get_available_products(self):
        return [product for product in self.all_products if product['available'] != 0]

    def get_product(self, barcode):
        return next((product for product in self.all_products if product["barcode"] == barcode), None)

    def remove_product(self, barcode):
        product = self.get_product(barcode)
        if product:
            self.all_products = [product for product in self.all_products if product['barcode'] != barcode]
            print(f"Product with barcode {barcode} removed successfully.")
        else:
            raise ValueError(f"There isn't any product with barcode {barcode}.")

    def add_product(self, product):
        self.all_products.append(product.__dict__)

    def update_file(self):
        # todo: edit file if: mall_in_file exists and mall_in_file != mall
        # if not exists add to file
        mall_in_file = self.file_handler.find_row("manager", self.manager)
        # pairs = zip(self.__dict__, mall_in_file)
        # any(x != y for x, y in pairs)
        if mall_in_file:
            self.file_handler.edit_row("manager", self.manager, self.__dict__)
        elif mall_in_file is None:
            self.file_handler.add_to_file(self.__dict__)


    def display_products(self, username, list_products=[]):
        # todo: use pretty table for showing products
        if not list_products:
            list_products = self.all_products
        if username not in self.blocked_customers:
            print("\n{:<10}{:<8}{:<8}{:<13}{}".format("Barcode", "Name", "Brand", "Available", "Price"))
            print("______________________________________________")
            for product in list_products:
                print("{:<10}{:<8}{:<8}{:<13}{}".format(product["barcode"], product["name"], product["brand"],
                                                        product["available"], product["price"]))
            print()
        else:
            print()

    def enter_to_mall(self, visiting_time):
        if self.is_open(visiting_time):
            print(f"Welcome to the {self.name} shopping mall.")
            self.display_products(self.all_products)
        else:
            print("Sorry... We're closed. Come again later.")

    def is_open(self, visiting_time):
        opening_time_obj = datetime.strptime(self.opening_time, '%H:%M')
        closing_time_obj = datetime.strptime(self.closing_time, '%H:%M')
        if opening_time_obj < visiting_time < closing_time_obj:
            return True
        return False

    def __str__(self):
        return f"{self.name.title()} Shopping Mall - Opening hours: {self.opening_time} am - {self.closing_time} pm"
