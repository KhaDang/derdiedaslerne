from pprint import pprint
import requests

SHEETY_CATEGORIES_ENDPOINT = "https://api.sheety.co/1754305b3bd13450e62ec977b56a0781/derDieDas/categories"
SHEETY_DYNAMIC_ENDPOINT = "https://api.sheety.co/1754305b3bd13450e62ec977b56a0781/derDieDas/"
class DataManager:

    def __init__(self):
        self.category = {}
    def __del__(self):
        print("Object destrusted!")
    def get_sheets_data(self):
        response = requests.get(url=SHEETY_CATEGORIES_ENDPOINT)
        data = response.json()
        self.category = data["categories"]
        return self.category
    def get_detail_data(self, sheet_name):
        detail_end_point = f"{SHEETY_DYNAMIC_ENDPOINT}{sheet_name}"
        response = requests.get(url=detail_end_point)
        data = response.json()
        return data[sheet_name]
