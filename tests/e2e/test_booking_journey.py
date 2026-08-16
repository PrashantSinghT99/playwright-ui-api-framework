from datetime import date
from time import sleep

import pytest
from playwright.sync_api import Page

from quality_framework.api import RestfulBookerApi, expect_status
from quality_framework.api.models import Booking, Bookings, Rooms
from quality_framework.config import Settings
from quality_framework.data import BookingFactory
from quality_framework.ui import ReservationPage

pytestmark = [pytest.mark.e2e, pytest.mark.mutation]


def test_ui_booking_is_observable_and_cleanable_through_api(
    page: Page,
    settings: Settings,
    api_client: RestfulBookerApi,
    authenticated_api: RestfulBookerApi,
    booking_factory: BookingFactory,
    future_stay: tuple[date, date],
    booking_cleanup: list[int],
) -> None:
    rooms = Rooms.model_validate(
        expect_status(api_client.get_rooms(*future_stay), 200).json()
    ).rooms
    assert rooms, "No room is available for the isolated test window"
    room = rooms[0]
    booking = booking_factory.build(room_id=room.room_id, checkin=future_stay[0])
    reservation = ReservationPage(page, settings)

    reservation.open_for_dates(room.room_id, *future_stay)
    reservation.start_booking()
    reservation.enter_guest(booking)
    reservation.submit_booking()

    persisted = _wait_for_booking(authenticated_api, booking)
    assert persisted.booking_id is not None
    booking_cleanup.append(persisted.booking_id)


def _wait_for_booking(client: RestfulBookerApi, expected: Booking) -> Booking:
    for _ in range(10):
        response = client.get_bookings(expected.room_id)
        if response.status == 200:
            bookings = Bookings.model_validate(response.json()).bookings
            match = next(
                (
                    booking
                    for booking in bookings
                    if booking.firstname == expected.firstname
                    and booking.lastname == expected.lastname
                ),
                None,
            )
            if match is not None:
                return match
        sleep(0.5)
    pytest.fail("UI-created booking did not become observable through the API")
