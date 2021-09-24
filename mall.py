from file_handler import FileHandler


class Mall:
    file_handler = FileHandler("products.csv")

    def __init__(self, manager, name, opening_time, closing_time):
        self.manager = manager
        self.name = name
        self.opening_time = opening_time
        self.closing_time = closing_time
        # list of dictionaris (product.__dict__ added to this list)
        self.all_products = []
        self.get_products()

    def get_products(self):
        """
        Check file malls.csv if this mall exists, get products from file
        """
        mall = self.file_handler.find_row("manager", self.manager)
        if mall:
            self.all_products = mall["all_products"]



    def update_file(self):
        self.file_handler.add_to_file(self.__dict__)


