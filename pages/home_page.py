from selenium.webdriver.common.by import By
from .base_page import BasePage
from selenium.webdriver.common.action_chains import ActionChains
from utils import get_prices
import allure


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

    @allure.step("Проверка видимости элементов главной страницы")
    def assert_page_elements_is_visible(self):
        self.logger.info("Проверка видимости элементов главной страницы")

        self.assert_element_visible(self.LOGO)

        clothes_button = self.get_visible_element(self.CLOTHES_BTN)
        ActionChains(self.browser).move_to_element(clothes_button).perform()
        self.assert_element_visible(self.CLOTHES_FOR_MEN_BTN)

        self.assert_element_visible(self.SIGN_IN)
        self.assert_element_visible(self.CART)

        self.logger.info("Все элементы главной страницы видимы")

    @allure.step("Открытие страницы случайного товара")
    def open_product_page(self):
        self.logger.info("Открытие страницы случайного товара")

        all_products = self.find_all_elements(self.PRODUCTS)
        if all_products:
            self.click_on_random_element(all_products)
            self.logger.debug(f"Выбран товар из {len(all_products)} доступных")
        else:
            self.logger.error("Товары не найдены на главной странице")
            raise Exception("Products not found")

    @allure.step("Добавление товара в корзину")
    def add_to_cart(self):
        self.logger.info("Добавление товара в корзину")

        self.get_visible_element(self.ADD_TO_CART_BTN).click()
        self.get_visible_element(self.CLOSE_BUTTON).click()

        self.logger.info("Товар добавлен в корзину")

    @allure.step("Проверка корзины")
    def check_cart(self):
        self.logger.info("Проверка корзины")

        self.assert_element_invisible(self.MODAL_LABEL)
        self.get_visible_element(self.CART).click()

        products_list = self.find_all_elements(self.CART_ITEMS)
        self.logger.debug(f"Найдено товаров в корзине: {len(products_list)}")

        assert len(products_list) == 1

        self.logger.info("Корзина проверена успешно")

    @allure.step("Проверка изменения цен при смене валюты")
    def check_prices(self):
        self.logger.info("Проверка изменения цен при смене валюты")

        initial_price_list, new_price_list = get_prices(self)

        self.logger.debug(f"Цены до смены валюты: {initial_price_list}")
        self.logger.debug(f"Цены после смены валюты: {new_price_list}")

        assert initial_price_list != new_price_list

        self.logger.info("Цены успешно изменились")
