import pytest

from quality_framework.api import RestfulBookerApi, expect_status
from quality_framework.api.models import Bookings, ErrorResponse, Rooms
from quality_framework.config import Settings

pytestmark = pytest.mark.api


def test_invalid_credentials_are_rejected(api_client: RestfulBookerApi) -> None:
    response = expect_status(api_client.login("not-a-user", "not-a-password"), 401)

    error = ErrorResponse.model_validate(response.json())
    assert error.error == "Invalid credentials"


def test_protected_booking_route_requires_authentication(api_client: RestfulBookerApi) -> None:
    rooms = Rooms.model_validate(expect_status(api_client.get_rooms(), 200).json()).rooms

    response = expect_status(api_client.get_bookings(rooms[0].room_id), 401)

    assert ErrorResponse.model_validate(response.json()).error == "Authentication required"


def test_booking_detail_requires_authentication(api_client: RestfulBookerApi) -> None:
    response = api_client.get_booking(2_147_483_647)

    expect_status(response, 403)


@pytest.mark.smoke
def test_admin_can_read_bookings(
    api_client: RestfulBookerApi,
    settings: Settings,
) -> None:
    rooms = Rooms.model_validate(expect_status(api_client.get_rooms(), 200).json()).rooms
    authenticated = api_client.authenticate(settings.admin_username, settings.admin_password)

    response = expect_status(authenticated.get_bookings(rooms[0].room_id), 200)

    Bookings.model_validate(response.json())
