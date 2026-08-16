import pytest

from quality_framework.polling import poll_until

pytestmark = pytest.mark.unit


def test_polling_returns_after_transient_absence() -> None:
    observations = iter([None, "ready"])

    result = poll_until(
        lambda: next(observations),
        timeout_seconds=0.1,
        interval_seconds=0,
        description="test observation",
    )

    assert result == "ready"


def test_polling_reports_a_diagnostic_timeout() -> None:
    with pytest.raises(TimeoutError, match="waiting for unavailable booking"):
        poll_until(
            lambda: None,
            timeout_seconds=0.001,
            interval_seconds=0.001,
            description="unavailable booking",
        )
