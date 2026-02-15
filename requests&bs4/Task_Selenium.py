"""
In this module we parse product pages:
Use Selenium and XPATH tools.

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
    ElementClickInterceptedException
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager



def config():
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)
    return driver, wait




def open_site(driver, wait):
    try:
        # Open site
        driver.get("https://brain.com.ua")
        # Find Search string
        search_box = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//input[@type="text" and @placeholder]'))
        )
        # Input text in search string
        search_box.send_keys('Apple iPhone 15 128GB Black')
        # Click to button
        search_box.send_keys(Keys.RETURN)
        # Go to the product page
        first_link = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//div[contains(@class, "content")]//a[1]'))
        )
        first_link.click()
        return True

    except (
        NoSuchElementException,
        TimeoutException,
        ElementClickInterceptedException
        ) as e:
        return False


def extract_title(wait):
    try:
        # wait until the element appears on the pages
        title_element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//h1[@itemprop="name"]')
                )
            )
        return title_element.get_attribute("textContent").strip()
    except (NoSuchElementException, TimeoutException) as e:
        return None