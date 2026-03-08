from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils import get_random_email, get_random_string, get_random_date
import allure


class RegistrationPage(BasePage):
    SOCIAL_TITLE = (By.XPATH, '//*[@class="radio-inline"]')
    FIRST_NAME = (By.XPATH, '//input[@id="field-firstname"]')
    LAST_NAME = (By.XPATH, '//input[@id="field-lastname"]')
    EMAIL = (By.XPATH, '//input[@id="field-email"]')
    PASSWORD = (By.XPATH, '//input[@id="field-password"]')
    SHOW_PASSWORD = (By.XPATH, '//button[@data-action="show-password"]')
    BIRTHDATE = (By.XPATH, '//input[@id="field-birthday"]')
    REQUIRED_CHECKBOXES = (By.XPATH, '//*[@class="custom-checkbox"]//input[@required]')
    OPTIONAL_CHECKBOXES = (By.XPATH, '//*[@class="custom-checkbox"]//input[not(@required)]')

    SAVE_BTN = (By.XPATH, '//button[@data-link-action="save-customer"]')

    ACCOUNT_NAME = (By.XPATH, '//*[@class="account"]//*[@class="hidden-sm-down"]')

    @allure.step("Проверка видимости всех элементов страницы регистрации")
    def assert_page_elements_is_visible(self):
        self.logger.info("Проверка видимости элементов страницы регистрации")

        self.assert_element_visible(self.FIRST_NAME)
        self.assert_element_visible(self.LAST_NAME)
        self.assert_element_visible(self.EMAIL)
        self.assert_element_visible(self.PASSWORD)
        self.assert_element_visible(self.SHOW_PASSWORD)
        self.assert_element_visible(self.BIRTHDATE)
        self.assert_element_visible(self.SAVE_BTN)

        self.logger.info("Все элементы страницы регистрации видимы")

    @allure.step("Выбор пола")
    def choose_gender(self):
        self.logger.info("Выбор пола")

        genders = self.find_all_elements(self.SOCIAL_TITLE)
        self.click_on_random_element(genders)

    @allure.step("Ввод имени и фамилии")
    def insert_first_and_last_names(self):
        self.logger.info("Ввод имени и фамилии")

        first_name = self.get_visible_element(self.FIRST_NAME)
        self.clear_and_send_keys(first_name, get_random_string())

        last_name = self.get_visible_element(self.LAST_NAME)
        self.clear_and_send_keys(last_name, get_random_string())

    @allure.step("Ввод email")
    def insert_email(self):
        email = self.get_visible_element(self.EMAIL)
        email_text = get_random_email()

        self.logger.info(f"Ввод email: {email_text}")

        self.clear_and_send_keys(email, email_text)

    @allure.step("Ввод пароля")
    def insert_password(self):
        self.logger.info("Ввод пароля")

        password = self.get_visible_element(self.PASSWORD)
        self.clear_and_send_keys(password, get_random_string())

    @allure.step("Ввод даты рождения")
    def insert_birthdate(self):
        birthdate = self.get_visible_element(self.BIRTHDATE)
        birthdate_text = get_random_date()

        self.logger.info(f"Ввод даты рождения: {birthdate_text}")

        self.clear_and_send_keys(birthdate, birthdate_text)

    @allure.step("Выбор чекбоксов")
    def choose_checkboxes(self):
        self.logger.info("Выбор чекбоксов")

        required_checkboxes = self.find_all_elements(self.REQUIRED_CHECKBOXES)
        self.click_on_all_elements(required_checkboxes)

        optional_checkboxes = self.find_all_elements(self.OPTIONAL_CHECKBOXES)
        self.click_on_random_element(optional_checkboxes)

    @allure.step("Проверка успешности регистрации")
    def check_successful_registration(self):
        self.logger.info("Проверка успешности регистрации")
        self.assert_element_visible(self.ACCOUNT_NAME, timeout=15)
        self.logger.info("Регистрация прошла успешно")

    @allure.step("Регистрация нового аккаунта")
    def register_new_account(self):
        self.logger.info("НАЧАЛО РЕГИСТРАЦИИ НОВОГО АККАУНТА")
        self.choose_gender()
        self.insert_first_and_last_names()
        self.insert_email()
        self.insert_password()
        self.insert_birthdate()
        self.choose_checkboxes()

        self.get_visible_element(self.SAVE_BTN).click()

        self.check_successful_registration()

        self.logger.info("РЕГИСТРАЦИЯ УСПЕШНО ЗАВЕРШЕНА")
