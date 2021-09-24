class Product:
    def __init__(self, barcode, price, brand, name, available, expiration_date, **kwargs):
        self.barcode = barcode
        self.price = price
        self.brand = brand
        self.name = name
        self.available = available
        self.expiration_date = expiration_date
        self.__dict__.update({k: v for k, v in kwargs.items()})
