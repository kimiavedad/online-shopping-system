from file_handler import FileHandler
import hashlib
import logging


class User:
    file_handler_users = FileHandler("users.csv")
    file_handler_malls = FileHandler("malls.csv")
    file_handler_receipts = FileHandler("receipt.csv")
    role = None

    def __init__(self, username, password):
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()

    @classmethod
    def sign_up(cls):
        print("******* SIGN UP ********")
        username = cls.validate_signup_username(input("Username (phone-number): "))
        password = input("Password: ")
        cls.validate_signup_password(input("Repeat password: "), password)
        return cls(username, password)

    @classmethod
    def log_in(cls):
        print("******** LOG IN *********")
        username = cls.validate_login_username(input("Username: "))
        password = cls.validate_login_password(username, input("Password: "))
        logging.info(f"User {username} logged in.")
        return cls(username, password)

    def to_dict(self):
        return {"role": self.role, "username": self.username, "password": self.password}

    def interface(self):
        pass

    @classmethod
    def validate_login_username(cls, username):
        User.check_empty("Username", username)
        user = User.find_user(username)
        if user and user["role"] == cls.role:
            return username
        raise ValueError(f"{cls.role.title()} {username} not found.")

    @staticmethod
    def validate_login_password(username, passwd):
        User.check_empty("Password", passwd)
        user = User.find_user(username)
        hash_passwd = hashlib.sha256(passwd.encode()).hexdigest()
        if hash_passwd == user["password"]:
            return passwd
        raise ValueError("Wrong password.")

    @staticmethod
    def find_user(username):
        return User.file_handler_users.find_row("username", username)

    @staticmethod
    def validate_signup_password(passwd, re_passwd):
        User.check_empty("Password", passwd)
        if passwd == re_passwd:
            return re_passwd
        raise ValueError("The password doesn't match.")

    @staticmethod
    def validate_signup_username(phone_number):
        User.check_empty("Username", phone_number)
        # TODO: USE REGEX
        if len(phone_number) == 11 and phone_number.startswith("09") and phone_number.isalnum():
            if User.file_handler_users.find_row("username", phone_number):
                raise ValueError("This user already exists.")
            return phone_number
        raise ValueError("Invalid phone number.")

    @staticmethod
    def check_empty(field, value):
        """ check input value if it's empty raise error"""
        if value == "":
            raise ValueError(f"{field.title()} field is mandatory and can not be empty.")
        return value
