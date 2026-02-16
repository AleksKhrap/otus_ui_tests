from pages.accessories_page import AccessoriesPage
import pytest


class TestAccessoriesPage:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        self.accessories_page = AccessoriesPage(browser, browser.base_url + "/6-accessories")
        self.accessories_page.open()

    def test_check_accessories_page_availability(self):
        self.accessories_page.check_page_elements()

    def test_change_currency_and_check_prices(self):
        self.accessories_page.check_prices()
