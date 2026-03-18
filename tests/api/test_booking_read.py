import allure
import pytest
import logging
from config import settings

pytestmark = pytest.mark.api


@allure.epic("API тесты")
@allure.feature("Просмотр бронирований")
class TestBookingRead:
    logger = logging.getLogger(__name__)

    @allure.story("Получение бронирований")
    @allure.title("Получение списка ID бронирований")
    def test_get_booking_ids_returns_non_empty_list(self, api_client):
        self.logger.info("Получение списка всех ID бронирований")

        response = api_client.get_booking_ids()
        assert response.status_code == 200

        body = response.json()
        self.logger.info("Получено %s бронирований", len(body))

        assert isinstance(body, list)
        assert body, "Ожидался непустой список бронирований"
        assert "bookingid" in body[0]

    @allure.story("Фильтрация бронирований")
    @allure.title("Фильтрация бронирований по параметру {filter_name}")
    @pytest.mark.parametrize("filter_name", ["firstname", "lastname", "firstname+lastname"])
    def test_get_booking_ids_with_name_filters(self, api_client, create_booking, filter_name):
        self.logger.info("Фильтрация бронирований по %s", filter_name)

        booking = create_booking["booking"]

        if filter_name == "firstname":
            params = {"firstname": booking["firstname"]}
        elif filter_name == "lastname":
            params = {"lastname": booking["lastname"]}
        else:
            params = {
                "firstname": booking["firstname"],
                "lastname": booking["lastname"],
            }

        self.logger.info("Параметры фильтра: %s", params)

        with allure.step(f"Отправка запроса с фильтром {filter_name}: {params}"):
            response = api_client.get_booking_ids(**params)

        with allure.step("Проверка результата"):
            assert response.status_code == 200

            body = response.json()
            self.logger.info("Найдено бронирований: %s", len(body))

            booking_ids = [item["bookingid"] for item in body]
            self.logger.info("Найденные ID: %s", booking_ids)

            assert create_booking["bookingid"] in booking_ids, (
                f"ID бронирования не найден по фильтру {filter_name}"
            )

    @allure.story("Фильтрация бронирований")
    @allure.title("Фильтрация бронирований по checkin и checkout")
    def test_get_booking_ids_with_date_filters(self, api_client, create_booking):
        self.logger.info("Фильтрация бронирований по датам")

        dates = create_booking["booking"]["bookingdates"]
        self.logger.info("Даты бронирования: checkin=%s, checkout=%s", dates["checkin"], dates["checkout"])

        response = api_client.get_booking_ids(
            checkin=dates["checkin"],
            checkout=dates["checkout"]
        )

        assert response.status_code == 200

        body = response.json()
        assert isinstance(body, list)

        for item in body:
            assert "bookingid" in item
            assert isinstance(item["bookingid"], int)

    @allure.story("Получение бронирования")
    @allure.title("Получение существующего бронирования по ID")
    def test_get_existing_booking_by_id(self, api_client, create_booking):
        self.logger.info("Получение существующего бронирования по ID")

        booking_id = create_booking["bookingid"]
        self.logger.info("Запрос бронирования ID %s", booking_id)

        response = api_client.get_booking(booking_id)

        assert response.status_code == 200

        body = response.json()
        self.logger.info("Получено бронирование: firstname=%s, lastname=%s", body["firstname"], body["lastname"])

        assert body["firstname"] == create_booking["booking"]["firstname"]
        assert body["lastname"] == create_booking["booking"]["lastname"]
        assert body["bookingdates"] == create_booking["booking"]["bookingdates"]

        self.logger.info("Данные бронирования совпадают с ожидаемыми")

    @allure.story("Получение бронирования")
    @allure.title("Получение несуществующего бронирования 404")
    def test_get_non_existing_booking_returns_404(self, api_client):
        self.logger.info("Получение несуществующего бронирования")

        response = api_client.get_booking(settings.FAILURE_ID)

        assert response.status_code == 404
