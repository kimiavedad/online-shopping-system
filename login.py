from Kimia_Vedad_HW9_Maktab61.customer import Customer
from file_handler import FileHandler
import hashlib
from manager import Manager
from mall import Mall


class Login:
    file_handler_users = FileHandler("users.csv")
    file_handler_malls = FileHandler("products.csv")
    file_handler_receipts = FileHandler("receipt.csv")

    def __init__(self):
        while True:
            try:
                print("******** LOG IN *********")
                print("(Press enter to cancel)")
                username = self.validate_username(input("Username: "))
                password = self.validate_password(username, input("Password: "))
                user = self.find_user(username)
                if user["role"] == "manager":
                    mall = self.get_mall(user["username"])
                    Manager(user["username"], password, mall)
                else:
                    all_receipts = self.get_receipts(user["username"])
                    Customer(user["username"], password, all_receipts)
                return
            except BreakException as e:
                return
            except ValueError as e:
                print(e)

    def validate_username(self, username):
        self.check_canceling(username)
        user = self.find_user(username)
        if user:
            return username
        raise ValueError(f"Username {username} not found.")

    def validate_password(self, username, passwd):
        self.check_canceling(passwd)
        user = self.find_user(username)
        hash_passwd = hashlib.sha256(passwd.encode()).hexdigest()
        if hash_passwd == user["password"]:
            return passwd
        raise ValueError("Wrong password.")

    def find_user(self, username):
        return self.file_handler_users.find_row("username", username)

    def get_mall(self, manager_username):
        """ create a mall object from file"""
        mall = self.file_handler_malls.find_row("manager", manager_username)
        mall["all_products"] = eval(mall["all_products"])
        mall["blocked_customers"] = eval(mall["blocked_customers"])
        return Mall(mall["manager"], mall["name"], mall["opening_time"], mall["closing_time"], mall["all_products"],
                    mall["blocked_customers"])

    def get_receipts(self, customer_username):
        """ read all receipt of a customer from file and convert it to list of dictionary using eval() """
        all_receipts = self.file_handler_receipts.find_row("customer", customer_username)["all_receipts"]
        if all_receipts:
            all_receipts = eval(all_receipts)
        else:
            all_receipts = []
        return all_receipts

    @staticmethod
    def check_canceling(value):
        """ check input value if it's empty raise an BreakException"""
        if value == "":
            raise BreakException("Canceling...")


class BreakException(Exception):
    pass
