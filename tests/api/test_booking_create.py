import allure
import pytest
import logging

pytestmark = pytest.mark.api


@allure.epic("API тесты")
@allure.feature("Создание бронирования")
class TestBookingCreate:
    logger = logging.getLogger(__name__)

    @allure.story("Создание бронирования")
    @allure.title("Создание нового бронирования")
    def test_create_booking_success(self, api_client, booking_payload, auth_token):
        self.logger.info("Создание нового бронирования")

        response = api_client.add_booking(booking_payload)

        assert response.status_code == 200

        body = response.json()
        self.logger.info("Бронирование создано с ID: %s", body["bookingid"])

        assert isinstance(body["bookingid"], int)
        assert body["booking"] == booking_payload

        api_client.delete_booking(body["bookingid"], token=auth_token)

    @allure.story("Создание бронирования")
    @allure.title("Создание бронирования без additionalneeds")
    def test_create_booking_without_additionalneeds(self, api_client, booking_without_additionalneeds, auth_token):
        self.logger.info("Создание бронирования без additionalneeds")
        response = api_client.add_booking(booking_without_additionalneeds)

        assert response.status_code == 200

        body = response.json()
        self.logger.info("Бронирование создано с ID: %s", body["bookingid"])

        assert body["booking"]["firstname"] == booking_without_additionalneeds["firstname"]
        assert "additionalneeds" not in body["booking"]

        api_client.delete_booking(body["bookingid"], token=auth_token)

    @allure.story("Создание бронирования")
    @allure.title("Создание бронирования с depositpaid={depositpaid}")
    @pytest.mark.parametrize("depositpaid", [True, False])
    def test_create_booking_with_different_deposit_flags(self, api_client, booking_payload, auth_token, depositpaid):
        self.logger.info("Создание бронирования с depositpaid=%s", depositpaid)
        payload = {**booking_payload, "depositpaid": depositpaid}

        response = api_client.add_booking(payload)

        assert response.status_code == 200

        body = response.json()
        self.logger.info("Бронирование создано с ID: %s", body["bookingid"])

        assert body["booking"]["depositpaid"] is depositpaid

        api_client.delete_booking(body["bookingid"], token=auth_token)
