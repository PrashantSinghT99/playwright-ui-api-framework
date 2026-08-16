"""Public hotel landing-page behaviors."""

from playwright.sync_api import Locator, expect

from quality_framework.ui.base_page import BasePage


class HomePage(BasePage):
    @property
    def hero_heading(self) -> Locator:
        return self.page.get_by_role("heading", name="Welcome to Shady Meadows B&B", exact=True)

    @property
    def rooms_heading(self) -> Locator:
        return self.page.get_by_role("heading", name="Our Rooms", exact=True)

    @property
    def check_availability_button(self) -> Locator:
        return self.page.get_by_role("button", name="Check Availability", exact=True)

    def room_heading(self, room_type: str) -> Locator:
        return self.page.get_by_role("heading", name=room_type, exact=True)

    def open_first_room(self) -> None:
        self.page.get_by_role("link", name="Book now", exact=True).first.click()

    def expect_room_types(self, *room_types: str) -> None:
        for room_type in room_types:
            expect(self.room_heading(room_type)).to_be_visible()

    def expect_loaded(self) -> None:
        expect(self.hero_heading).to_be_visible()
        expect(self.rooms_heading).to_be_visible()
        expect(self.check_availability_button).to_be_enabled()
