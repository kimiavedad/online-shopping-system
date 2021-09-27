from prettytable import PrettyTable


class ShoppingBag:
    pass

# inja b file add nakon chon k hey mikham azash object besazam
# vaqti karbar log out mikne residhash save beshan tu file

class Receipt:
    x = PrettyTable()

    def __init__(self, mall_name, customer_number, date, hour, purchased_products):
        self.mall = mall_name
        self.customer = customer_number
        # purchased_products is a list of tuples first position is product and second position is quantity
        self.purchased_products = purchased_products
        self.date = date
        self.hour = hour
        self.sum_prices = self.calculate_sum()

    def calculate_sum(self):
        prices = [int(p["price"]) * int(p["quantity"]) for p in self.purchased_products]
        return sum(prices)

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



