from pprint import pprint
import requests
# For example you structured your google spreadsheet with many sheets. The first sheet should be categories sheet and name exactly "Catergories"
# The other sheets should be named as the topic that the words meaning
SHEETY_CATEGORIES_ENDPOINT = "PLACE YOUR SHEETY URL HERE .../derDieDas/Categories"
SHEETY_DYNAMIC_ENDPOINT = "PLACE YOUR SHEETY URL HERE .../derDieDas"
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
