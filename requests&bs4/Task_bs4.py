"""
Fields database:
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


from bs4 import BeautifulSoup
import requests
from pprint import pprint

def config():
    cookies = {}
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

    url = 'https://example-shop.com/product-page.html'

    # r = requests.get(url, headers=headers, cookies=cookies)
    # try:
    #     r.raise_for_status()
    # except requests.HTTPError as e:
    #     print(f"Error {e}")
    # soup = BeautifulSoup(r.text, 'lxml')

    #  For the parse test locally
    with open('page.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')

    return soup

def parse_title(soup):
    try:
        return soup.find('h1', class_="item-header").text.strip()
    except AttributeError:
        return  None


def parse_color(soup):
    try:
        return soup.find('a', title=lambda s: s and "колір" in s.lower()).text.strip()
    except AttributeError:
        return None


def parse_product_code(soup):
    try:
        return  soup.find('span', class_="code-value").text.strip()
    except AttributeError:
        return None


def parse_manufacturer(soup):
    try:
        return  soup.find('span', string="Виробник").find_next("span").text.strip()
    except AttributeError:
        return  None


def parse_img_url(soup):
    try:
        block_a_img = soup.find_all('a', class_="image-link")
        return  [a.find('img')['src'] for a in block_a_img]
    except AttributeError:
        return  None


def parse_review_count(soup):
    try:
        return  int(''.join(soup.find('div', class_="rating-block").find_next('span').text))
    except (AttributeError, ValueError):
        return  None
