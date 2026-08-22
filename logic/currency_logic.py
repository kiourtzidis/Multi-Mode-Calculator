import requests
from datetime import datetime

class CurrencyLogic:

    def __init__(self):
        self.rates = {}
        self.base_currency = 'USD'
        self.last_updated = None
        self.refresh_rates()


    def refresh_rates(self):
        try:
            response = requests.get(f'https://api.frankfurter.app/latest?from={self.base_currency}')
            data = response.json()
            self.rates = data['rates']
            self.rates[self.base_currency] = 1.0
            self.last_updated = datetime.now().strftime('%H:%M:%S · %b %d %Y')
        except requests.RequestException:
            pass


    def get_currencies(self):
        return sorted(self.rates.keys())


    def convert(self, amount, from_code, to_code):

        if from_code not in self.rates or to_code not in self.rates:
            return None

        usd_amount = amount / self.rates[from_code]
        return usd_amount * self.rates[to_code]


    def get_last_updated(self):
        return self.last_updated or 'Update failed'