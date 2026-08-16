"""Load the framework's focused pytest plugins as the test-suite composition root."""

pytest_plugins = (
    "quality_framework.pytest_plugins.policy",
    "quality_framework.pytest_plugins.configuration",
    "quality_framework.pytest_plugins.browser",
    "quality_framework.pytest_plugins.api",
    "quality_framework.pytest_plugins.data",
)
