"""Pappers API integration for French company registration data."""

from typing import Any

from .base import BaseEnrichment


class PappersEnrichment(BaseEnrichment):
    """
    Pappers.fr API for French company legal data.

    TODO: Implement API integration
    - Official docs: https://www.pappers.fr/api
    - Endpoints:
      - /entreprise/{siren}: Company details
      - /recherche: Search companies
    - Auth: API Key in header (Authorization: Bearer)
    - Pricing: Free tier 100 requests/day
    """

    def __init__(self, api_key: str | None = None, dry_run: bool = False):
        # TODO: Load API key from environment PAPPERS_API_KEY
        super().__init__(api_key, dry_run)

    def enrich(self, lead: dict[str, Any]) -> dict[str, Any]:
        """
        Enrich lead with French company registration data.

        TODO: Implement API call
        1. Search company by name/domain to get SIREN
        2. GET /entreprise/{siren} for detailed info
        3. Extract employee count, revenue, legal form
        4. Get dirigesants (executives) names
        """
        if not self.api_key:
            raise ValueError(
                "Pappers API key required. "
                "Set PAPPERS_API_KEY env var or use dry_run=True."
            )

        # TODO: Implement actual API call
        # 1. Search: GET https://api.pappers.fr/v1/recherche?q={company_name}
        # 2. Details: GET https://api.pappers.fr/v1/entreprise/{siren}
        raise NotImplementedError("API call not yet implemented")

    def dry_run_mock(self) -> dict[str, Any]:
        """Return realistic mock enrichment data for testing."""
        return {
            "siren": "123456789",
            "siret": "12345678901234",
            "legal_form": "SARL",
            "employee_count": 12,
            "revenue_range": "500K-1M EUR",
            "creation_date": "2018-03-15",
            "dirigeants": ["Jean Dubois", "Marie Laurent"],
            "naf_code": "4322A",
            "naf_label": "Travaux d'installation d'eau et de gaz",
            "enrichment_source": "pappers",
        }
