import allure
import pytest
import logging
from config import settings

pytestmark = pytest.mark.api


@allure.epic("API тесты")
@allure.feature("Аутентификация")
class TestAuth:
    logger = logging.getLogger(__name__)

    @allure.story("Создание токена")
    @allure.title("Успешное получение auth_token")
    def test_create_token_success(self, api_client):
        self.logger.info("ТЕСТ: Успешное получение auth_token")

        username, password = settings.API_USER, settings.API_PASSWORD
        self.logger.info("Запрос токена с credentials: admin/***")

        response = api_client.create_token(username=username, password=password)

        assert response.status_code == 200

        body = response.json()
        self.logger.info("Токен получен: %s", body.get("token", "не найден"))

        assert "token" in body

        assert isinstance(body["token"], str)
        assert len(body["token"]) > 0

        self.logger.info("Токен валиден")

    @allure.story("Создание токена")
    @allure.title("Ошибка авторизации для некорректных credentials: {username}/{password}")
    @pytest.mark.parametrize(
        "username,password",
        [
            ("admin", "wrong_password"),
            ("wrong_user", "password123"),
            ("wrong_user", "wrong_password"),
        ],
    )
    def test_create_token_with_invalid_credentials(self, api_client, username, password):
        self.logger.info("Ошибка авторизации для %s/%s", username, password)

        response = api_client.create_token(username=username, password=password)

        assert response.status_code == 200
        body = response.json()

        assert "token" not in body
        assert body.get("reason") == "Bad credentials"

    @allure.story("Создание токена")
    @allure.title("Ошибка авторизации при пустом поле {field_name}")
    @pytest.mark.parametrize(
        "field_name,payload",
        [
            ("username", {"username": "", "password": "password123"}),
            ("password", {"username": "admin", "password": ""}),
        ],
    )
    def test_create_token_with_empty_required_field(self, api_client, field_name, payload):
        self.logger.info("Ошибка авторизации при пустом поле %s", field_name)
        response = api_client._request("POST", "/auth", json=payload, headers=api_client._json_headers())

        assert response.status_code == 200

        body = response.json()
        self.logger.info("Ответ: %s", body)

        assert "token" not in body
        assert body.get("reason") == "Bad credentials"
