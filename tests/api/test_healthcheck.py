import allure
import pytest
import logging

pytestmark = pytest.mark.api


@allure.epic("API тесты")
@allure.feature("Healthcheck")
class TestPing:
    logger = logging.getLogger(__name__)

    @allure.story("Ping")
    @allure.title("Проверка готовности API")
    def test_ping(self, api_client):
        self.logger.info("Проверка доступности API (ping)")

        response = api_client.session.get(f"{api_client.base_url}/ping")

        assert response.status_code == 201, f"Ожидался 201, но получен {response.status_code}"

        self.logger.info("API доступно")
