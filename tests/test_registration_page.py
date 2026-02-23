from pages.registration_page import RegistrationPage
from utils import open_page
import pytest


class TestRegistrationPage:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        self.registration_page = RegistrationPage(browser)
        open_page(self.registration_page, browser.base_url + "/registration")

    def test_check_registration_page_availability(self):
        self.registration_page.check_page_elements()

    def test_create_new_user(self):
        self.registration_page.register_new_account()
