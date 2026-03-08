from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure


class ProductPage(BasePage):
    ADD_TO_CART_BTN = (By.XPATH, '//button[@data-button-action="add-to-cart"]')
    SIZE = (By.XPATH, '//select[@id="group_1"]')
    QUANTITY = (By.XPATH, '//input[@id="quantity_wanted"]')
    PRODUCT_DESCRIPTION = (By.XPATH, '//div[@id="product-description-short-1"]')
    REGULAR_PRICE = (By.XPATH, '//*[@class="regular-price"]')

    @allure.step("Проверка видимости страницы товара")
    def assert_page_is_visible(self):
        self.logger.info("Проверка видимости страницы товара")

        self.assert_element_visible(self.ADD_TO_CART_BTN)
        self.assert_element_visible(self.SIZE)
        self.assert_element_visible(self.QUANTITY)
        self.assert_element_visible(self.PRODUCT_DESCRIPTION)
        self.assert_element_visible(self.REGULAR_PRICE)

        self.logger.info("Все элементы страницы товара видимы")
