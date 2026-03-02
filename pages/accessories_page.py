from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils import PRICES, get_prices


class AccessoriesPage(BasePage):
    SEARCH_FILTERS = (By.XPATH, '//div[@id="search_filters"]')
    SORT_BY = (By.XPATH, '//button[@class="btn-unstyle select-title"]')
    PRODUCT_LIST = (By.XPATH, '//*[@class="products row"]')
    WISHLISTS = (By.XPATH, '//button[@class="wishlist-button-add"]')

    def assert_page_elements_is_visible(self):
        self.assert_element_visible(self.PRODUCT_LIST)
        self.assert_element_visible(PRICES)
        self.assert_element_visible(self.SORT_BY)
        self.assert_element_visible(self.SEARCH_FILTERS)
        self.assert_element_visible(self.WISHLISTS)

    def check_prices(self):
        initial_price_list, new_price_list = get_prices(self)
        assert initial_price_list != new_price_list
