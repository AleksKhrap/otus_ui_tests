class TestHomePage:
    def test_check_home_page_availability(self, home_page):
        home_page.assert_page_elements_is_visible()

    def test_add_product_to_cart(self, home_page):
        home_page.open_product_page()
        home_page.add_to_cart()
        home_page.check_cart()

    def test_change_currency_and_check_prices(self, home_page):
        home_page.check_prices()
