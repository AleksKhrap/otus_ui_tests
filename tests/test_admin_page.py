class TestAdminPage:
    def test_check_admin_page_availability(self, admin_page):
        admin_page.assert_login_form_is_visible()

    def test_login_to_admin_page(self, admin_page):
        admin_page.login_to_admin_panel()
        admin_page.logout()
        admin_page.assert_login_form_is_visible()

    def test_create_new_product_in_admin_panel(self, admin_page):
        admin_page.login_to_admin_panel()
        admin_page.open_products_page()
        admin_page.add_new_product()

    def test_delete_product_in_admin_panel(self, admin_page):
        admin_page.login_to_admin_panel()
        admin_page.open_products_page()
        admin_page.delete_product()
