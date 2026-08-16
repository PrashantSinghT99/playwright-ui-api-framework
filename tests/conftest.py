"""Cross-layer pytest composition and safety controls."""

import warnings
from collections.abc import Generator
from datetime import UTC, date, datetime, timedelta
from typing import Any

import pytest
from faker import Faker
from playwright.sync_api import APIRequestContext, Playwright

from quality_framework.api.client import RestfulBookerApi
from quality_framework.config import Settings, get_settings
from quality_framework.data import BookingFactory


def pytest_addoption(parser: pytest.Parser) -> None:
    safety = parser.getgroup("target safety")
    safety.addoption(
        "--run-mutation",
        action="store_true",
        default=False,
        help="run tests that create or update target-application data",
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if config.getoption("--run-mutation"):
        return

    skip_mutation = pytest.mark.skip(reason="requires explicit --run-mutation opt-in")
    for item in items:
        if "mutation" in item.keywords:
            item.add_marker(skip_mutation)


def pytest_report_header(config: pytest.Config) -> str:
    del config
    return f"test target: {get_settings().web_url}"


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture(scope="session")
def browser_context_args(
    browser_context_args: dict[str, Any],
) -> dict[str, Any]:
    return {
        **browser_context_args,
        "locale": "en-GB",
        "timezone_id": "Europe/London",
        "viewport": {"width": 1440, "height": 900},
    }


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


@pytest.fixture
def booking_factory() -> BookingFactory:
    return BookingFactory(Faker("en_GB"))


@pytest.fixture
def future_stay() -> tuple[date, date]:
    checkin = datetime.now(tz=UTC).date() + timedelta(days=400)
    return checkin, checkin + timedelta(days=2)


@pytest.fixture
def booking_cleanup(authenticated_api: RestfulBookerApi) -> Generator[list[int]]:
    created_ids: list[int] = []
    yield created_ids

    for booking_id in reversed(created_ids):
        response = authenticated_api.delete_booking(booking_id)
        if response.status not in {200, 204, 404}:
            warnings.warn(
                f"Unable to clean booking {booking_id}: HTTP {response.status}",
                stacklevel=1,
            )
