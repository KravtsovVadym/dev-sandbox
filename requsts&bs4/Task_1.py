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




if __name__ == '__main__':
    main()
