import allure


@allure.epic("Администрирование")
@allure.feature("Админ-панель")
class TestAdminPage:
    @allure.story("Проверка доступности страницы")
    @allure.title("Тест доступности страницы логина админки")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_admin_page_availability(self, admin_page):
        admin_page.assert_login_form_is_visible()

    @allure.story("Авторизация")
    @allure.title("Тест входа и выхода из админки")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_to_admin_page(self, admin_page):
        admin_page.login_to_admin_panel()
        admin_page.logout()
        admin_page.assert_login_form_is_visible()

    @allure.story("Управление товарами")
    @allure.title("Тест создания нового товара")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_new_product_in_admin_panel(self, admin_page):
        admin_page.login_to_admin_panel()
        admin_page.open_products_page()
        admin_page.add_new_product()

    @allure.story("Управление товарами")
    @allure.title("Тест удаления товара")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_product_in_admin_panel(self, admin_page):
        admin_page.login_to_admin_panel()
        admin_page.open_products_page()
        admin_page.delete_product()
