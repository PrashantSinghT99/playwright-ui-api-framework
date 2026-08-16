"""API transport and authenticated domain-client fixtures."""

from collections.abc import Generator

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from quality_framework.api.client import RestfulBookerApi
from quality_framework.config import Settings


@pytest.fixture(scope="session")
def api_context(playwright: Playwright, settings: Settings) -> Generator[APIRequestContext]:
    context = playwright.request.new_context(
        base_url=settings.web_url,
        extra_http_headers={
            "Accept": "application/json",
            "User-Agent": "playwright-quality-framework/1.0",
        },
        timeout=settings.navigation_timeout_ms,
    )
    yield context
    context.dispose()


@pytest.fixture(scope="session")
def api_client(api_context: APIRequestContext) -> RestfulBookerApi:
    return RestfulBookerApi(api_context)


@pytest.fixture(scope="session")
def authenticated_api(api_client: RestfulBookerApi, settings: Settings) -> RestfulBookerApi:
    return api_client.authenticate(settings.admin_username, settings.admin_password)
