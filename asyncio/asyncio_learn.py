"""
Async Web Scraper for Hotline.ua Product Prices

This script asynchronously fetches a webpage from Hotline.ua (Ukrainian e-commerce platform)
and extracts minimum and maximum prices for a specific product.

Key components:
1. aiohttp - for asynchronous HTTP requests (non-blocking I/O)
2. BeautifulSoup - for HTML parsing and data extraction
3. asyncio - for running the async event loop

The script looks for price elements with inline style "font-size:24px;"
which appear to be the price display format on Hotline.ua product pages.

Note: Web scraping may violate website terms of service. Use responsibly with rate limiting.
"""

import aiohttp
import asyncio
from bs4 import BeautifulSoup
async def fetch_data(session, name, data):
    async with session.get(data["url"]) as response:
        html = await response.text()
        if response.status == 200:
            soup = BeautifulSoup(html, "html.parser")
            price_spans = soup.find_all("span",
                                         {"style": data["selector"]}
                                         if name == "hotline"
                                         else {"class": data["selector"]})

            if len(price_spans) >= 2:
                print(f"{name}\nmin: {price_spans[0].text} грн")
                print(f"max: {price_spans[1].text} грн\n{"_"*20}")

            if 0 < len(price_spans) < 2:
                print(f"{name}\nб/у {price_spans[0].text} грн\n{"_"* 20}")

        else:
            print(f"Error {response.status}")


async def main():
    shops = {
        "prom": {
            "url":
                "https://prom.ua/ua/p2687450789-operativna-pamyat-kingston.html",
            "selector":
                "yzKb6"},

        "hotline": {
            "url":
                "https://hotline.ua/ua/computer-moduli-pamyati-dlya-pk-i-noutbukov/kingston-8-gb-so-dimm-ddr4-2666-mhz-kcp426ss88/",
            "selector":
                "font-size:24px;"}
    }
    async with aiohttp.ClientSession() as session:
        async with asyncio.TaskGroup() as tg:
            for name, data in shops.items():
                tg.create_task(fetch_data(session, name, data))
            print(f"kingston 8gb sodimm ddr4 2666\n")


if __name__ == ("__main__"):
    asyncio.run(main())
