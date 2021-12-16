import logging

from file_handler import FileHandler
from datetime import datetime, time


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
        return [product for product in self.all_products if int(product['available']) <= 3]

    def get_available_products(self):
        return [product for product in self.all_products if int(product['available']) > 0]

    def get_product(self, barcode):
        return next((product for product in self.all_products if product["barcode"] == barcode), None)

    def remove_product(self, name):
        product = self.get_product(name)
        if product:
            self.all_products = [product for product in self.all_products if product['name'] != name]
            print(f"Product {name} removed successfully.")
        else:
            raise ValueError(f"There isn't any product {name}.")

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

    def display_products_to_manager(self, list_products):
        # todo: use pretty table for showing products
        print("\n{:<10}{:<11}{:<8}{:<13}{}".format("Barcode", "Name", "Brand", "Available", "Price"))
        print("______________________________________________")
        for product in list_products:
            print("{:<10}{:<11}{:<8}{:<13}{}".format(product["barcode"], product["name"], product["brand"],
                                                     product["available"], product["price"]))
        print()

    def display_products_to_customer(self, customer_username):
        # todo: use pretty table for showing products
        list_products = self.get_available_products()
        if customer_username not in self.blocked_customers:
            if list_products:
                print("*********List of available products*********")
                print("\n{:<13}{:<13}{}".format("Name", "Brand", "Price"))
                print("______________________________________________")
                for product in list_products:
                    print("{:<13}{:<13}{}".format(product["name"], product["brand"], product["price"]))
                print("********************************************")
            else:
                raise ValueError("There is no available product in this mall.")
        else:
            raise ValueError("Oops! You can't buy from this shop.")

    def is_open(self, visiting_time):
        opening_time_obj = datetime.strptime(self.opening_time, '%H:%M').time()
        closing_time_obj = datetime.strptime(self.closing_time, '%H:%M').time()
        if opening_time_obj < visiting_time < closing_time_obj:
            return True
        return False

    def buy(self, list_product):
        """change available amount for purchased product"""
        for p_mall in self.all_products:
            for p in list_product:
                if p_mall["name"] == p["name"]:
                    available = int(p_mall["available"])
                    available -= int(p["quantity"])
                    p_mall["available"] = available
                    if p_mall["available"] == 0:
                        logging.warning(f"{p_mall['name']} is no longer available in the mall.")
                        self.remove_product(p_mall["name"])

    def __str__(self):
        return f"{self.name.title()} Shopping Mall - Opening hours: {self.opening_time} am - {self.closing_time} pm"
