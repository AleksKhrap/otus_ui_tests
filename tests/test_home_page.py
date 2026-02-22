from pages.home_page import HomePage
from utils import open_page
import pytest


class TestHomePage:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        self.home_page = HomePage(browser)
        open_page(self.home_page, browser.base_url)

    def test_check_home_page_availability(self):
        self.home_page.check_page_elements()

    def test_add_product_to_cart(self):
        self.home_page.open_product_page()
        self.home_page.add_to_cart()
        self.home_page.check_cart()

    def test_change_currency_and_check_prices(self):
        self.home_page.check_prices()
