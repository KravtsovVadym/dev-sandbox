"""
This module parses the ad on the page.

This module uses search approaches
using (find / find_all), the Beautifulsoup library
The find method is technically faster than select() or select_one()
as it does not call third-party libraries


Next example (model fields that need to be parsed).
Fields in database
===================
title
color
memory_size
memory_unit
manufacturer
price
price_discount
img_url
product_code
review_count
screen_diagonal
display_resolution
characteristics
====================
"""

import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup


def config():
    cookies = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0",
    }
    url = "https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html"

    r = requests.get(url, headers=headers, cookies=cookies)
    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        print(f"Error {e}")
    soup = BeautifulSoup(r.text, "lxml")

    return soup


def parse_title(soup):
    try:
        return soup.find("h1", class_="desktop-only-title").text.strip()
    except AttributeError as e:
        print(f"Element not found: {e}")
        return None


def parse_color(soup):
    try:
        return soup.find("a", title=lambda s: s and "колір" in s.lower()).text.strip()
    except AttributeError as e:
        print(f"Element not found: {e}")
        return None


def parse_product_code(soup):
    try:
        return soup.find("span", class_="br-pr-code-val").text.strip()
    except AttributeError as e:
        print(f"Element not found: {e}")
        return None


def parse_manufacturer(soup):
    try:
        return soup.find("span", string="Виробник").find_next("span").text.strip()
    except AttributeError as e:
        print(f"Element not found: {e}")
        return None


def parse_img_url(soup):
    try:
        block_a_img = soup.find_all("a", class_="product-modal-button")
        return [a.find("img")["src"] for a in block_a_img]
    except AttributeError as e:
        print(f"Element not found: {e}")
        return None


def parse_review_count(soup):
    try:
        return int(
            "".join(
                soup.find("div", class_="br-pt-rt-main-mark").find_next("span").text
            )
        )
    except (AttributeError, ValueError) as e:
        print(f"Element not found: {e}")
        return None


def parse_screen_diagonal(soup):
    try:
        return float(
            soup.find(
                "a", title=lambda s: s and "діагональ екрану" in s.lower()
            ).text.rstrip('"')
        )
    except (AttributeError, ValueError) as e:
        print(f"Element not found: {e}")
        return None


def parse_display_resolution(soup):
    try:
        return soup.find(
            "a", title=lambda s: s and "роздільна здатність" in s.lower()
        ).text.strip()
    except AttributeError as e:
        print(f"Element not found: {e}")
        return None


def parse_price(soup):
    price = None
    price_discount = None

    try:
        block_div_prc = soup.find("div", {"data-series-product-id": "0"}).find_all(
            "span"
        )
        price = int("".join(filter(str.isdigit, block_div_prc[0].text)))

        if len(block_div_prc) == 2:
            return int("".join(filter(str.isdigit, block_div_prc[1].text)))
    except (AttributeError, IndexError, ValueError) as e:
        print(f"Error: {e}")
        return price, price_discount

    return price, price_discount


def parse_memory(soup):
    a_tag = soup.find("a", title=lambda s: s and "вбудована пам'ять" in s.lower())
    memory = None
    unit = None
    try:
        # Parsing logic (memory size)
        # Integer values ​​only
        memory = int("".join(filter(str.isdigit, a_tag.text)))
    except (AttributeError, ValueError) as e:
        print(f"Error: {e}")
        return memory, unit
    # Parsing logic (memory units)
    try:
        # Literal values only
        unchek_unit = "".join(filter(str.isalpha, a_tag.text.upper()))
        if unchek_unit in ["MB", "GB", "TB", "ГБ", "МБ", "ТБ"]:
            unit = unchek_unit
    except (AttributeError, ValueError) as e:
        print(f"Error: {e}")
        return memory, unit

    return memory, unit


def parse_characteristic(soup):
    all_chr = {}
    # The main unit with all the characteristics
    block_div_chr = soup.find("div", class_="br-pr-chr")
    if not block_div_chr:
        return None

    # Blocks that contain names and characteristics
    block_div_item = block_div_chr.find_all("div")
    if not block_div_item:
        return None

    for div_tag in block_div_item:
        h3_key = None  # Characteristic block name
        try:
            if h3_tag := div_tag.find("h3"):
                h3_key = h3_tag.text.strip()
        except AttributeError as e:
            print(f"Error block characteristics: {e}")
            return None

        if not h3_key:
            continue

        # A block that contains only characteristics by category
        block = div_tag.find("div")
        if not block:
            continue

        desc_chr = {}  # To store title and feature

        # Parse recursive all title with feature
        for block_div in block.find_all("div"):
            desc_title = None
            desc_feat = None

            spans = block_div.find_all("span")

            if not spans:
                continue

            try:  # This block title 'chr'
                desc_title = spans[0].text
            except AttributeError as e:
                print(f"Element not found: {e}")
                desc_title = None

            # This block feature
            if len(spans) > 1:
                try:
                    desc_feat = " ".join(spans[1].text.split())
                except AttributeError as e:
                    print(f"Element not found: {e}")
                    desc_feat = None

            desc_chr[desc_title] = desc_feat
        all_chr[h3_key] = desc_chr

    return all_chr


def main():
    soup = config()
    # Prevents functions from being retriggered
    memory_size, memory_unit = parse_memory(soup)
    price, price_discount = parse_price(soup)
    product = {  # Fields in database
        "title": parse_title(soup),
        "color": parse_color(soup),
        "memory_size": memory_size,
        "memory_unit": memory_unit,
        "manufacturer": parse_manufacturer(soup),
        "price": price,
        "price_discount": price_discount,
        "img_url": parse_img_url(soup),
        "product_code": parse_product_code(soup),
        "review_count": parse_review_count(soup),
        "screen_diagonal": parse_screen_diagonal(soup),
        "display_resolution": parse_display_resolution(soup),
        "characteristics": parse_characteristic(soup),
    }
    # Immediately save in json, for further use
    with open("../files/parse_data_brain.json", "w", encoding="utf-8") as file:
        json.dump(product, file, ensure_ascii=False, indent=4)

    pprint(product)


if __name__ == "__main__":
    main()
