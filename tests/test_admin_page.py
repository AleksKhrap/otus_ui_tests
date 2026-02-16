from pages.admin_page import AdminPage
import pytest


class TestAdminPage:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        self.admin_page = AdminPage(browser, browser.base_url + "/administration")
        self.admin_page.open()

    def test_check_admin_page_availability(self):
        self.admin_page.login_form_is_visible()

    def test_login_to_admin_page(self):
        email = "admin@example.com"
        password = "Admin123!"

        self.admin_page.input_email(email)
        self.admin_page.input_password(password)
        self.admin_page.submit_login()

        self.admin_page.admin_panel_is_visible()
        self.admin_page.logout()
        self.admin_page.login_form_is_visible()
