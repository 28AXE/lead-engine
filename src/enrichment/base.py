"""Base class for all data enrichment providers."""

from abc import ABC, abstractmethod
from typing import Any


class BaseEnrichment(ABC):
    """Abstract base class for data enrichment providers."""

    def __init__(self, api_key: str | None = None, dry_run: bool = False):
        self.api_key = api_key
        self.dry_run = dry_run
        self._validate_credentials()

    def _validate_credentials(self) -> None:
        """Check if API key is present."""
        if not self.api_key and not self.dry_run:
            print(f"[WARNING] {self.__class__.__name__}: API key not configured. Use dry_run=True for mock data.")

    @abstractmethod
    def enrich(self, lead: dict[str, Any]) -> dict[str, Any]:
        """
        Enrich a lead with additional data.

        Args:
            lead: Basic lead dictionary

        Returns:
            Lead dictionary with added enrichment data
        """
        pass

    @abstractmethod
    def dry_run_mock(self) -> dict[str, Any]:
        """
        Return mock enrichment data for testing.

        Returns:
            Dictionary with realistic fake enrichment data
        """
        pass

    def execute(self, lead: dict[str, Any]) -> dict[str, Any]:
        """Execute enrichment, using mock data if in dry_run mode."""
        if self.dry_run:
            mock_data = self.dry_run_mock()
            return {**lead, **mock_data}
        return self.enrich(lead)
