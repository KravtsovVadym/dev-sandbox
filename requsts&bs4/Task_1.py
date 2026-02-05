"""
This module parses the ad on the page.
Next example (model fields that need to be parsed).

This module uses two search approaches
Beautifulsoup library
the first is through (find /find_all)
The find method is technically faster than select() or select_one()
since third-party libraries are not called.

In this task, I used an approach with checking for an empty string
although it is possible to apply an easier solution to this problem
check the already parsed dictionary for empty lines before saving to the database.

Checks with conditional operators were not performed for the purpose of debugging.

Fields database
===================
title
collor
memory_size
memory_unit
manufacturer
price
price_discount
img_ulr
product_code
review_count
screen_diagonal
display_resolution
characteristics
====================
"""

# from load_django import *
from bs4 import BeautifulSoup
import requests

FIELDS = {
    'title': 'h1[class="desktop-only-title"]',
    'color': 'a[title*="Колір" i]',
    'memory_size': 'a[title*="пам" i]',
    'memory_unit': 'a[title*="пам" i]',
    # 'manufacturer': ,
    # 'price':
    # 'price_discount':
    # 'img_ulr':
    # 'product_code':
    # 'review_count':
    # 'screen_diagonal':
    # 'display_resolution':
    # 'characteristics':
}


def parameters():

    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://www.google.com/',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'TE': 'Trailers',
    }

    url = ''

    return url, headers

"""Check for empty string"""
def check_value(value):
    if value is None: return None
    value = value.strip()
    return value if value else None

"""The main function of the parser"""
def parse_brain(url, headers):
    product = {}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    try:
        value = soup.find('h1', class_='desktop-only-title')
        product['title'] = check_value(value.text)
    except AttributeError:
        product['title'] = None

    try:
        value = soup.select_one('a[title*="колір"i]')
        product['color'] = check_value(value.text)
    except AttributeError:
        product['color'] = None

    # Parsimo memory and unit of measurement
    memory = soup.select_one('a[title*="вбудована пам"i]')
    # Parsing logic (memory size)
    try:
        # Only chile values
        m_filter = ''.join(filter(str.isdigit, memory.text))
        product['memory_size'] = int(m_filter)

    except (AttributeError, ValueError):
        product['memory_size'] = None


    # Parsing logic (memory units)
    try:
        # Only literal values
        unit = ''.join(filter(str.isalpha, memory.text)).upper()
        if unit in ['MB', 'GB', 'TB', 'ГБ', 'МБ', 'ТБ']:
            product['memory_unit'] = unit
        else:
            product['memory_unit'] = None
    except (AttributeError, ValueError):
        product['memory_unit'] = None


    try:
        value = soup.find('span', string="Виробник").find_next("span")
        product['manufacturer'] = check_value(value.text)
    except AttributeError:
        product['manufacturer'] = None


    # Block all prices
    block_div = soup.find('div', class_='main-price-block')

    # Price in int format
    try:
        value = block_div.find_all('span')
        product['price'] = int(''.join(filter(str.isdigit, value[0].text)))
        if len(value) > 1:
            product['price_discount'] = int(''.join(filter(str.isdigit, value[1].text)))
        else:
            product['price_discount'] = None
    except (AttributeError, IndexError, ValueError):
        product['price'] = None
        product['price_discount'] = None

    try:
        block_a = soup.find_all('a', class_="product-modal-button")
        product['img_url'] = [a.find('img')['src'] for a in block_a]

    except AttributeError:
        product['img_url'] = None


    for k, v in product.items():
        print(f"{k}: {v}")



def main():
    url, headers = parameters()
    parse_brain(url, headers)


if __name__ == '__main__':
    main()