import os
import csv
import pickle


class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                reader = csv.DictReader(file)
                return list(reader)
        else:
            return []

    def add_to_file(self, new_value, mode="a"):
        if new_value:
            if isinstance(new_value, dict):
                fields = new_value.keys()
                new_value = [new_value]
            elif isinstance(new_value, list):
                if new_value:
                    fields = new_value[0].keys()

            with open(self.file_path, mode) as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerows(new_value)
    #

    def find_row(self, unique_param, checking_param):
        all_rows = self.read_file()
        for row in all_rows:
            if row[unique_param] == checking_param:
                return row



    # def edit_row(self, updated_dict):
    #     all_rows = self.read_file()
    #     final_rows = []
    #     for row in all_rows:
    #         information = ast.literal_eval(row["information"])
    #         if information["address"]["postal_code"] == updated_dict["information"]["address"]["postal_code"]:
    #             row = updated_dict
    #         final_rows.append(row)
    #     self.add_to_file(final_rows, mode="w")
    #


    # def read_file(self):
    #     list_objects = []
    #     if os.path.exists(self.file_path):
    #         with open(self.file_path, 'rb') as file:
    #             obj = pickle.load(file)
    #             list_objects.append(obj)
    #     return list_objects
    #
    # def find_obj(self, unique_param, checking_param):
    #     all_objects = self.read_file()
    #     for obj in all_objects:
    #         if obj.__dict__[unique_param] == checking_param:
    #             return obj
    #
    #
    # def add_to_file(self, obj):
    #     # fields = obj.keys()
    #     with open(self.file_path, 'wb') as file:
    #         pickle.dump(obj, file)
