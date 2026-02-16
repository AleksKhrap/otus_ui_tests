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
        self.browser.find_element(*self.FIRST_NAME)
        self.browser.find_element(*self.LAST_NAME)
        self.browser.find_element(*self.EMAIL)
        self.browser.find_element(*self.PASSWORD)
        self.browser.find_element(*self.SHOW_PASSWORD)
        self.browser.find_element(*self.BIRTHDATE)
        self.browser.find_element(*self.SAVE_BTN)
