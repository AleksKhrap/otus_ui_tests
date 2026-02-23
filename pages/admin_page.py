from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils import clear_and_send_keys, get_random_price


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

    def login_form_is_visible(self):
        self.assert_element_visible(self.EMAIL)
        self.assert_element_visible(self.PASSWORD)
        self.assert_element_visible(self.SUBMIT_BUTTON)
        self.assert_element_visible(self.FORGOTTEN_PASSWORD)
        self.assert_element_visible(self.STAY_LOGGED_IN)

    def input_email(self, email):
        email_field = self.assert_element_visible(self.EMAIL)
        clear_and_send_keys(email_field, email)

    def input_password(self, password):
        password_field = self.assert_element_visible(self.PASSWORD)
        clear_and_send_keys(password_field, password)

    def submit_login(self):
        self.assert_element_visible(self.SUBMIT_BUTTON).click()

    def admin_panel_is_visible(self):
        self.assert_element_visible(self.EMPLOYEE_ICON)

    def logout(self):
        self.assert_element_visible(self.EMPLOYEE_ICON).click()
        self.assert_element_visible(self.SIGN_OUT).click()

    def expand_catalog_menu(self):
        self.assert_element_visible(self.CATALOG_MENU).click()

    def open_admin_products_page(self):
        self.assert_element_visible(self.PRODUCTS_SUBMENU).click()

    def switch_to_product_modal(self):
        self.assert_element_visible(self.MODAL_FRAME)

        iframe = self.assert_element_visible(self.IFRAME)
        self.browser.switch_to.frame(iframe)

    def get_all_product_id_values(self):
        id_values_list = self.get_all_element_values(self.ALL_PRODUCT_IDS)
        return id_values_list

    def add_new_product(self):
        self.assert_element_visible(self.ADD_NEW_PRODUCT_BTN).click()

        self.switch_to_product_modal()
        add_button = self.assert_element_present(self.ADD_PRODUCT_MODAL_BTN)
        add_button.click()
        self.browser.switch_to.default_content()

        product_name = self.assert_element_visible(self.PRODUCT_NAME)
        clear_and_send_keys(product_name, self.TEST_PRODUCT_NAME)

        self.assert_element_visible(self.PRICING).click()
        rt_price = self.assert_element_visible(self.RETAIL_PRICE)
        retail_price_value = get_random_price()
        clear_and_send_keys(rt_price, retail_price_value)

        product_name.click()
        result_rt_price = self.assert_element_visible(self.RESULT_RETAIL_PRICE)
        result_rt_price_value = result_rt_price.get_attribute('value')
        assert retail_price_value == round(float(result_rt_price_value), 2), \
            f"{retail_price_value} != {result_rt_price_value}"

        cost_price = self.assert_element_visible(self.COST_PRICE)
        cost_price_value = retail_price_value - get_random_price(max_price=10)
        clear_and_send_keys(cost_price, cost_price_value)

        self.assert_element_visible(self.SAVE_BUTTON).click()
        self.assert_element_visible(self.SUCCESSFUL_ALERT)

    def delete_product(self):
        id_list_values = self.get_all_product_id_values()

        self.assert_element_visible(self.ADDITIONAL_ACTIONS).click()
        self.assert_element_visible(self.DELETE_BUTTON).click()

        self.assert_element_visible(self.MODAL_DELETE_BUTTON).click()

        self.assert_element_visible(self.SUCCESSFUL_ALERT)

        new_id_list_values = self.get_all_product_id_values()

        assert id_list_values not in new_id_list_values, (f"Исходный список: {id_list_values} целиком содержится"
                                                          f"в новом списке: {new_id_list_values}, но не должен")
