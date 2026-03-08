from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils import PRICES, get_prices
import allure


class AccessoriesPage(BasePage):
    SEARCH_FILTERS = (By.XPATH, '//div[@id="search_filters"]')
    SORT_BY = (By.XPATH, '//button[@class="btn-unstyle select-title"]')
    PRODUCT_LIST = (By.XPATH, '//*[@class="products row"]')
    WISHLISTS = (By.XPATH, '//button[@class="wishlist-button-add"]')

    @allure.step("Проверка видимости всех элементов страницы аксессуаров")
    def assert_page_elements_is_visible(self):
        self.logger.info("Проверка видимости элементов страницы аксессуаров")

        self.assert_element_visible(self.PRODUCT_LIST)
        self.assert_element_visible(PRICES)
        self.assert_element_visible(self.SORT_BY)
        self.assert_element_visible(self.SEARCH_FILTERS)
        self.assert_element_visible(self.WISHLISTS)

        self.logger.info("Все элементы страницы аксессуаров видимы")

    @allure.step("Проверка изменения цен при смене валюты")
    def check_prices(self):
        self.logger.info("Проверка изменения цен при смене валюты")

        initial_price_list, new_price_list = get_prices(self)

        self.logger.debug(f"Цены в EUR: {initial_price_list}")
        self.logger.debug(f"Цены в USD: {new_price_list}")

        assert initial_price_list != new_price_list

        self.logger.info("Цены успешно изменились")
