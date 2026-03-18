import allure
import pytest
from api_core.client import ApiContext, BookerClient
from utils import get_random_string
import logging
from datetime import datetime
from logger_config import setup_logging


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed and "api_context" in item.funcargs:
        context: ApiContext = item.funcargs["api_context"]
        context.attach()


@pytest.fixture()
def api_context() -> ApiContext:
    return ApiContext()


@pytest.fixture()
def api_client(request: pytest.FixtureRequest, api_context: ApiContext) -> BookerClient:
    client = BookerClient(
        base_url=request.config.getoption("--api-url"),
        context=api_context,
    )
    yield client
    client.close()


@pytest.fixture(scope="session")
def auth_token(request: pytest.FixtureRequest) -> str:
    context = ApiContext()
    client = BookerClient(base_url=request.config.getoption("--api-url"), context=context)

    try:
        response = client.create_token(username="admin", password="password123")
        assert response.status_code == 200, response.text

        token = response.json().get("token")
        assert token, response.text

        allure.attach(
            token,
            name="auth_token",
            attachment_type=allure.attachment_type.TEXT,
        )
        return token
    finally:
        client.close()


@pytest.fixture()
@allure.step("Подготовка тестового payload для booking")
def booking_payload() -> dict:
    return {
        "firstname": get_random_string(6),
        "lastname": get_random_string(8),
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-04-01",
            "checkout": "2026-04-10",
        },
        "additionalneeds": "Breakfast"
    }


@pytest.fixture()
def create_booking(api_client: BookerClient, auth_token: str, booking_payload: dict) -> dict:
    logger = logging.getLogger("fixtures")
    with allure.step("Создание тестового бронирования"):
        logger.info("Создание бронирования с payload: %s", booking_payload)
        response = api_client.add_booking(booking_payload)
        assert response.status_code == 200, response.text

        body = response.json()
        booking_id = body["bookingid"]

        logger.info("Создано бронирование с id: %s", booking_id)

        yield {"bookingid": booking_id, "booking": body["booking"]}

    if booking_id:
        with allure.step("Удаление тестового бронирования"):
            logger.info("Удаление бронирования id: %s", booking_id)
            api_client.delete_booking(booking_id=booking_id, token=auth_token)


@pytest.fixture()
@allure.step("Подготовка payload без additionalneeds")
def booking_without_additionalneeds(booking_payload: dict) -> dict:
    payload = {**booking_payload}
    payload.pop("additionalneeds")
    return payload
