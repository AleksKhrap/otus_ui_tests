class TestProductPage:
    def test_check_product_page_availability(self, product_page):
        product_page.assert_page_is_visible()
