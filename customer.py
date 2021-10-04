import hashlib
from datetime import datetime, time, date
from user import User
from receipt import Receipt, ShoppingBag
from file_handler import FileHandler
from mall import Mall
import logging


class Customer(User):
    role = "customer"

    def __init__(self, username, password):
        """create a new object when customer signs in or logs in"""
        super().__init__(username, password)
        self.all_receipts = []
        self.list_shopping_bag = []

    @classmethod
    def sign_up(cls):
        customer = super().sign_up()
        logging.info("New customer registered.")
        customer.file_handler_users.add_to_file(customer.to_dict())
        return customer

    @classmethod
    def log_in(cls):
        customer = super().log_in()
        customer.all_receipts = cls.get_receipts_from_file(customer.username)
        return customer

    @staticmethod
    def get_receipts_from_file(customer_username):
        """ read all receipt of a customer from file and convert it to list of dictionary using eval() """
        row = Customer.file_handler_receipts.find_row("customer", customer_username)
        if row:
            all_receipts = eval(row["all_receipts"])
        else:
            all_receipts = []
        return all_receipts

    @staticmethod
    def customer_menu():
        print("******* CUSTOMER MENU ******")
        print("1.List of all previous receipts")
        print("2.Start shopping")
        # print("3.Search for a mall")
        # print("4.Choose a mall")
        # print("5.Search for a product")
        # print("6.Add ")
        # print("7.Shopping bag")
        print("3.Logout")

    def interface(self):
        choices = {"1": self.print_all_receipts, "2": self.start_shopping}
        while True:
            try:
                self.customer_menu()
                choice = input("Please enter your choice : ")
                if choice == "3":
                    return
                action = choices.get(choice)
                if action:
                    action()
                else:
                    raise ValueError(f"{choice} is not a valid choice. Try again")
            except ValueError as e:
                logging.error()
                print(e)

    def print_all_receipts(self):
        if self.all_receipts:
            for receipt in self.all_receipts:
                receipt_obj = Receipt(receipt["mall"], receipt["customer"], receipt["date"], receipt["hour"],
                                      receipt["purchased_products"])
                receipt_obj.display()
        else:
            print("List receipts is empty.")

    def start_shopping(self):
        """search for a mall or show list of malls and start shopping if selected_mall exists."""
        choice = input("1.list of all shopping mall\n2.search for a mall.\nChoose [1/2]: ")
        selected_mall = None
        while True:
            if choice == "1":
                list_malls = self.list_open_malls()
                if list_malls:
                    self.print_malls(list_malls)
                    selected_mall = self.choose_mall(list_malls)
                else:
                    print("There is no open shopping mall.")  # if there is no mall in the malls.csv or shops are closed
                break
            elif choice == "2":
                selected_mall = self.search_mall()
                break
            else:
                raise ValueError(f"{choice} is not a valid choice.")
        if selected_mall:
            self.list_shopping_bag = []
            selected_mall.display_products_to_customer(self.username)
            self.select_products(selected_mall)
            while self.list_shopping_bag:
                self.view_shopping_bag(selected_mall)
                choice = input("1.checkout \n2.edit shopping bag\n")
                if choice == "1":
                    break
                if choice == "2":
                    self.edit_shopping_bag(selected_mall)

            if self.list_shopping_bag:
                self.checkout(selected_mall)

    def list_open_malls(self):
        list_malls = []
        empty_list = True
        now = datetime.now().time()
        malls = self.file_handler_malls.read_file()
        if malls:
            for mall in malls:
                mall_obj = Mall.get_mall(mall["manager"])
                if mall_obj.is_open(now):
                    empty_list = False
                    list_malls.append(mall_obj)
        return list_malls

    def print_malls(self, list_malls):
        for mall_obj in list_malls:
            print(mall_obj)

    def choose_mall(self, malls):
        """return mall_obj if exists in the list"""
        mall_name = input("Choose a mall from list above: ").lower()  # اسم فروشگاه رو اینجا میدیم بهش
        mall = next((m for m in malls if m.name == mall_name), None)
        if mall:
            return mall
        else:
            print(f"There is currently no mall associated with this name ({mall_name}) in our system.")

    def search_mall(self):
        mall_name = input("Mall Name: ")
        mall = self.file_handler_malls.find_row("name", mall_name)
        if mall:
            now = datetime.now().time()
            mall_obj = Mall.get_mall(mall["manager"])
            if mall_obj.is_open(now):
                return mall_obj
            else:
                print(mall_obj)
                print("This shop is closed now. Come again later.")
        else:
            print(f"There is currently no mall associated with this name ({mall_name}) in our system.")

    def select_products(self, mall):
        continue_shopping = "y"
        while continue_shopping != "n":
            product = self.find_product_in_list(mall.get_available_products(), "Enter name of product: ")
            if product:
                quantity = int(input("Quantity: "))
                if quantity > int(product["available"]):
                    print(f"We've got only {product['available']} {product['name']} available.")
                else:
                    self.add_to_shopping_bag(product, quantity)
            else:
                print("This product isn't in the mall.")
            continue_shopping = input("Do you want to continue? [y/n]: ")

    def add_to_shopping_bag(self, product_dict, quantity):
        product_dict = {"name": product_dict["name"], "price": product_dict["price"],
                        "quantity": int(quantity)}
        self.list_shopping_bag.append(product_dict)
        print(f"{quantity} {product_dict['name']} added to your shopping bag.")

    def view_shopping_bag(self, mall_obj):
        shopping_bag = ShoppingBag(mall_obj.name, self.list_shopping_bag)
        shopping_bag.display()

    def edit_shopping_bag(self, mall_obj):
        while len(self.list_shopping_bag) > 0:
            product = self.find_product_in_list(self.list_shopping_bag, "Which item do you want to remove? ")
            if product:
                self.remove_from_shopping_bag(product["name"])
                choice = input("OK. Do you want to remove more? [y/n]: ")
                if choice == "n":
                    break
            else:
                print("this product isn't in your shopping bag")
        else:
            print("Your shopping bag is empty.")

    def checkout(self, mall_obj):
        # create a receipt and add it to all receipts.
        today = datetime.now().strftime("%d/%m/%Y")
        hour = datetime.now().time().strftime('%H:%M')
        new_receipt = Receipt(mall_obj.name, self.username, today, hour, self.list_shopping_bag)
        self.all_receipts.append(new_receipt.__dict__)
        mall_obj.buy(self.list_shopping_bag)
        self.update_file()
        mall_obj.update_file()
        self.list_shopping_bag = []
        print("Thank you for your purchase!")
        new_receipt.display()

    def search_products(self):
        pass

    def remove_from_shopping_bag(self, product_name):
        self.list_shopping_bag = [p for p in self.list_shopping_bag if p["name"] != product_name]

    def find_product_in_list(self, products, message):
        product_name = input(message)
        product = next((product for product in products if product["name"] == product_name),
                       None)
        return product

    def to_dict_receipts(self):
        dict_to_write = {"customer": self.username, "all_receipts": self.all_receipts}
        return dict_to_write

    def update_file(self):
        customer_in_file = self.file_handler_receipts.find_row("customer", self.username)
        if customer_in_file:
            self.file_handler_receipts.edit_row("customer", self.username, self.to_dict_receipts())
        else:
            self.file_handler_receipts.add_to_file(self.to_dict_receipts())
