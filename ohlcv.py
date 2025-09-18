import requests
import os

ALVAN_ENDPOINT = "https://www.alphavantage.co/query"

class OHLSV:
    def __init__(self):
        self.key = os.environ['ALVAN_KEY']
        self.endpoint = ALVAN_ENDPOINT
        self.data = {}

    def get_data(self, symbol):
        alvan_parameter = {
            "function": "DIGITAL_CURRENCY_DAILY",
            "symbol": symbol,
            "market": "USD",
            "apikey": self.key,
        }
        response = requests.get(self.endpoint, params=alvan_parameter)
        response.raise_for_status()
        self.data = response.json()["Time Series (Digital Currency Daily)"]

        return self.data