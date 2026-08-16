from unittest.mock import Mock

import pytest

from quality_framework.api.client import RestfulBookerApi, expect_status
from quality_framework.api.models import Booking
from quality_framework.data import BookingFactory

pytestmark = pytest.mark.unit


def test_authenticate_returns_client_with_cookie_header() -> None:
    request = Mock()
    request.post.return_value = _response(200, {"token": "abc123"})

    client = RestfulBookerApi(request).authenticate("admin", "password")
    client.get_bookings(1)

    request.get.assert_called_once_with(
        "/api/booking",
        params={"roomid": "1"},
        headers={"Cookie": "token=abc123"},
    )


def test_booking_model_is_serialized_with_api_aliases() -> None:
    request = Mock()
    request.post.return_value = _response(201, {})
    booking: Booking = BookingFactory().build()

    RestfulBookerApi(request).create_booking(booking)

    payload = request.post.call_args.kwargs["data"]
    assert payload["roomid"] == booking.room_id
    assert payload["depositpaid"] is False
    assert payload["bookingdates"]["checkin"] == booking.booking_dates.checkin.isoformat()


def test_status_assertion_includes_response_diagnostics() -> None:
    response = _response(500, {"error": "broken"})

    with pytest.raises(AssertionError, match=r"HTTP 200.*broken"):
        expect_status(response, 200)


def _response(status: int, payload: object) -> Mock:
    response = Mock()
    response.status = status
    response.url = "https://example.test/api"
    response.json.return_value = payload
    response.text.return_value = str(payload)
    return response
