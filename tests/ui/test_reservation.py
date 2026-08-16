from datetime import UTC, datetime, timedelta

import pytest
from playwright.sync_api import Page

from quality_framework.config import Settings
from quality_framework.ui import ReservationPage

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_guest_sees_itemized_price_before_reserving(page: Page, settings: Settings) -> None:
    checkin = datetime.now(tz=UTC).date() + timedelta(days=60)
    reservation = ReservationPage(page, settings)

    reservation.open_for_dates(1, checkin, checkin + timedelta(days=2))

    reservation.expect_quote(nightly_rate=100, nights=2)
