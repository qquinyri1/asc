import aiohttp
import asyncio
from datetime import datetime, timedelta

class CurrencyAPIClient:
    BASE_URL = "https://api.privatbank.ua/p24api"
    
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def fetch_currency_rates(self, date):
        url = f"{self.BASE_URL}/exchange_rates?json&date={date:%d.%m.%Y}"
        async with self.session.get(url) as response:
            data = await response.json()
            return data

    async def fetch_last_week_rates(self):
        today = datetime.now()
        rates = []
        for _ in range(10):
            date = today - timedelta(days=1)
            rates.append(await self.fetch_currency_rates(date))
            today = date
        return rates

    async def close(self):
        await self.session.close()

class CurrencyRatePrinter:
    @staticmethod
    def print_rates(rates):
        for rate in rates:
            date = rate.get("date")
            if date:
                currencies = rate.get("exchangeRate")
                if currencies:
                    eur = next((c for c in currencies if c["currency"] == "EUR"), None)
                    usd = next((c for c in currencies if c["currency"] == "USD"), None)
                    if eur and usd:
                        eur_rate = eur["saleRate"]
                        usd_rate = usd["saleRate"]
                        print(f"Date: {date} - EUR: {eur_rate} USD: {usd_rate}")

async def main():
    try:
        api_client = CurrencyAPIClient()
        rates = await api_client.fetch_last_week_rates()
        CurrencyRatePrinter.print_rates(rates)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await api_client.close()

if __name__ == "__main__":
    asyncio.run(main())

