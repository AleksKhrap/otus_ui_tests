from pages.registration_page import RegistrationPage
import pytest


class TestRegistrationPage:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        self.registration_page = RegistrationPage(browser, browser.base_url + "/registration")
        self.registration_page.open()

    def test_check_registration_page_availability(self):
        self.registration_page.check_page_elements()
