from selenium.webdriver.common.by import By
from .base_page import BasePage


class AdminPage(BasePage):
    EMAIL = (By.XPATH, '//input[@id="email"]')
    PASSWORD = (By.XPATH, '//input[@id="passwd"]')
    SUBMIT_BUTTON = (By.XPATH, '//button[@id="submit_login"]')
    FORGOTTEN_PASSWORD = (By.XPATH, '//a[@id="forgot-password-link"]')
    STAY_LOGGED_IN = (By.XPATH, '//input[@id="stay_logged_in"]/..')

    EMPLOYEE_ICON = (By.XPATH, '//*[@id="employee_infos"]')
    SIGN_OUT = (By.XPATH, '//*[@id="header_logout"]')

    def login_form_is_visible(self):
        self.assert_element_visible(self.EMAIL)
        self.assert_element_visible(self.PASSWORD)
        self.assert_element_visible(self.SUBMIT_BUTTON)
        self.assert_element_visible(self.FORGOTTEN_PASSWORD)
        self.assert_element_visible(self.STAY_LOGGED_IN)

    def input_email(self, email):
        email_field = self.assert_element_visible(self.EMAIL)
        email_field.clear()
        email_field.send_keys(email)

    def input_password(self, password):
        password_field = self.assert_element_visible(self.PASSWORD)
        password_field.clear()
        password_field.send_keys(password)

    def submit_login(self):
        self.assert_element_visible(self.SUBMIT_BUTTON).click()

    def admin_panel_is_visible(self):
        self.timeout = 30
        self.assert_element_visible(self.EMPLOYEE_ICON)

    def logout(self):
        self.assert_element_visible(self.EMPLOYEE_ICON).click()
        self.assert_element_visible(self.SIGN_OUT).click()
