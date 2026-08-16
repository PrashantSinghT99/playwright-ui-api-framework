"""Collection-time safety policy and execution metadata."""

import pytest

from quality_framework.config import get_settings


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
