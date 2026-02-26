import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOption
from selenium.webdriver.firefox.options import Options as FFOptions

from pages.accessories_page import AccessoriesPage
from pages.admin_page import AdminPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.registration_page import RegistrationPage
from utils import open_page


def pytest_addoption(parser):
    parser.addoption("--browser", default="ch")
    parser.addoption("--headless", action="store_true")
    parser.addoption("--url", default="http://localhost:8081")


@pytest.fixture()
def browser(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    base_url = request.config.getoption("--url")

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

    yield driver
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
