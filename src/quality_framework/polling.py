"""Small polling primitive for explicit eventual-consistency boundaries."""

from collections.abc import Callable
from time import monotonic, sleep
from typing import TypeVar

T = TypeVar("T")


def poll_until(
    probe: Callable[[], T | None],
    *,
    timeout_seconds: float,
    interval_seconds: float,
    description: str,
) -> T:
    """Return the first non-None probe result or raise a diagnostic timeout."""

    deadline = monotonic() + timeout_seconds
    while True:
        result = probe()
        if result is not None:
            return result

        remaining = deadline - monotonic()
        if remaining <= 0:
            raise TimeoutError(f"Timed out waiting for {description}")
        sleep(min(interval_seconds, remaining))
