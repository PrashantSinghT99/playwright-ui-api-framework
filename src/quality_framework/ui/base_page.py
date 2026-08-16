"""Shared browser-page behavior."""

from urllib.parse import urljoin

from playwright.sync_api import Page

from quality_framework.config import Settings


class BasePage:
    def __init__(self, page: Page, settings: Settings) -> None:
        self.page = page
        self.settings = settings
        self.page.set_default_timeout(settings.action_timeout_ms)
        self.page.set_default_navigation_timeout(settings.navigation_timeout_ms)

    def open(self, path: str = "/") -> None:
        url = urljoin(f"{self.settings.web_url}/", path.lstrip("/"))
        self.page.goto(url, wait_until="domcontentloaded")
