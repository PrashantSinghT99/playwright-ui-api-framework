"""Administrator authentication behaviors."""

import re

from playwright.sync_api import Locator, expect

from quality_framework.ui.base_page import BasePage


class AdminLoginPage(BasePage):
    @property
    def username_input(self) -> Locator:
        return self.page.get_by_label("Username", exact=True)

    @property
    def password_input(self) -> Locator:
        return self.page.get_by_label("Password", exact=True)

    @property
    def login_button(self) -> Locator:
        return self.page.get_by_role("button", name="Login", exact=True)

    @property
    def logout_button(self) -> Locator:
        return self.page.get_by_role("button", name="Logout", exact=True)

    def open_login(self) -> None:
        self.open("/admin")
        expect(self.login_button).to_be_visible()

    def sign_in(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def expect_signed_in(self) -> None:
        expect(self.page.get_by_role("link", name="Rooms", exact=True)).to_be_visible()
        expect(self.logout_button).to_be_visible()

    def expect_sign_in_rejected(self) -> None:
        expect(self.page.get_by_text("Invalid credentials", exact=True)).to_be_visible()
        expect(self.login_button).to_be_visible()

    def sign_out(self) -> None:
        self.logout_button.click()
        expect(self.page).to_have_url(re.compile(r"/$"))
        expect(
            self.page.get_by_role(
                "heading",
                name="Welcome to Shady Meadows B&B",
                exact=True,
            )
        ).to_be_visible()
