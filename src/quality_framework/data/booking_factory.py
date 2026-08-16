"""Parallel-safe booking test-data generation."""

from datetime import UTC, date, datetime, timedelta
from uuid import uuid4

from faker import Faker

from quality_framework.api.models import Booking, BookingDates


class BookingFactory:
    """Create valid domain objects with a unique worker/run fingerprint."""

    def __init__(self, faker: Faker | None = None) -> None:
        self._faker = faker or Faker()

    def build(
        self,
        *,
        room_id: int = 1,
        checkin: date | None = None,
        nights: int = 2,
    ) -> Booking:
        if nights < 1:
            raise ValueError("nights must be at least one")

        start = checkin or (datetime.now(tz=UTC).date() + timedelta(days=400))
        suffix = uuid4().hex[:6]
        firstname = f"Auto{suffix}"[:18]
        lastname = f"Test{self._faker.last_name()}"[:30]

        return Booking(
            room_id=room_id,
            firstname=firstname,
            lastname=lastname,
            deposit_paid=False,
            booking_dates=BookingDates(
                checkin=start,
                checkout=start + timedelta(days=nights),
            ),
            email=f"{suffix}@example.test",
            phone="01234567890",
        )
