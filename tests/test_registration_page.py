import allure


@allure.epic("Регистрация пользователя")
@allure.feature("Страница регистрации")
class TestRegistrationPage:
    @allure.story("Проверка доступности страницы")
    @allure.title("Тест доступности страницы регистрации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_registration_page_availability(self, registration_page):
        allure.dynamic.description("Проверка видимости всех элементов формы регистрации")

        registration_page.assert_page_elements_is_visible()

    @allure.story("Создание пользователя")
    @allure.title("Тест регистрации нового пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_new_user(self, registration_page):
        allure.dynamic.description("Регистрация нового пользователя со случайными данными")

        registration_page.register_new_account()
