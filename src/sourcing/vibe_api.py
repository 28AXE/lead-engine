"""Vibe Prospecting API integration for B2B company discovery."""

from typing import Any

from .base import BaseSourcing


class VibeProspectingAPI(BaseSourcing):
    """
    Explorium Vibe Prospecting API for B2B company sourcing.

    TODO: Implement API integration
    - Official docs: https://developers.explorium.ai/vibe-prospecting/
    - Endpoint: POST /api/v1/prospecting/search
    - Auth: API Key in header (X-API-Key)
    """

    def __init__(self, api_key: str | None = None, dry_run: bool = False):
        # TODO: Load API key from environment VIBE_PROSPECTING_API_KEY
        super().__init__(api_key, dry_run)

    def search(self, keywords: list[str], geo: list[str]) -> list[dict[str, Any]]:
        """
        Search companies using Vibe Prospecting API.

        TODO: Implement API call
        1. Build query with keywords and geo filters
        2. POST to /api/v1/prospecting/search
        3. Parse response and extract company data
        4. Handle pagination for large result sets
        """
        if not self.api_key:
            raise ValueError(
                "Vibe Prospecting API key required. "
                "Set VIBE_PROSPECTING_API_KEY env var or use dry_run=True."
            )

        # TODO: Implement actual API call
        # response = requests.post(
        #     "https://api.explorium.ai/v1/prospecting/search",
        #     headers={"X-API-Key": self.api_key},
        #     json={"keywords": keywords, "geo": geo}
        # )
        raise NotImplementedError("API call not yet implemented")

    def dry_run_mock(self) -> list[dict[str, Any]]:
        """Return 3 realistic mock prospects for testing."""
        return [
            {
                "name": "Artisan Plomberie Services",
                "domain": "artisan-plomberie.fr",
                "industry": "Plomberie et chauffage",
                "employees": 12,
                "location": "Lyon, France",
                "geo": "FR",
                "keywords": ["plombier", "chauffagiste", "sanitaire"],
                "source": "vibe_api",
            },
            {
                "name": "EcoChauf Expert",
                "domain": "ecochauf-expert.be",
                "industry": "Énergies renouvelables",
                "employees": 8,
                "location": "Bruxelles, Belgique",
                "geo": "BE",
                "keywords": ["chauffagiste", "pompe à chaleur", "solaire"],
                "source": "vibe_api",
            },
            {
                "name": "Rapid Dépannage 24/7",
                "domain": "rapid-depannage247.fr",
                "industry": "Services d'urgence",
                "employees": 25,
                "location": "Marseille, France",
                "geo": "FR",
                "keywords": ["plombier", "dépannage", "urgence"],
                "source": "vibe_api",
            },
        ]
