from pages.admin_page import AdminPage
import pytest
from config import settings
from utils import open_page


class TestAdminPage:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        self.admin_page = AdminPage(browser)
        open_page(self.admin_page, browser.base_url + "/administration")

    def test_check_admin_page_availability(self):
        self.admin_page.login_form_is_visible()

    def test_login_to_admin_page(self):
        email, password = settings.get_admin_creds()

        self.admin_page.input_email(email)
        self.admin_page.input_password(password)
        self.admin_page.submit_login()

        self.admin_page.admin_panel_is_visible()
        self.admin_page.logout()
        self.admin_page.login_form_is_visible()
