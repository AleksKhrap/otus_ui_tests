import allure


@allure.epic("Аксессуары")
@allure.feature("Страница аксессуаров")
class TestAccessoriesPage:
    @allure.story("Проверка доступности страницы")
    @allure.title("Тест доступности страницы аксессуаров")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_accessories_page_availability(self, accessories_page):
        accessories_page.assert_page_elements_is_visible()

    @allure.story("Работа с ценами")
    @allure.title("Тест изменения цен при смене валюты")
    @allure.severity(allure.severity_level.NORMAL)
    def test_change_currency_and_check_prices(self, accessories_page):
        accessories_page.check_prices()
