"""
In this module we parse the Brain page:
Use Playwright and XPATH tools.

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

from pprint import pprint
import json

from playwright.sync_api import (
    sync_playwright,
    TimeoutError,
    Error,
)


# Browser configuration
def config(pw):
    browser = pw.chromium.launch(args=["--disable-blink-features=AutomationControlled"])

    context = browser.new_context(
        permissions=["geolocation"],
        geolocation={"latitude": 50.45, "longitude": 30.52},
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        ),
        viewport={"width": 1920, "height": 1080},
        locale="uk-UA",
        timezone_id="Europe/Kyiv",
    )
    return context, browser


# Site configuration
def run_site(ctx, bw):
    """Open main page and perform search input"""
    try:
        page = ctx.new_page()
        page.goto("https://brain.com.ua")
        page.set_default_timeout(5000)
    except (Error, TimeoutError) as e:
        print(f"Error Playwright: {e}")
        return

    try:
        # Input and input text in search string
        search_input = page.locator(
            '//input[@class="search-button-first-form"]/preceding::input[1]'
        )
        search_input.fill("Apple iPhone 15 128GB Black")
        # Find and click on the search button
        page.locator('//input[@class="qsr-submit"]').click()
    except (Error, TimeoutError) as e:
        print(f"Error Playwright: {e}")
        return

    try:
        # Click on first result search
        first_link = page.locator('//div[@class="tab-content-wrapper"]//a')
        first_link.first.click()
    except (Error, TimeoutError) as e:
        print(f"Error Playwright: {e}")
        return

    return page


def extract_title(pg):
    try:
        return (
            pg.locator('//h1[contains(@class, "desktop-only-title")]')
            .text_content()
            .strip()
        )
    except (Error, TimeoutError):
        # print(f"Error Playwright: {e}")
        return None


def extract_color(pg):
    try:
        return pg.locator('//a[contains(@title, "Колір")]').text_content().strip()
    except (Error, TimeoutError) as e:
        print(f"Error Playwright: {e}")
        return None


def extract_memory(pg):
    try:
        memory_list = (
            pg.locator('//a[contains(@title, "пам\'ять")]').text_content().split()
        )
        if (
            len(memory_list) > 1
            and memory_list[0].isdigit()
            and memory_list[1].upper() in ["MB", "GB", "TB"]
        ):
            # Order First(memory), Second(unit)
            return memory_list[0], memory_list[1].upper()
        else:
            return memory_list[0], None
    except (Error, TimeoutError) as e:
        print(f"Error Playwright: {e}")
        return None


def extract_manufacturer(pg):
    try:
        return (
            pg.locator('//span[text()="Виробник"]/following-sibling::span[1]')
            .text_content()
            .strip()
        )
    except (Error, TimeoutError) as e:
        print(f"Error Playwright: {e}")
        return None


def extract_price(pg):
    try:
        price_list = pg.locator(
            '//div[contains(@class,"main-price-block")]//span'
        ).all()
        if len(price_list) > 1:
            price = int("".join(filter(str.isdigit, price_list[0].text_content())))
            price_discount = int(
                "".join(filter(str.isdigit, price_list[1].text_content()))
            )
            # First price, Seconds price discount
            return price, price_discount
        # If not price discount
        if price_list:
            return price_list[0], None
    except (Error, TimeoutError) as e:
        print(f"Error Playwright: {e}")
        return None


def extract_img_url(pg):
    try:
        a_list = pg.locator('//a[contains(@class, "product-modal-button")]').all()
        img_list = [a.locator("//img").get_attribute("src") for a in a_list]
        return img_list
    except (Error, TimeoutError) as e:
        print(f"Error Playwright: {e}")
        return None


def extract_code(pg):
    try:
        return (
            pg.locator(
                '//div[contains(@class, "main-right-block")]//span[contains(@class,"pr-code-val")]'
            )
            .text_content()
            .strip()
        )
    except (Error, TimeoutError) as e:
        print(f"Error Playwright: {e}")
        return None


def extract_review(pg):
    try:
        review = pg.locator('//div[contains(@class, "br-pt-rating")]//a/span')
        return int(review.text_content().strip())
    except (Error, TimeoutError) as e:
        print(f"Error Playwright: {e}")
        return None


def extract_diagonal(pg):
    try:
        diagonal_element = pg.locator('//a[contains(@title, "Діагональ")]')
        return float(diagonal_element.text_content().rstrip('"'))
    except (Error, TimeoutError) as e:
        print(f"Error Playwright: {e}")
        return None


def extract_resolution(pg):
    try:
        return (
            pg.locator('//a[contains(@title, "Роздільна здатність")]')
            .text_content()
            .strip()
        )
    except (Error, TimeoutError) as e:
        print(f"Error Playwright: {e}")
        return None


def characteristics(pg):
    all_chr = {}

    block_div_chr = pg.locator('//div[@class= "br-pr-chr"]/div').all()
    for div_parent in block_div_chr:
        h3 = None  # Title block chracteristic
        try:
            h3 = div_parent.locator("xpath=./h3").text_content()
        except (Error, TimeoutError):
            # print(f"Error Playwright {e}")
            pass
        cases_chr = {}  # For keys and values (characteristic)
        # In this cycle, get all spans from divs
        for div_child in div_parent.locator("xpath=./div//div").all():
            key_name = None
            val_desc = None
            spans = div_child.locator("xpath=./span").all()
            try:
                if key_name := spans[0].text_content().strip():
                    pass
                if val_desc := "".join(spans[1].text_content().split()):
                    pass
            except (Error, TimeoutError) as e:
                print(f"Error Playwright: {e}")
                pass
            cases_chr[key_name] = val_desc
        all_chr[h3] = cases_chr

    return all_chr


def main():
    with sync_playwright() as p:
        context, browser = config(p)
        page = run_site(context, browser)
        memory_size, memory_unit = extract_memory(page)
        price, price_discount = extract_price(page)
        product = {
            "title": extract_title(page),
            "color": extract_color(page),
            "memory_size": memory_size,
            "memory_unit": memory_unit,
            "manufacturer": extract_manufacturer(page),
            "price": price,
            "price_discount": price_discount,
            "img_url": extract_img_url(page),
            "product_code": extract_code(page),
            "review_count": extract_review(page),
            "screen_diagonal": extract_diagonal(page),
            "display_resolution": extract_resolution(page),
            "characteristics": characteristics(page),
        }

        browser.close()
        # Immediately save in json, for further use
        with open("../files/parse_data_brain.json", "w", encoding="utf-8") as file:
            json.dump(product, file, ensure_ascii=False, indent=4)

        pprint(product)


if __name__ == "__main__":
    main()
