from prettytable import PrettyTable


class ShoppingBag:
    def __init__(self, mall_name, selected_products):
        self.mall = mall_name
        self.purchased_products = selected_products
        self.sum_prices = self.calculate_sum()

    def calculate_sum(self):
        prices = [int(p["price"]) * int(p["quantity"]) for p in self.purchased_products]
        return sum(prices)

    def display(self):
        print("******************** Shopping bag ************************")
        print(f"          {self.mall.title()}          ")
        print("{:<11}{:<9}{:<9}{}".format("Product", "Qty", "Price", "Total price"))
        print("________________________________________")
        for product in self.purchased_products:
            total_price = int(product["price"]) * int(product["quantity"])
            print("{:<11}{:<9}{:<9}{}".format(product["name"], product["quantity"], product["price"], total_price))
        print(f"Sum: {self.sum_prices}")
        print("**********************************************************")


# inja b file add nakon chon k hey mikham azash object besazam
# vaqti karbar log out mikne residhash save beshan tu file


class Receipt(ShoppingBag):
    # x = PrettyTable()

    def __init__(self, mall_name, customer_number, date, hour, purchased_products):
        super().__init__(mall_name, purchased_products)
        self.customer = customer_number
<<<<<<< HEAD
        self.purchased_products = purchased_products
=======
>>>>>>> phase2
        self.date = date
        self.hour = hour

    def display(self):
        print("**********************************************************")
        print(f"          {self.mall.title()}          ")
        print(f"Customer: {self.customer}")
        print(f"Date: {self.date} {self.hour}")
        print("{:<11}{:<9}{:<9}{}".format("Product", "Qty", "Price", "Total price"))
        print("________________________________________")
        for product in self.purchased_products:
            total_price = int(product["price"]) * int(product["quantity"])
            print("{:<11}{:<9}{:<9}{}".format(product["name"], product["quantity"], product["price"], total_price))
        print(f"Sum: {self.sum_prices}")
        print("**********************************************************")



