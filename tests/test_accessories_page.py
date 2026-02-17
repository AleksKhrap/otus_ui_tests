from pages.accessories_page import AccessoriesPage
import pytest
from utils import open_page


class TestAccessoriesPage:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        self.accessories_page = AccessoriesPage(browser)
        open_page(self.accessories_page, browser.base_url + "/6-accessories")

    def test_check_accessories_page_availability(self):
        self.accessories_page.check_page_elements()

    def test_change_currency_and_check_prices(self):
        self.accessories_page.check_prices()
