from datetime import date

import pytest
from playwright.sync_api import Page

from quality_framework.api import RestfulBookerApi, expect_status
from quality_framework.api.models import Rooms
from quality_framework.config import Settings
from quality_framework.ui import ReservationPage

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_guest_sees_itemized_price_before_reserving(
    page: Page,
    settings: Settings,
    api_client: RestfulBookerApi,
    future_stay: tuple[date, date],
) -> None:
    rooms = Rooms.model_validate(
        expect_status(api_client.get_rooms(*future_stay), 200).json()
    ).rooms
    assert rooms, "No room is available for the isolated test window"
    room = rooms[0]
    reservation = ReservationPage(page, settings)

    reservation.open_for_dates(room.room_id, *future_stay)

    reservation.expect_quote(nightly_rate=room.room_price, nights=2)
