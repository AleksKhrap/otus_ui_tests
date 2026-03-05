import allure


@allure.epic("Главная страница")
@allure.feature("Главная страница")
class TestHomePage:
    @allure.story("Проверка доступности страницы")
    @allure.title("Тест доступности главной страницы")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_home_page_availability(self, home_page):
        home_page.assert_page_elements_is_visible()

    @allure.story("Работа с корзиной")
    @allure.title("Тест добавления товара в корзину")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_product_to_cart(self, home_page):
        home_page.open_product_page()
        home_page.add_to_cart()
        home_page.check_cart()

    @allure.story("Работа с ценами")
    @allure.title("Тест изменения цен при смене валюты")
    @allure.severity(allure.severity_level.NORMAL)
    def test_change_currency_and_check_prices(self, home_page):
        home_page.check_prices()
