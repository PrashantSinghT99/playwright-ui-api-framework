"""Validated settings and Playwright assertion configuration."""

import pytest
from playwright.sync_api import expect

from quality_framework.config import Settings, get_settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture(scope="session", autouse=True)
def configure_playwright_expectations(settings: Settings) -> None:
    """Apply the environment assertion budget once per pytest worker."""

    expect.set_options(timeout=settings.expect_timeout_ms)
