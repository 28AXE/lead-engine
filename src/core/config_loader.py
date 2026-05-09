"""Configuration loader for YAML and environment-based settings."""

from pathlib import Path
from typing import Any, Optional

import yaml
from dotenv import load_dotenv
import os

REQUIRED_FIELDS = [
    "vertical",
    "description",
    "geo",
    "keywords",
    "signals",
    "scoring_weights",
    "scoring_thresholds",
    "outreach",
    "notifications",
    "cache",
]


class ConfigError(Exception):
    """Raised when configuration is invalid or missing required fields."""


class ConfigLoader:
    """Loads and validates YAML configuration with typed access to parameters."""

    def __init__(self, config_path: str | Path):
        self.config_path = Path(config_path)
        self._config: dict[str, Any] = {}
        self._load()
        self._validate()

    def _load(self) -> None:
        """Load YAML configuration file."""
        if not self.config_path.exists():
            raise ConfigError(f"Configuration file not found: {self.config_path}")

        load_dotenv()

        with open(self.config_path, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f)

        if not self._config:
            raise ConfigError(f"Configuration file is empty: {self.config_path}")

    def _validate(self) -> None:
        """Validate that all required fields are present."""
        missing = [field for field in REQUIRED_FIELDS if field not in self._config]
        if missing:
            raise ConfigError(
                f"Missing required configuration fields: {', '.join(missing)}"
            )

        # Validate scoring_weights structure
        weights = self._config.get("scoring_weights", {})
        required_weights = ["domain_age", "ad_activity", "budget_signal", "vertical_fit"]
        missing_weights = [w for w in required_weights if w not in weights]
        if missing_weights:
            raise ConfigError(
                f"Missing scoring weights: {', '.join(missing_weights)}"
            )

        # Validate scoring_thresholds structure
        thresholds = self._config.get("scoring_thresholds", {})
        required_thresholds = ["hot", "warm", "cold"]
        missing_thresholds = [t for t in required_thresholds if t not in thresholds]
        if missing_thresholds:
            raise ConfigError(
                f"Missing scoring thresholds: {', '.join(missing_thresholds)}"
            )

    @property
    def vertical(self) -> str:
        return self._config["vertical"]

    @property
    def description(self) -> str:
        return self._config["description"]

    @property
    def dry_run(self) -> bool:
        return self._config.get("dry_run", False)

    @property
    def geo(self) -> list[str]:
        return self._config["geo"]

    @property
    def keywords(self) -> list[str]:
        return self._config["keywords"]

    @property
    def signals(self) -> list[str]:
        return self._config["signals"]

    @property
    def scoring_weights(self) -> dict[str, int]:
        return self._config["scoring_weights"]

    @property
    def scoring_thresholds(self) -> dict[str, int]:
        return self._config["scoring_thresholds"]

    @property
    def outreach(self) -> dict[str, str]:
        return self._config["outreach"]

    @property
    def notifications(self) -> dict[str, Any]:
        return self._config["notifications"]

    @property
    def cache(self) -> dict[str, Any]:
        return self._config["cache"]

    @property
    def cache_enabled(self) -> bool:
        return self._config["cache"].get("enabled", True)

    @property
    def cache_ttl_hours(self) -> int:
        return self._config["cache"].get("ttl_hours", 24)

    def is_signal_enabled(self, signal_name: str) -> bool:
        """Check if a specific signal source is enabled."""
        return signal_name in self._config.get("signals", [])

    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key from environment variables."""
        env_key = f"{service.upper()}_API_KEY"
        return os.getenv(env_key)

    def __repr__(self) -> str:
        return f"ConfigLoader(vertical='{self.vertical}', dry_run={self.dry_run})"
