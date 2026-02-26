from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils import get_random_price
from config import settings


class AdminPage(BasePage):
    EMAIL = (By.XPATH, '//input[@id="email"]')
    PASSWORD = (By.XPATH, '//input[@id="passwd"]')
    SUBMIT_BUTTON = (By.XPATH, '//button[@id="submit_login"]')
    FORGOTTEN_PASSWORD = (By.XPATH, '//a[@id="forgot-password-link"]')
    STAY_LOGGED_IN = (By.XPATH, '//input[@id="stay_logged_in"]/..')

    EMPLOYEE_ICON = (By.XPATH, '//*[@id="employee_infos"]')
    SIGN_OUT = (By.XPATH, '//*[@id="header_logout"]')

    CATALOG_MENU = (By.XPATH, '//*[@id="subtab-AdminCatalog"]')
    PRODUCTS_SUBMENU = (By.XPATH, '//*[@id="subtab-AdminProducts"]')
    ADD_NEW_PRODUCT_BTN = (By.XPATH, '//*[@id="page-header-desc-configuration-add"]')

    MODAL_FRAME = (By.ID, "modal-create-product")
    IFRAME = (By.XPATH, '//iframe[@name="modal-create-product-iframe"]')
    ADD_PRODUCT_MODAL_BTN = (By.XPATH, '//*[@id="create_product_create"]')
    PRODUCT_NAME = (By.XPATH, '//*[@id="product_header_name_1"]')
    PRICING = (By.XPATH, '//*[@id="product_pricing-tab-nav"]')
    RETAIL_PRICE = (By.XPATH, '//*[@id="product_pricing_retail_price_price_tax_excluded"]')
    RESULT_RETAIL_PRICE = (By.XPATH, '//*[@id="product_pricing_retail_price_price_tax_included"]')
    COST_PRICE = (By.XPATH, '//*[@id="product_pricing_wholesale_price"]')

    SAVE_BUTTON = (By.XPATH, '//button[@id="product_footer_save"]')

    SUCCESSFUL_ALERT = (By.XPATH, '//*[@class="alert alert-success d-print-none"]')

    ALL_PRODUCT_IDS = (By.XPATH, '//*[contains(@class, "column-id_product")]')

    ADDITIONAL_ACTIONS = (By.XPATH, '//*[@id="product_grid_table"]/tbody/tr[1]//a[2]')
    DELETE_BUTTON = (By.XPATH, '//*[@id="product_grid_table"]/tbody/tr[1]//a[@data-title="Delete selection"]')
    MODAL_DELETE_BUTTON = (By.XPATH, '//button[@class="btn btn-danger btn-lg btn-confirm-submit"]')

    TEST_PRODUCT_NAME = "Test product"

    def assert_login_form_is_visible(self):
        self.assert_element_visible(self.EMAIL)
        self.assert_element_visible(self.PASSWORD)
        self.assert_element_visible(self.SUBMIT_BUTTON)
        self.assert_element_visible(self.FORGOTTEN_PASSWORD)
        self.assert_element_visible(self.STAY_LOGGED_IN)

    def input_email(self, email):
        email_field = self.get_visible_element(self.EMAIL)
        self.clear_and_send_keys(email_field, email)

    def input_password(self, password):
        password_field = self.get_visible_element(self.PASSWORD)
        self.clear_and_send_keys(password_field, password)

    def submit_login(self):
        self.get_visible_element(self.SUBMIT_BUTTON).click()

    def assert_admin_panel_visible(self):
        self.assert_element_visible(self.EMPLOYEE_ICON, timeout=30)

    def login_to_admin_panel(self):
        email, password = settings.get_admin_creds()

        self.input_email(email)
        self.input_password(password)
        self.submit_login()

        self.assert_admin_panel_visible()

    def open_products_page(self):
        self.expand_catalog_menu()
        self.open_admin_products_page()

    def logout(self):
        self.get_visible_element(self.EMPLOYEE_ICON).click()
        self.get_visible_element(self.SIGN_OUT).click()

    def expand_catalog_menu(self):
        self.get_visible_element(self.CATALOG_MENU).click()

    def open_admin_products_page(self):
        self.get_visible_element(self.PRODUCTS_SUBMENU).click()

    def switch_to_product_modal(self):
        self.assert_element_visible(self.MODAL_FRAME)

        iframe = self.get_visible_element(self.IFRAME)
        self.browser.switch_to.frame(iframe)

    def get_all_product_id_values(self):
        id_values_list = self.get_all_element_values(self.ALL_PRODUCT_IDS)
        return id_values_list

    def add_new_product(self):
        self.get_visible_element(self.ADD_NEW_PRODUCT_BTN).click()

        self.switch_to_product_modal()
        add_button = self.get_present_element(self.ADD_PRODUCT_MODAL_BTN)
        add_button.click()
        self.browser.switch_to.default_content()

        product_name = self.get_visible_element(self.PRODUCT_NAME)
        self.clear_and_send_keys(product_name, self.TEST_PRODUCT_NAME)

        self.get_visible_element(self.PRICING).click()
        rt_price = self.get_visible_element(self.RETAIL_PRICE)
        retail_price_value = get_random_price()
        self.clear_and_send_keys(rt_price, retail_price_value)

        product_name.click()
        result_rt_price = self.get_visible_element(self.RESULT_RETAIL_PRICE)
        result_rt_price_value = result_rt_price.get_attribute('value')
        assert retail_price_value == round(float(result_rt_price_value), 2), \
            f"{retail_price_value} != {result_rt_price_value}"

        cost_price = self.get_visible_element(self.COST_PRICE)
        cost_price_value = retail_price_value - get_random_price(max_price=10)
        self.clear_and_send_keys(cost_price, cost_price_value)

        self.get_visible_element(self.SAVE_BUTTON).click()

        self.assert_element_visible(self.SUCCESSFUL_ALERT)

    def delete_product(self):
        id_list_values = self.get_all_product_id_values()

        self.get_visible_element(self.ADDITIONAL_ACTIONS).click()
        self.get_visible_element(self.DELETE_BUTTON).click()

        self.get_visible_element(self.MODAL_DELETE_BUTTON).click()

        self.assert_element_visible(self.SUCCESSFUL_ALERT)

        new_id_list_values = self.get_all_product_id_values()

        assert id_list_values not in new_id_list_values, (f"Исходный список: {id_list_values} целиком содержится"
                                                          f"в новом списке: {new_id_list_values}, но не должен")
