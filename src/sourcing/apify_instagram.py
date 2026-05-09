"""Apify Instagram scraper for influencer marketing signals."""

from typing import Any

from .base import BaseSourcing


class ApifyInstagramScraper(BaseSourcing):
    """
    Apify Instagram Scraper Actor for influencer marketing signals.

    TODO: Implement API integration
    - Official docs: https://apify.com/apify/instagram-scraper
    - Actor: apify/instagram-scraper
    - Auth: API Token in header (Authorization: Bearer)
    """

    def __init__(self, api_key: str | None = None, dry_run: bool = False):
        # TODO: Load API key from environment APIFY_API_TOKEN
        super().__init__(api_key, dry_run)

    def search(self, keywords: list[str], geo: list[str]) -> list[dict[str, Any]]:
        """
        Scrape Instagram profiles using Apify Actor.

        TODO: Implement API call
        1. Start Instagram Scraper actor run
        2. Wait for completion (or use webhook)
        3. Fetch results from dataset
        4. Extract profile data and influencer metrics
        """
        if not self.api_key:
            raise ValueError(
                "Apify API token required. "
                "Set APIFY_API_TOKEN env var or use dry_run=True."
            )

        # TODO: Implement actual API call
        # 1. Start run: POST https://api.apify.com/v2/acts/apify~instagram-scraper/runs
        # 2. Poll status: GET https://api.apify.com/v2/actor-runs/{runId}
        # 3. Fetch data: GET https://api.apify.com/v2/datasets/{datasetId}/items
        raise NotImplementedError("API call not yet implemented")

    def dry_run_mock(self) -> list[dict[str, Any]]:
        """Return 3 realistic mock Instagram profiles for testing."""
        return [
            {
                "name": "Plombier Pro Tips",
                "domain": "plombier-pro-tips.com",
                "industry": "Formation plomberie",
                "employees": 3,
                "location": "France",
                "geo": "FR",
                "keywords": ["plombier", "formation", "conseils"],
                "source": "apify_instagram",
                "instagram_handle": "@plombier_pro_tips",
                "followers": 45000,
                "influencer_count": 2,
            },
            {
                "name": "Maison & Rénovation BE",
                "domain": "maison-renov.be",
                "industry": "Rénovation habitat",
                "employees": 8,
                "location": "Belgique",
                "geo": "BE",
                "keywords": ["rénovation", "sanitaire", "bricolage"],
                "source": "apify_instagram",
                "instagram_handle": "@maison_renov_be",
                "followers": 28000,
                "influencer_count": 3,
            },
            {
                "name": "Eco Habitat Solutions",
                "domain": "ecohabitat-solutions.fr",
                "industry": "Éco-rénovation",
                "employees": 12,
                "location": "Bordeaux, France",
                "geo": "FR",
                "keywords": ["éco-rénovation", "chauffage", "solaire"],
                "source": "apify_instagram",
                "instagram_handle": "@ecohabitat_solutions",
                "followers": 62000,
                "influencer_count": 5,
            },
        ]
