from pages.product_page import ProductPage
import pytest


class TestProductPage:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        self.product_page = ProductPage(browser, browser.base_url +
                                        "/1-1-hummingbird-printed-t-shirt.html#/1-size-s/8-color-white")
        self.product_page.open()

    def test_check_product_page_availability(self):
        self.product_page.page_is_visible()
