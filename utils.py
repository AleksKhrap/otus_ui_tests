from selenium.webdriver.common.by import By
import random
import string
from datetime import date, timedelta, datetime

PRICES = (By.XPATH, '//*[@class="price"]')
CURRENCY_BUTTON = (By.XPATH, '//button[@data-toggle="dropdown"]')
DOLLAR = (By.XPATH, '//*[@title="US Dollar"]')

def open_page(page, url):
    page.browser.get(url)

def get_prices(page):
    initial_prices = page.find_all_elements(PRICES)
    initial_price_list = [price.text.strip().replace('€', '').replace(',', '') for price in initial_prices]

    page.get_visible_element(CURRENCY_BUTTON).click()
    page.get_visible_element(DOLLAR).click()

    new_prices = page.find_all_elements(PRICES)
    new_price_list = [price.text.strip().replace('$', '').replace(',', '') for price in new_prices]

    return initial_price_list, new_price_list

def get_random_string(length=10):
    return "".join([random.choice(string.ascii_letters) for _ in range(length)])

def get_random_email():
    return (get_random_string() + "@" + random.choice(["mail", "gmail", "yandex", "bk"])
            + "." + random.choice(["com", "org", "ru"]))

def get_random_date(start_year=1910, end_year=datetime.now().year):
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)

    days_between = (end_date - start_date).days

    random_days = random.randint(0, days_between)

    new_date = start_date + timedelta(days=random_days)

    return new_date.strftime('%m/%d/%Y')

def get_random_price(min_price=10.0, max_price=1000.0):
    return round(random.uniform(min_price, max_price), 2)
