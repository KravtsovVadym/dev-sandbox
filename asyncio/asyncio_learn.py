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

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            if response.status == 200:
                soup = BeautifulSoup(html, "html.parser")
                price_spans = soup.find_all("span", style="font-size:24px;")
                if len(price_spans) >= 2:
                    min_price = price_spans[0].text
                    max_price = price_spans[1].text
                    print(min_price, max_price, sep="\n")
                else:
                    print("not found")
            else:
                print(f"Error {response.status}")
                return None

if __name__ == ("__main__"):
    asyncio.run(fetch_data("https://hotline.ua/ua/computer-moduli-pamyati-dlya-pk-i-noutbukov/kingston-8-gb-so-dimm-ddr4-2666-mhz-kcp426ss88/"))