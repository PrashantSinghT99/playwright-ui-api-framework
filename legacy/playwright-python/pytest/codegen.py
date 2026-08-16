from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://www.saucedemo.com/")
    page.locator("[data-test=\"username\"]").fill("standard_user")
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    page.pause()
    page.locator("[data-test=\"login-button\"]").click()
    page.get_by_role("button", name="Open Menu").click()
    page.locator("[data-test=\"logout-sidebar-link\"]").click()