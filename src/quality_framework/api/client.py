"""Domain-focused wrapper over Playwright's APIRequestContext."""

from collections.abc import Mapping
from datetime import date
from typing import Any

from playwright.sync_api import APIRequestContext, APIResponse

from quality_framework.api.models import AuthToken, Booking


def expect_status(response: APIResponse, expected: int) -> APIResponse:
    """Assert a response status while preserving useful failure diagnostics."""

    assert response.status == expected, (
        f"Expected HTTP {expected}, got {response.status} for {response.url}. "
        f"Response body: {response.text()[:1_000]}"
    )
    return response


class RestfulBookerApi:
    """Small API client that owns routes/auth, while tests own assertions."""

    def __init__(self, request: APIRequestContext, token: str | None = None) -> None:
        self._request = request
        self._token = token

    @property
    def is_authenticated(self) -> bool:
        return self._token is not None

    def with_token(self, token: str) -> "RestfulBookerApi":
        return RestfulBookerApi(self._request, token=token)

    def authenticate(self, username: str, password: str) -> "RestfulBookerApi":
        response = self.login(username, password)
        expect_status(response, 200)
        token = AuthToken.model_validate(response.json()).token
        return self.with_token(token)

    def login(self, username: str, password: str) -> APIResponse:
        return self._request.post(
            "/api/auth/login",
            data={"username": username, "password": password},
        )

    def get_rooms(self, checkin: date | None = None, checkout: date | None = None) -> APIResponse:
        params: dict[str, str | float | bool] = {}
        if checkin is not None:
            params["checkin"] = checkin.isoformat()
        if checkout is not None:
            params["checkout"] = checkout.isoformat()
        return self._request.get("/api/room", params=params or None)

    def get_room(self, room_id: int) -> APIResponse:
        return self._request.get(f"/api/room/{room_id}")

    def get_bookings(self, room_id: int) -> APIResponse:
        return self._request.get(
            "/api/booking",
            params={"roomid": str(room_id)},
            headers=self._auth_headers(),
        )

    def get_booking(self, booking_id: int) -> APIResponse:
        return self._request.get(
            f"/api/booking/{booking_id}",
            headers=self._auth_headers(),
        )

    def create_booking(self, booking: Booking | Mapping[str, Any]) -> APIResponse:
        return self._request.post("/api/booking", data=self._payload(booking))

    def update_booking(
        self,
        booking_id: int,
        booking: Booking | Mapping[str, Any],
    ) -> APIResponse:
        return self._request.put(
            f"/api/booking/{booking_id}",
            data=self._payload(booking),
            headers=self._auth_headers(),
        )

    def delete_booking(self, booking_id: int) -> APIResponse:
        return self._request.delete(
            f"/api/booking/{booking_id}",
            headers=self._auth_headers(),
        )

    def _auth_headers(self) -> dict[str, str]:
        return {"Cookie": f"token={self._token}"} if self._token else {}

    @staticmethod
    def _payload(booking: Booking | Mapping[str, Any]) -> dict[str, Any]:
        if isinstance(booking, Booking):
            return booking.model_dump(by_alias=True, mode="json", exclude_none=True)
        return dict(booking)
