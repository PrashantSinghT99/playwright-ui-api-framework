from datetime import date

import pytest

from quality_framework.data import BookingFactory

pytestmark = pytest.mark.unit


def test_factory_builds_valid_unique_bookings() -> None:
    factory = BookingFactory()

    first = factory.build(room_id=2, checkin=date(2027, 1, 10), nights=3)
    second = factory.build(room_id=2, checkin=date(2027, 1, 10), nights=3)

    assert first.room_id == 2
    assert first.booking_dates.checkout == date(2027, 1, 13)
    assert first.firstname != second.firstname
    assert first.email != second.email


def test_factory_rejects_zero_nights() -> None:
    with pytest.raises(ValueError, match="at least one"):
        BookingFactory().build(nights=0)
