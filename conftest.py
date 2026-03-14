import pytest
import allure
import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOption
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

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
            logger = logging.getLogger("conftest")

            try:
                screenshot = browser.get_screenshot_as_png()

                allure.attach(
                    screenshot,
                    name=f"failure_screenshot_{datetime.now().strftime('%H%M%S')}",
                    attachment_type=allure.attachment_type.PNG
                )

                logger.error(f"Тест {item.name} упал. Скриншот сохранен в отчете Allure")
            except Exception as e:
                logger.error(f"Сессия была закрыта до скриншота: {e}")


def pytest_configure():
    setup_logging()

    logger = logging.getLogger()
    logger.info("ЗАПУСК ТЕСТОВ")
    logger.info(f"Время: {datetime.now()}")


def pytest_addoption(parser):
    parser.addoption("--browser", default="ch")
    parser.addoption("--headless", action="store", default="true")
    parser.addoption("--url", default="http://localhost:8081")
    parser.addoption("--executor", action="store", default="local")
    parser.addoption("--browser_version", action="store", default="latest")


@pytest.fixture()
def browser(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless") == "true"
    base_url = request.config.getoption("--url")
    executor = request.config.getoption("--executor")
    browser_version = request.config.getoption("--browser_version")

    logger = logging.getLogger()
    logger.info(f"Запуск браузера: {browser_name}, headless: {headless}, executor: {executor}")

    driver = None

    if browser_name in ["ff", "firefox"]:
        browser_name = "firefox"
        options = FFOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    elif browser_name == "edge":
        options = EdgeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    else:
        browser_name = "chrome"
        options = ChromeOption()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    if headless:
        options.add_argument("--headless")

    if executor == "selenoid":
        command_executor = "http://selenoid:4444/wd/hub"
        logger.info(f"Selenoid: {command_executor}")

        options.set_capability("browserName", browser_name)
        options.set_capability("browserVersion", browser_version)

        options.set_capability(
            "selenoid:options",
            {
                "enableVNC": True,
                "enableVideo": False,
                "sessionTimeout": "3m"
            }
        )

        driver = webdriver.Remote(
            command_executor=command_executor,
            options=options
        )

    else:
        if browser_name == "firefox":
            driver = webdriver.Firefox(options=options)
        elif browser_name == "edge":
            driver = webdriver.Edge(options=options)
        else:
            driver = webdriver.Chrome(options=options)

        driver.set_page_load_timeout(180)

    driver.base_url = base_url

    if not headless:
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
