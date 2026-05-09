"""Base class for all marketing signal collectors."""

from abc import ABC, abstractmethod
from typing import Any


class BaseSignal(ABC):
    """Abstract base class for marketing signal collectors."""

    def __init__(self, api_key: str | None = None, dry_run: bool = False):
        self.api_key = api_key
        self.dry_run = dry_run
        self._validate_credentials()

    def _validate_credentials(self) -> None:
        """Check if API key is present."""
        if not self.api_key and not self.dry_run:
            print(f"[WARNING] {self.__class__.__name__}: API key not configured. Use dry_run=True for mock data.")

    @abstractmethod
    def run(self, keywords: list[str], geo: list[str]) -> list[dict[str, Any]]:
        """
        Collect marketing signals for prospects.

        Args:
            keywords: List of keywords to search for
            geo: List of country codes (e.g., ["FR", "BE"])

        Returns:
            List of signal dictionaries
        """
        pass

    @abstractmethod
    def dry_run_mock(self) -> list[dict[str, Any]]:
        """
        Return mock signal data for testing.

        Returns:
            List of 3 realistic fake signal entries
        """
        pass

    def execute(self, keywords: list[str], geo: list[str]) -> list[dict[str, Any]]:
        """Execute signal collection, using mock data if in dry_run mode."""
        if self.dry_run:
            return self.dry_run_mock()
        return self.run(keywords, geo)
