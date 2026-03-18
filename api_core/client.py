import json
import allure
import requests
from typing import Any
import logging


class ApiContext:
    """Хранит последнюю пару request/response для Allure при падении."""

    def __init__(self) -> None:
        self.last_request: dict[str, Any] = {}
        self.last_response: dict[str, Any] = {}

    def remember(self, method: str, url: str, **kwargs: Any) -> None:
        headers = kwargs.get("headers") or {}
        json_body = kwargs.get("json")
        params = kwargs.get("params")

        self.last_request = {
            "method": method,
            "url": url,
            "headers": headers,
            "params": params,
            "json": json_body,
        }

    def remember_response(self, response: requests.Response) -> None:
        try:
            body: Any = response.json()
        except ValueError:
            body = response.text

        self.last_response = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": body,
        }

    def attach(self) -> None:
        if self.last_request:
            allure.attach(
                json.dumps(self.last_request, ensure_ascii=False, indent=2),
                name="last_request",
                attachment_type=allure.attachment_type.JSON,
            )
        if self.last_response:
            allure.attach(
                json.dumps(self.last_response, ensure_ascii=False, indent=2),
                name="last_response",
                attachment_type=allure.attachment_type.JSON,
            )


class BookerClient:
    def __init__(self, base_url: str, context: ApiContext) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.context = context

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Инициализация клиента. base_url=%s", self.base_url)

    def close(self) -> None:
        self.session.close()

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = f"{self.base_url}{path}"
        self.context.remember(method=method, url=url, **kwargs)

        self.logger.info("Отправка запроса: %s %s", method, url)

        with allure.step(f"{method} {path}"):
            response = self.session.request(method=method, url=url, timeout=15, **kwargs)
            self.context.remember_response(response)
            self._attach_exchange(method, url, kwargs, response)

            self.logger.info("Статус ответа: %s", response.status_code)
            return response

    @staticmethod
    def _attach_exchange(method: str, url: str, request_kwargs: dict[str, Any], response: requests.Response) -> None:
        req_payload = {
            "method": method,
            "url": url,
            "params": request_kwargs.get("params"),
            "json": request_kwargs.get("json"),
            "headers": request_kwargs.get("headers"),
        }
        allure.attach(
            json.dumps(req_payload, ensure_ascii=False, indent=2),
            name=f"request_{method}_{response.request.path_url.replace('/', '_')}",
            attachment_type=allure.attachment_type.JSON,
        )

        try:
            response_body: Any = response.json()
        except ValueError:
            response_body = response.text

        resp_payload = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response_body,
        }
        allure.attach(
            json.dumps(resp_payload, ensure_ascii=False, indent=2),
            name=f"response_{response.status_code}",
            attachment_type=allure.attachment_type.JSON,
        )

    @staticmethod
    def _json_headers(token: str | None = None) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if token:
            headers["Cookie"] = f"token={token}"
        return headers

    def create_token(self, username: str, password: str) -> requests.Response:
        return self._request(
            "POST",
            "/auth",
            json={"username": username, "password": password},
            headers=self._json_headers(),
        )

    def get_booking_ids(self, **params: Any) -> requests.Response:
        filtered = {key: value for key, value in params.items() if value is not None}
        return self._request("GET", "/booking", params=filtered)

    def get_booking(self, booking_id: int | str) -> requests.Response:
        return self._request("GET", f"/booking/{booking_id}")

    def add_booking(self, payload: dict[str, Any]) -> requests.Response:
        return self._request("POST", "/booking", json=payload, headers=self._json_headers())

    def update_booking(self, booking_id: int, payload: dict[str, Any], token: str | None = None) -> requests.Response:
        headers = self._json_headers()
        if token:
            headers["Cookie"] = f"token={token}"
        return self._request("PUT", f"/booking/{booking_id}", json=payload, headers=headers)

    def partial_update_booking(self,
                               booking_id: int,
                               payload: dict[str, Any],
                               token: str | None = None,
                               ) -> requests.Response:
        headers = self._json_headers()
        if token:
            headers["Cookie"] = f"token={token}"
        return self._request("PATCH", f"/booking/{booking_id}", json=payload, headers=headers)

    def delete_booking(self, booking_id: int, token: str | None = None) -> requests.Response:
        self.logger.info("Очистка: удаление бронирования ID %s", booking_id)
        headers: dict[str, str] = {}
        if token:
            headers["Cookie"] = f"token={token}"
        return self._request("DELETE", f"/booking/{booking_id}", headers=headers)
