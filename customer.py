import hashlib
from datetime import datetime, time, date

from Kimia_Vedad_HW9_Maktab61.receipt import Receipt
from file_handler import FileHandler
from mall import Mall


class Customer:
    file_handler_users = FileHandler("users.csv")
    file_handler_products = FileHandler("malls.csv")
    file_handler_receipts = FileHandler("receipt.csv")
    role = "customer"

    def __init__(self, username, password, all_receipts=[]):
        """create a new object when customer signs in or logs in"""
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.all_receipts = all_receipts
        self.selected_products = []
        self.customer_interface()

    def to_dict_receipts(self):
        dict_to_write = {"customer": self.username, "all_receipts": self.all_receipts}
        return dict_to_write

    def to_dict(self):
        return {"role": self.role, "username": self.username, "password": self.password}

    @staticmethod
    def display_customer_menu():
        print("******* CUSTOMER MENU ******")
        print("1.List of all previous receipts")
        print("2.List of all shopping malls")
        print("3.Search for a mall")
        print("4.Select a mall")
        print("5.Logout")

    def customer_interface(self):
        choices = {"1": self.print_all_receipts, "2": self.print_all_malls, "3": self.search_mall, "4":self.select_mall}
        while True:
            try:
                self.display_customer_menu()
                choice = input("Please enter your choice : ")
                if choice == "5":
                    self.file_handler_receipts.add_to_file(self.to_dict_receipts())
                    return
                action = choices.get(choice)
                if action:
                    action()
                else:
                    raise ValueError(f"{choice} is not a valid choice. Try again")
            except ValueError as e:
                print(e)

    def print_all_receipts(self):
        for receipt in self.all_receipts:
            receipt_obj = Receipt(receipt["mall"], receipt["customer"], receipt["date"], receipt["hour"],
                                  receipt["purchased_products"])
            receipt_obj.display()

    def print_all_malls(self):
        malls = self.file_handler_products.read_file()
        print()

    def search_mall(self):
        mall_name = input("Mall Name: ")
        mall = self.get_mall(mall_name)
        if mall:
           print(mall)
        else:
            print(f"There is currently no mall associated with this name ({mall_name}) in our system.")


    def select_mall(self):
        mall = self.get_mall(input("Mall Name: "))
        if self.username not in mall.blocked_customers:
            mall.display_products(self.username)
            self.selected_products = []
            # item = input("Select a products you want tp buy or enter to cancle.")
        else:
            print("You can't buy from this shop.")

    def add_to_shopping_bag(self):
        # select from product of mall.
        # create a product object
        # ask the quantity
        # product_dict = {"name": product.__dict__["name"], "price":  product.__dict__["price"], "quantity":quantity}
        # add this tuple to list selected_products
        pass

    def remover_from_shopping_bag(self):
        pass

    def search_products(self):
        pass

    def view_shopping_bag(self):
        pass

    def buy(self):
        # create a receipt and add it to all receipts.

        date = datetime.now().strftime("%d/%m/%Y")
        hour = datetime.now().time().strftime('%H:%M')
        # receipt = Receipt(mallpurchased_products=self.selected_products)
        # self.all_receipts.append(receipt.__dict__)
        pass



    def get_mall(self, mall_name):
        mall = self.file_handler_products.find_row("name", mall_name)
        if mall:
            return Mall(mall["manager"], mall["name"], mall["opening_time"], mall["closing_time"], mall["all_products"],
                    mall["blocked_customers"])





