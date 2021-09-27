from datetime import datetime

from customer import Customer
from manager import Manager
from mall import Mall
from file_handler import FileHandler


class SignUp:
    file_handler = FileHandler("users.csv")

    def __init__(self):
        while True:
            try:
                print("******* SIGN UP ********")
                print("(Press enter to cancel)")

                role = self.validate_role(input("Role: ").lower())
                username = self.validate_username(input("Username (phonenumber): "))
                password = input("Password: ")
                self.validate_password(input("Repeat password: "), password)

                if role == "manager":
                    mall_name = input("Mall name: ")
                    opening_time = self.validate_time(input("Opening time (%H:%M): "))
                    closing_time = self.validate_time(input("Closing time (%H:%M): "))
                    mall = Mall(username, mall_name, opening_time, closing_time)
                    manager = Manager(username, password, mall)
                    self.file_handler.add_to_file(manager.to_dict())
                    return
                # todo: edit attributes of customer
                customer = Customer(username, password)
                self.file_handler.add_to_file(customer.to_dict())
                return
            except BreakException as e:
                return
            except ValueError as e:
                print(e)

    def validate_role(self, role):
        self.check_canceling(role)
        if role == "manager" or role == "customer":
            return role
        raise ValueError("A Role can be a manager or a customer.")

    def validate_password(self, passwd, re_passwd):
        self.check_canceling(passwd)
        if passwd == re_passwd:
            return re_passwd
        raise ValueError("The password doesn't match.")

    def validate_username(self, phone_number):
        self.check_canceling(phone_number)
        if len(phone_number) == 11 and phone_number.startswith("09") and phone_number.isalnum():
            if self.file_handler.find_row("username", phone_number):
                raise ValueError("This user already exists.")
            return phone_number
        raise ValueError("Invalid phone number.")

    def validate_time(self, input_time):
        self.check_canceling(input_time)
        # check if the input time is in required format otherwise raise an error.
        try:
            datetime.strptime(input_time, '%H:%M')
        except Exception:
            raise ValueError(f"{input_time} does not match format %H:%M")
        else:
            return input_time

    def check_canceling(self, value):
        if value == "":
            print("Canceling...")
            raise BreakException()


class BreakException(Exception):
    pass
