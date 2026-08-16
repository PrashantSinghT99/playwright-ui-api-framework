import pytest
from pydantic import ValidationError

from quality_framework.config import Settings

pytestmark = pytest.mark.unit


def test_urls_are_normalized_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_BASE_URL", "https://example.test/environment/")

    settings = Settings()

    assert settings.web_url == "https://example.test/environment"
    assert settings.api_url == "https://example.test/environment/api"


def test_invalid_base_url_fails_fast() -> None:
    with pytest.raises(ValidationError):
        Settings(base_url="not-a-url")  # type: ignore[arg-type]


def test_non_positive_timeout_fails_fast() -> None:
    with pytest.raises(ValidationError):
        Settings(action_timeout_ms=0)
