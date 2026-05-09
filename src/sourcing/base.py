"""Base class for all prospect sourcing sources."""

from abc import ABC, abstractmethod
from typing import Any


class BaseSourcing(ABC):
    """Abstract base class for prospect sourcing providers."""

    def __init__(self, api_key: str | None = None, dry_run: bool = False):
        self.api_key = api_key
        self.dry_run = dry_run
        self._validate_credentials()

    def _validate_credentials(self) -> None:
        """Check if API key is present."""
        if not self.api_key and not self.dry_run:
            print(f"[WARNING] {self.__class__.__name__}: API key not configured. Use dry_run=True for mock data.")

    @abstractmethod
    def search(self, keywords: list[str], geo: list[str]) -> list[dict[str, Any]]:
        """
        Search for prospects matching keywords in specified geographies.

        Args:
            keywords: List of keywords to search for
            geo: List of country codes (e.g., ["FR", "BE"])

        Returns:
            List of prospect dictionaries with basic info
        """
        pass

    @abstractmethod
    def dry_run_mock(self) -> list[dict[str, Any]]:
        """
        Return mock data for testing without API calls.

        Returns:
            List of 3 realistic fake prospects
        """
        pass

    def execute(self, keywords: list[str], geo: list[str]) -> list[dict[str, Any]]:
        """Execute search, using mock data if in dry_run mode."""
        if self.dry_run:
            return self.dry_run_mock()
        return self.search(keywords, geo)
