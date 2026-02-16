"""
In this module we parse the Brain page:
Use Selenium and XPATH tools.

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

from random import randint
from pprint import pprint
from time import sleep
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def config():
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)
    return driver, wait


def open_site(driver, wait):  # driver
    try:
        # Open site
        driver.get("https://brain.com.ua")
        # Find Search string
        search_box = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//input[@class="quick-search-input"]')
            )
        )
        # Input text in search string
        search_box.send_keys("Apple iPhone 15 128GB Black")
        # Click to buttom
        search_box.send_keys(Keys.RETURN)
        # Go to the product page
        first_link = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="tab-content-wrapper"]//a[1]')
            )
        )
        first_link.click()
        return True

    except (
        NoSuchElementException,
        TimeoutException,
        ElementClickInterceptedException,
    ) as e:
        print(f"Element not found {e}")
        return None


def extract_title(dw):
    try:
        return (
            dw.find_element(By.XPATH, '//h1[contains(@class, "desktop-only-title")]')
            .get_attribute("textContent")
            .strip()
        )
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Element not found: {e}")
        return None


def extract_color(dw):
    try:
        color_element = dw.find_element(By.XPATH, '//a[contains(@title, "Колір")]')
        #  We return through get_attribute, because the text is invisible
        return color_element.get_attribute("textContent").strip()
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        return None


def extract_memory(dw):
    try:
        memory_list = (
            dw.find_element(By.XPATH, '//a[contains(@title, "пам\'ять")]')
            .get_attribute("textContent")
            .split()
        )
        # Checking on memory and memory unit
        if (
            len(memory_list) > 1
            and memory_list[0].isdigit()
            and memory_list[1].upper() in ["MB", "GB", "TB"]
        ):
            # Order First(memory), Second(unit)
            return memory_list[0], memory_list[1].upper()
        else:
            return memory_list[0], None
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        return None


def extrakt_manufacturer(dw):
    try:
        manufacturer_element = dw.find_element(
            By.XPATH, '//span[text()="Виробник"]/following-sibling::span[1]'
        )
        return manufacturer_element.get_attribute("textContent").strip()
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        return None


def extract_price(dw):
    try:
        price_list = dw.find_elements(
            By.XPATH, '//div[contains(@class,"main-price-block")]//span'
        )
        if len(price_list) > 1:
            price = int(
                "".join(filter(str.isdigit, price_list[0].get_attribute("textContent")))
            )
            price_discount = int(
                "".join(filter(str.isdigit, price_list[1].get_attribute("textContent")))
            )
            # First price, Seconds price discount
            return price, price_discount
        # If not price discount
        if price_list:
            return price_list[0], None

    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        return None


def extract_img_url(dw):
    try:
        a_list = dw.find_elements(
            By.XPATH, '//a[contains(@class, "product-modal-button")]'
        )
        img_list = [
            a.find_element(By.XPATH, "//img").get_attribute("src") for a in a_list
        ]
        return img_list
    except NoSuchElementException as e:
        print(f"Element not found {e}")
        return None


def extract_code(dw):
    sleep(randint(2, 3))
    try:
        code_element = dw.find_element(
            By.XPATH,
            '//div[contains(@class, "main-right-block")]//span[contains(@class,"pr-code-val")]',
        )
        return code_element.get_attribute("textContent").strip()
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        return None


def extract_review(dw):
    try:
        review_element = dw.find_element(
            By.XPATH, '//div[contains(@class, "br-pt-rating")]//a/span'
        )
        return int(review_element.get_attribute("textContent").strip())
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        return None


def extract_diagonal(dw):
    try:
        diagonal_element = dw.find_element(
            By.XPATH, '//a[contains(@title, "Діагональ")]'
        )
        return float(diagonal_element.get_attribute("textContent").rstrip('"'))
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        return None


def extract_resolution(dw):
    try:
        resolution_element = dw.find_element(
            By.XPATH, '//a[contains(@title, "Роздільна здатність")]'
        )
        return resolution_element.get_attribute("textContent").strip()
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        return None


def characteristics(dw):
    all_chr = {}

    block_div_chr = dw.find_elements(By.XPATH, '//div[@class= "br-pr-chr"]/div')
    for div_parent in block_div_chr:
        h3 = None  # Title block chracteristic
        try:
            h3 = div_parent.find_element(By.XPATH, "./h3").get_attribute("textContent")
        except NoSuchElementException as e:
            print(f"Element not found {e}")
            pass
        cases_chr = {}  # For keys and values (characteristic) presave #######
        # In this cycle, we get all spans from divs
        for div_child in div_parent.find_elements(By.XPATH, "./div//div"):
            key_name = None
            val_desc = None
            spans = div_child.find_elements(By.XPATH, "./span")
            try:
                if key_name := spans[0].get_attribute("textContent").strip():
                    pass
                if val_desc := "".join(spans[1].get_attribute("textContent").split()):
                    pass
            except IndexError as e:
                print(f"Element not found: {e}")
                pass
            cases_chr[key_name] = val_desc
        all_chr[h3] = cases_chr

    return all_chr


def main():
    driver, wait = config()
    open_site(driver, wait)
    memory_size, memory_unit = extract_memory(driver)
    price, price_discount = extract_price(driver)
    product = {  # Fields in database
        "title": extract_title(driver),
        "color": extract_color(driver),
        "memory_size": memory_size,
        "memory_unit": memory_unit,
        "manufacturer": extrakt_manufacturer(driver),
        "price": price,
        "price_discount": price_discount,
        "img_url": extract_img_url(driver),
        "product_code": extract_code(driver),
        "review_count": extract_review(driver),
        "screen_diagonal": extract_diagonal(driver),
        "display_resolution": extract_resolution(driver),
        "characteristics": characteristics(driver),
    }
    driver.quit()
    # Immediately save in json, for further use
    with open("../files/parse_data_brain.json", "w", encoding="utf-8") as file:
        json.dump(product, file, ensure_ascii=False, indent=4)
    pprint(product)


if __name__ == "__main__":
    main()
