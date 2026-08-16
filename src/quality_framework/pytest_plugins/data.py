"""Parallel-safe test data and idempotent cleanup fixtures."""

import warnings
from collections.abc import Generator
from datetime import UTC, date, datetime, timedelta

import pytest
from faker import Faker

from quality_framework.api.client import RestfulBookerApi
from quality_framework.data import BookingFactory

_CLEANUP_SUCCESS_STATUSES = {200, 202, 204, 404}


@pytest.fixture
def booking_factory() -> BookingFactory:
    return BookingFactory(Faker("en_GB"))


@pytest.fixture
def future_stay() -> tuple[date, date]:
    checkin = datetime.now(tz=UTC).date() + timedelta(days=400)
    return checkin, checkin + timedelta(days=2)


@pytest.fixture
def booking_cleanup(authenticated_api: RestfulBookerApi) -> Generator[list[int]]:
    created_ids: list[int] = []
    yield created_ids

    for booking_id in reversed(created_ids):
        response = authenticated_api.delete_booking(booking_id)
        if response.status not in _CLEANUP_SUCCESS_STATUSES:
            warnings.warn(
                f"Unable to clean booking {booking_id}: HTTP {response.status}",
                pytest.PytestWarning,
                stacklevel=1,
            )
