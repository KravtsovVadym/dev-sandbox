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
img_ulr
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