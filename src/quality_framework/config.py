"""Environment-driven framework configuration."""

from functools import lru_cache

from pydantic import AnyHttpUrl, Field, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated settings shared by API and UI layers."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="TEST_",
        extra="ignore",
        frozen=True,
    )

    base_url: AnyHttpUrl = AnyHttpUrl("https://automationintesting.online")
    admin_username: str = "admin"
    admin_password: str = "password"
    action_timeout_ms: PositiveInt = Field(default=10_000)
    navigation_timeout_ms: PositiveInt = Field(default=30_000)
    expect_timeout_ms: PositiveInt = Field(default=10_000)

    @property
    def web_url(self) -> str:
        """Return the normalized application origin without a trailing slash."""

        return str(self.base_url).rstrip("/")

    @property
    def api_url(self) -> str:
        """Return the application-owned API proxy root."""

        return f"{self.web_url}/api"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load and cache settings once per process/xdist worker."""

    return Settings()
