from selenium.webdriver.common.by import By
from .base_page import BasePage


class ProductPage(BasePage):
    ADD_TO_CART_BTN = (By.XPATH, '//button[@data-button-action="add-to-cart"]')
    SIZE = (By.XPATH, '//select[@id="group_1"]')
    QUANTITY = (By.XPATH, '//input[@id="quantity_wanted"]')
    PRODUCT_DESCRIPTION = (By.XPATH, '//div[@id="product-description-short-1"]')
    REGULAR_PRICE = (By.XPATH, '//*[@class="regular-price"]')

    def page_is_visible(self):
        self.browser.find_element(*self.ADD_TO_CART_BTN)
        self.browser.find_element(*self.SIZE)
        self.browser.find_element(*self.QUANTITY)
        self.browser.find_element(*self.PRODUCT_DESCRIPTION)
        self.browser.find_element(*self.REGULAR_PRICE)
