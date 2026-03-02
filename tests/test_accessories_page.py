class TestAccessoriesPage:
    def test_check_accessories_page_availability(self, accessories_page):
        accessories_page.assert_page_elements_is_visible()

    def test_change_currency_and_check_prices(self, accessories_page):
        accessories_page.check_prices()
