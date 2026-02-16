from selenium.webdriver.common.by import By
from .base_page import BasePage


class AccessoriesPage(BasePage):
    SEARCH_FILTERS = (By.XPATH, '//div[@id="search_filters"]')
    SORT_BY = (By.XPATH, '//button[@class="btn-unstyle select-title"]')
    PRODUCT_LIST = (By.XPATH, '//*[@class="products row"]')
    WISHLISTS = (By.XPATH, '//button[@class="wishlist-button-add"]')

    def check_page_elements(self):
        self.browser.find_element(*self.PRODUCT_LIST)
        self.browser.find_element(*self.PRICES)
        self.browser.find_element(*self.SORT_BY)
        self.browser.find_element(*self.SEARCH_FILTERS)
        self.browser.find_element(*self.WISHLISTS)

    def check_prices(self):
        initial_price_list, new_price_list = self.get_prices(self.PRICES, self.CURRENCY_BUTTON, self.DOLLAR)
        assert initial_price_list != new_price_list
