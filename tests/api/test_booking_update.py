import allure
import pytest
import logging
import data.booking_update_data as data

pytestmark = pytest.mark.api


@allure.epic("API тесты")
@allure.feature("Обновление бронирования")
class TestBookingUpdate:
    logger = logging.getLogger(__name__)

    @allure.story("Обновление бронирования")
    @allure.title("Полное обновление бронирования")
    def test_update_booking_success(self, api_client, create_booking, auth_token):
        self.logger.info("Полное обновление бронирования")

        updated_payload = data.UPDATED_PAYLOAD

        booking_id = create_booking["bookingid"]
        self.logger.info("Обновление бронирования ID %s", booking_id)

        response = api_client.update_booking(booking_id, updated_payload, token=auth_token)

        assert response.status_code == 200
        assert response.json() == updated_payload

        self.logger.info("Бронирование обновлено")

        get_response = api_client.get_booking(create_booking["bookingid"])
        assert get_response.status_code == 200
        assert get_response.json() == updated_payload

    @allure.story("Обновление бронирования")
    @allure.title("Частичное обновление имени")
    def test_partial_update_booking_firstname(self, api_client, create_booking, auth_token):
        self.logger.info("Частичное обновление имени")

        patch_payload = data.PATCHED_NAME

        booking_id = create_booking["bookingid"]
        self.logger.info("Частичное обновление бронирования ID %s", booking_id)

        response = api_client.partial_update_booking(booking_id, patch_payload, token=auth_token)

        assert response.status_code == 200
        body = response.json()

        assert body["firstname"] == patch_payload["firstname"]
        assert body["lastname"] == create_booking["booking"]["lastname"]

    @allure.story("Обновление бронирования")
    @allure.title("Частичное обновление additionalneeds")
    def test_partial_update_booking_additionalneeds(self, api_client, create_booking, auth_token):
        self.logger.info("Частичное обновление additionalneeds")

        patch_payload = data.ADDITIONAL_DINNER

        booking_id = create_booking["bookingid"]
        self.logger.info("Частичное обновление бронирования ID %s", booking_id)

        response = api_client.partial_update_booking(booking_id, patch_payload, token=auth_token)

        assert response.status_code == 200
        body = response.json()

        assert body["additionalneeds"] == "Dinner"
        assert body["firstname"] == create_booking["booking"]["firstname"]

    @allure.story("Обновление бронирования")
    @allure.title("Полное обновление без токена запрещено")
    def test_update_booking_without_token_returns_403(self, api_client, create_booking):
        self.logger.info("Полное обновление без токена")

        response = api_client.update_booking(
            create_booking["bookingid"],
            create_booking["booking"],
            token=None
        )

        assert response.status_code == 403

    @allure.story("Обновление бронирования")
    @allure.title("Частичное обновление без токена запрещено")
    def test_partial_update_booking_without_token_returns_403(self, api_client, create_booking):
        self.logger.info("Частичное обновление без токена")

        response = api_client.partial_update_booking(
            create_booking["bookingid"],
            data.FIRSTNAME_NO_AUTH,
            token=None
        )

        assert response.status_code == 403
