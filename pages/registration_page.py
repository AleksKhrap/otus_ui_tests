from selenium.webdriver.common.by import By
from .base_page import BasePage


class RegistrationPage(BasePage):
    FIRST_NAME = (By.XPATH, '//input[@id="field-firstname"]')
    LAST_NAME = (By.XPATH, '//input[@id="field-lastname"]')
    EMAIL = (By.XPATH, '//input[@id="field-email"]')
    PASSWORD = (By.XPATH, '//input[@id="field-email"]')
    SHOW_PASSWORD = (By.XPATH, '//button[@data-action="show-password"]')
    BIRTHDATE = (By.XPATH, '//input[@id="field-birthday"]')
    SAVE_BTN = (By.XPATH, '//button[@data-link-action="save-customer"]')

    def check_page_elements(self):
        self.assert_element_visible(self.FIRST_NAME)
        self.assert_element_visible(self.LAST_NAME)
        self.assert_element_visible(self.EMAIL)
        self.assert_element_visible(self.PASSWORD)
        self.assert_element_visible(self.SHOW_PASSWORD)
        self.assert_element_visible(self.BIRTHDATE)
        self.assert_element_visible(self.SAVE_BTN)
