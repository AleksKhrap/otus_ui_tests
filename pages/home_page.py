import time

from selenium.webdriver.common.by import By
from .base_page import BasePage
import random

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage(BasePage):
    LOGO = (By.XPATH, '//*[@id="_desktop_logo"]')
    CLOTHES_BTN = (By.XPATH, '//li[@id="category-3"]')
    CLOTHES_FOR_MEN_BTN = (By.XPATH, '//li[@id="category-4"]')
    SIGN_IN = (By.XPATH, '//div[@id="_desktop_user_info"]')
    CART = (By.XPATH, '//div[@id="_desktop_cart"]')

    PRODUCTS = (By.XPATH, '//*[contains(@class, "js-product-miniature")]')
    ADD_TO_CART_BTN = (By.XPATH, '//button[@data-button-action="add-to-cart"]')
    CLOSE_BUTTON = (By.XPATH, '//*[@id="blockcart-modal"]//button[@class="close"]')
    CART_ITEMS = (By.XPATH, '//*[@class="cart-item"]')

    MODAL_LABEL = (By.XPATH, '//*[@id="myModalLabel"]')

    def check_page_elements(self):
        self.browser.find_element(*self.LOGO)
        self.browser.find_element(*self.CLOTHES_BTN)
        self.browser.find_element(*self.CLOTHES_FOR_MEN_BTN)
        self.browser.find_element(*self.SIGN_IN)
        self.browser.find_element(*self.CART)

    def open_product_page(self):
        all_products = self.browser.find_elements(*self.PRODUCTS)
        if all_products:
            random_product = random.choice(all_products)
            random_product.click()
        else:
            raise Exception("Products not found")

    def add_to_cart(self):
        WebDriverWait(self.browser, 2).until(EC.visibility_of_element_located(self.ADD_TO_CART_BTN)).click()
        WebDriverWait(self.browser, 4).until(EC.visibility_of_element_located(self.CLOSE_BUTTON)).click()

    def check_cart(self):
        WebDriverWait(self.browser, 3).until(EC.invisibility_of_element_located(self.MODAL_LABEL))
        self.browser.find_element(*self.CART).click()
        products_list = self.browser.find_elements(*self.CART_ITEMS)
        assert len(products_list) == 1

    def check_prices(self):
        initial_price_list, new_price_list = self.get_prices(self.PRICES, self.CURRENCY_BUTTON, self.DOLLAR)
        assert initial_price_list != new_price_list
