"""Browser defaults shared by every UI test."""

from typing import Any

import pytest


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
