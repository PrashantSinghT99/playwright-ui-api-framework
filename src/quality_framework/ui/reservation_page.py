"""Room quote and guest-reservation behaviors."""

import re
from datetime import date

from playwright.sync_api import Locator, expect

from quality_framework.api.models import Booking
from quality_framework.ui.base_page import BasePage


class ReservationPage(BasePage):
    @property
    def booking_heading(self) -> Locator:
        return self.page.get_by_role("heading", name="Book This Room", exact=True)

    @property
    def reserve_button(self) -> Locator:
        return self.page.get_by_role("button", name="Reserve Now", exact=True)

    @property
    def confirmation_heading(self) -> Locator:
        return self.page.get_by_role("heading", name="Booking Confirmed", exact=True)

    def open_for_dates(self, room_id: int, checkin: date, checkout: date) -> None:
        self.open(
            f"/reservation/{room_id}?checkin={checkin.isoformat()}&checkout={checkout.isoformat()}"
        )

    def expect_quote(self, *, nightly_rate: int, nights: int) -> None:
        room_charge = nightly_rate * nights
        total = room_charge + 40
        expect(
            self.page.get_by_text(
                re.compile(rf"£{nightly_rate}\s*x\s*{nights}\s*nights"),
            )
        ).to_be_visible()
        expect(self.page.get_by_text(f"£{room_charge}", exact=True)).to_be_visible()
        expect(self.page.get_by_text(f"£{total}", exact=True)).to_be_visible()

    def start_booking(self) -> None:
        self.reserve_button.click()
        expect(self.page.get_by_label("Firstname", exact=True)).to_be_visible()

    def enter_guest(self, booking: Booking) -> None:
        self.page.get_by_label("Firstname", exact=True).fill(booking.firstname)
        self.page.get_by_label("Lastname", exact=True).fill(booking.lastname)
        if booking.email:
            self.page.get_by_label("Email", exact=True).fill(booking.email)
        if booking.phone:
            self.page.get_by_label("Phone", exact=True).fill(booking.phone)

    def submit_booking(self) -> None:
        self.reserve_button.click()
        expect(self.confirmation_heading).to_be_visible()
