import pytest
from playwright.sync_api import Page

from quality_framework.config import Settings
from quality_framework.ui import AdminLoginPage

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_admin_can_sign_in(page: Page, settings: Settings) -> None:
    login = AdminLoginPage(page, settings)
    login.open_login()

    login.sign_in(settings.admin_username, settings.admin_password)

    login.expect_signed_in()


def test_invalid_admin_credentials_are_rejected(page: Page, settings: Settings) -> None:
    login = AdminLoginPage(page, settings)
    login.open_login()

    login.sign_in("not-a-user", "not-a-password")

    login.expect_sign_in_rejected()


def test_admin_can_sign_out(page: Page, settings: Settings) -> None:
    login = AdminLoginPage(page, settings)
    login.open_login()
    login.sign_in(settings.admin_username, settings.admin_password)
    login.expect_signed_in()

    login.sign_out()
