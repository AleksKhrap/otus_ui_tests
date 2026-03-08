import pytest
import allure
import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOption
from selenium.webdriver.firefox.options import Options as FFOptions

from pages.accessories_page import AccessoriesPage
from pages.admin_page import AdminPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.registration_page import RegistrationPage
from utils import open_page
from logger_config import setup_logging


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для обработки результатов теста и добавления скриншотов при падении"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        if "browser" in item.fixturenames:
            browser = item.funcargs["browser"]

            screenshot = browser.get_screenshot_as_png()

            allure.attach(
                screenshot,
                name=f"failure_screenshot_{datetime.now().strftime('%H%M%S')}",
                attachment_type=allure.attachment_type.PNG
            )

            logger = logging.getLogger("conftest")
            logger.error(f"Тест {item.name} упал. Скриншот сохранен в отчете Allure")


def pytest_configure():
    setup_logging()

    logger = logging.getLogger()
    logger.info("ЗАПУСК ТЕСТОВ")
    logger.info(f"Время: {datetime.now()}")


def pytest_addoption(parser):
    parser.addoption("--browser", default="ch")
    parser.addoption("--headless", action="store_true")
    parser.addoption("--url", default="http://localhost:8081")


@pytest.fixture()
def browser(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    base_url = request.config.getoption("--url")

    logger = logging.getLogger()
    logger.info(f"Запуск браузера: {browser_name}, headless: {headless}")

    driver = None

    if browser_name == "ff":
        options = FFOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    elif browser_name == "edge":
        driver = webdriver.Edge()
    else:
        options = ChromeOption()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

    driver.base_url = base_url
    driver.maximize_window()
    driver.implicitly_wait(3)

    logger.info(f"Базовый URL: {base_url}")

    yield driver

    logger.info("Закрытие браузера")
    driver.quit()


@pytest.fixture()
def accessories_page(browser):
    page = AccessoriesPage(browser)
    open_page(page, browser.base_url + "/6-accessories")
    return page


@pytest.fixture()
def admin_page(browser):
    page = AdminPage(browser)
    open_page(page, browser.base_url + "/administration")
    return page


@pytest.fixture()
def home_page(browser):
    page = HomePage(browser)
    open_page(page, browser.base_url)
    return page


@pytest.fixture()
def product_page(browser):
    page = ProductPage(browser)
    open_page(page, browser.base_url +
              "/1-1-hummingbird-printed-t-shirt.html#/1-size-s/8-color-white")
    return page


@pytest.fixture()
def registration_page(browser):
    page = RegistrationPage(browser)
    open_page(page, browser.base_url + "/registration")
    return page
