import allure


@allure.epic("Товары")
@allure.feature("Страница товара")
class TestProductPage:
    @allure.story("Проверка доступности страницы")
    @allure.title("Тест доступности страницы товара")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_product_page_availability(self, product_page):
        product_page.assert_page_is_visible()
