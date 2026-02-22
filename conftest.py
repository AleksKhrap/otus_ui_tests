import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOption
from selenium.webdriver.firefox.options import Options as FFOptions


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
