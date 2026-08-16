from datetime import date

import pytest

from quality_framework.api import RestfulBookerApi, expect_status
from quality_framework.api.models import Booking, Bookings, Rooms
from quality_framework.data import BookingFactory

pytestmark = [pytest.mark.api, pytest.mark.mutation]


def test_booking_crud_lifecycle(
    api_client: RestfulBookerApi,
    authenticated_api: RestfulBookerApi,
    booking_factory: BookingFactory,
    future_stay: tuple[date, date],
    booking_cleanup: list[int],
) -> None:
    available_rooms = Rooms.model_validate(
        expect_status(api_client.get_rooms(*future_stay), 200).json()
    ).rooms
    assert available_rooms, "No room is available for the isolated test window"
    booking = booking_factory.build(room_id=available_rooms[0].room_id, checkin=future_stay[0])

    created_response = expect_status(api_client.create_booking(booking), 201)
    Booking.model_validate(created_response.json())

    booking_id = _find_booking_id(authenticated_api, booking)
    booking_cleanup.append(booking_id)

    updated = booking.model_copy(update={"deposit_paid": True})
    expect_status(authenticated_api.update_booking(booking_id, updated), 200)
    persisted = Booking.model_validate(
        expect_status(authenticated_api.get_booking(booking_id), 200).json()
    )
    assert persisted.deposit_paid is True

    expect_status(authenticated_api.delete_booking(booking_id), 200)
    booking_cleanup.remove(booking_id)


def _find_booking_id(client: RestfulBookerApi, expected: Booking) -> int:
    payload = expect_status(client.get_bookings(expected.room_id), 200).json()
    bookings = Bookings.model_validate(payload).bookings
    match = next(
        (
            booking
            for booking in bookings
            if booking.firstname == expected.firstname and booking.lastname == expected.lastname
        ),
        None,
    )
    assert match is not None, "Created booking was not queryable"
    assert match.booking_id is not None, "Created booking had no identifier"
    return match.booking_id
