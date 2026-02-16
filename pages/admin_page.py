from selenium.webdriver.common.by import By
from .base_page import BasePage

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AdminPage(BasePage):
    EMAIL = (By.XPATH, '//input[@id="email"]')
    PASSWORD = (By.XPATH, '//input[@id="passwd"]')
    SUBMIT_BUTTON = (By.XPATH, '//button[@id="submit_login"]')
    FORGOTTEN_PASSWORD = (By.XPATH, '//a[@id="forgot-password-link"]')
    STAY_LOGGED_IN = (By.XPATH, '//input[@id="stay_logged_in"]')

    EMPLOYEE_ICON = (By.XPATH, '//*[@id="employee_infos"]')
    SIGN_OUT = (By.XPATH, '//*[@id="header_logout"]')

    def login_form_is_visible(self):
        self.browser.find_element(*self.EMAIL)
        self.browser.find_element(*self.PASSWORD)
        self.browser.find_element(*self.SUBMIT_BUTTON)
        self.browser.find_element(*self.FORGOTTEN_PASSWORD)
        self.browser.find_element(*self.STAY_LOGGED_IN)

    def input_email(self, email):
        email_field = self.browser.find_element(*self.EMAIL)
        email_field.clear()
        email_field.send_keys(email)

    def input_password(self, password):
        password_field = self.browser.find_element(*self.PASSWORD)
        password_field.clear()
        password_field.send_keys(password)

    def submit_login(self):
        self.browser.find_element(*self.SUBMIT_BUTTON).click()

    def admin_panel_is_visible(self):
        WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located(self.EMPLOYEE_ICON))

    def logout(self):
        self.browser.find_element(*self.EMPLOYEE_ICON).click()
        self.browser.find_element(*self.SIGN_OUT).click()
