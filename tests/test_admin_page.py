from pages.admin_page import AdminPage
import pytest
from config import settings
from utils import open_page


class TestAdminPage:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        self.admin_page = AdminPage(browser)
        open_page(self.admin_page, browser.base_url + "/administration")

    @pytest.fixture(scope="function")
    def login_to_admin_panel(self):
        email, password = settings.get_admin_creds()

        self.admin_page.input_email(email)
        self.admin_page.input_password(password)
        self.admin_page.submit_login()

        self.admin_page.set_timeout(30)
        self.admin_page.admin_panel_is_visible()

        self.admin_page.set_timeout(5)

    @pytest.fixture(scope="function")
    def open_products_page(self):
        self.admin_page.expand_catalog_menu()
        self.admin_page.open_admin_products_page()

    def test_check_admin_page_availability(self):
        self.admin_page.login_form_is_visible()

    def test_login_to_admin_page(self, login_to_admin_panel):
        self.admin_page.logout()
        self.admin_page.login_form_is_visible()

    def test_create_new_product_in_admin_panel(self, login_to_admin_panel, open_products_page):
        self.admin_page.add_new_product()

    def test_delete_product_in_admin_panel(self, login_to_admin_panel, open_products_page):
        self.admin_page.delete_product()
