from selenium.webdriver.common.by import By
import random
import string
from datetime import date, timedelta, datetime
import logging

PRICES = (By.XPATH, '//*[@class="price"]')
CURRENCY_BUTTON = (By.XPATH, '//button[@data-toggle="dropdown"]')
DOLLAR = (By.XPATH, '//*[@title="US Dollar"]')

EMAIL_DOMAINS = ["mail.ru", "gmail.com", "yandex.ru", "bk.ru"]

logger = logging.getLogger("utils")

def open_page(page, url):
    logger.info(f"Открытие страницы: {url}")
    page.browser.get(url)

def get_prices(page):
    logger.info("Получение цен и переключение валюты")

    initial_prices = page.find_all_elements(PRICES)
    initial_price_list = [price.text.strip().replace('€', '').replace(',', '') for price in initial_prices]

    logger.debug(f"Начальные цены (EUR): {initial_price_list}")

    page.get_visible_element(CURRENCY_BUTTON).click()
    page.get_visible_element(DOLLAR).click()

    new_prices = page.find_all_elements(PRICES)
    new_price_list = [price.text.strip().replace('$', '').replace(',', '') for price in new_prices]

    logger.debug(f"Новые цены (USD): {new_price_list}")

    return initial_price_list, new_price_list

def get_random_string(length=10):
    return "".join([random.choice(string.ascii_letters) for _ in range(length)])

def get_random_email():
    email = f'{get_random_string()}@{random.choice(EMAIL_DOMAINS)}'
    logger.debug(f"Сгенерирован email: {email}")
    return email

def get_random_date(start_year=1910, end_year=datetime.now().year):
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)

    days_between = (end_date - start_date).days

    random_days = random.randint(0, days_between)

    new_date = start_date + timedelta(days=random_days)

    date_str = new_date.strftime('%m/%d/%Y')

    logger.debug(f"Сгенерирована дата: {date_str}")

    return date_str

def get_random_price(min_price=10.0, max_price=1000.0):
    price = round(random.uniform(min_price, max_price), 2)
    logger.debug(f"Сгенерирована цена: {price}")
    return price
