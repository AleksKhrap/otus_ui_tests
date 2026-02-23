from selenium.webdriver.common.by import By
from .base_page import BasePage
from selenium.webdriver.common.action_chains import ActionChains
from utils import get_prices, click_on_random_element


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
        self.assert_element_visible(self.LOGO)

        clothes_button = self.assert_element_visible(self.CLOTHES_BTN)
        ActionChains(self.browser).move_to_element(clothes_button).perform()
        self.assert_element_visible(self.CLOTHES_FOR_MEN_BTN)

        self.assert_element_visible(self.SIGN_IN)
        self.assert_element_visible(self.CART)

    def open_product_page(self):
        all_products = self.find_all_elements(self.PRODUCTS)
        if all_products:
            click_on_random_element(all_products)
        else:
            raise Exception("Products not found")

    def add_to_cart(self):
        self.assert_element_visible(self.ADD_TO_CART_BTN).click()
        self.assert_element_visible(self.CLOSE_BUTTON).click()

    def check_cart(self):
        self.assert_element_invisible(self.MODAL_LABEL)
        self.assert_element_visible(self.CART).click()
        products_list = self.find_all_elements(self.CART_ITEMS)
        assert len(products_list) == 1

    def check_prices(self):
        initial_price_list, new_price_list = get_prices(self)
        assert initial_price_list != new_price_list
