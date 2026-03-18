import allure
import pytest
import logging

pytestmark = pytest.mark.api


@allure.epic("API тесты")
@allure.feature("Удаление бронирования")
class TestBookingCreate:
    logger = logging.getLogger(__name__)

    @allure.story("Удаление бронирования")
    @allure.title("Удаление бронирования с токеном")
    def test_delete_booking_success(self, api_client, booking_payload, auth_token):
        self.logger.info("Удаление бронирования с токеном")

        create_response = api_client.add_booking(booking_payload)
        booking_id = create_response.json()["bookingid"]

        delete_response = api_client.delete_booking(booking_id, token=auth_token)
        assert delete_response.status_code == 201

        get_response = api_client.get_booking(booking_id)
        assert get_response.status_code == 404

    @allure.story("Удаление бронирования")
    @allure.title("Удаление без токена запрещено")
    def test_delete_booking_without_token_returns_403(self, api_client, create_booking):
        self.logger.info("Удаление без токена")

        response = api_client.delete_booking(create_booking["bookingid"], token=None)

        assert response.status_code == 403
