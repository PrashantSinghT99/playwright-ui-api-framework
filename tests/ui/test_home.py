import pytest
from playwright.sync_api import Page

from quality_framework.config import Settings
from quality_framework.ui import HomePage

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_guest_can_discover_available_room_types(page: Page, settings: Settings) -> None:
    home = HomePage(page, settings)

    home.open()

    home.expect_loaded()
    home.expect_room_types("Single", "Double", "Suite")
