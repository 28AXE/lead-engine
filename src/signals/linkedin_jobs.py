"""LinkedIn Jobs scraping for hiring signals."""

from typing import Any

from .base import BaseSignal


class LinkedInJobsSignal(BaseSignal):
    """
    LinkedIn Jobs scraping for hiring and growth signals.

    TODO: Implement scraping/integration
    - Official API: https://learn.microsoft.com/en-us/linkedin/marketing/
    - Note: LinkedIn API is restrictive for job data
    - Alternatives:
      - Apify LinkedIn Jobs Scraper: https://apify.com/apify/linkedin-jobs-scraper
      - Rainforest LinkedIn Jobs API: https://www.rainforestapi.com/
    - Use case: Detect if company is hiring (growth signal)
    """

    def __init__(self, api_key: str | None = None, dry_run: bool = False):
        # TODO: Load API key from environment (Apify token or Rainforest API key)
        super().__init__(api_key, dry_run)

    def run(self, keywords: list[str], geo: list[str]) -> list[dict[str, Any]]:
        """
        Get hiring signals from LinkedIn Jobs.

        TODO: Implement scraping via Apify or Rainforest API
        1. Search jobs by company name
        2. Count active job postings
        3. Extract job titles (look for marketing/performance roles)
        4. Detect growth trajectory
        """
        if not self.api_key:
            raise ValueError(
                "LinkedIn Jobs API key required. "
                "Set LINKEDIN_JOBS_API_KEY env var or use dry_run=True. "
                "Use Apify LinkedIn Jobs Scraper or Rainforest API."
            )

        # TODO: Implement actual API call
        # Option 1: Apify Actor
        # POST https://api.apify.com/v2/acts/apify~linkedin-jobs-scraper/runs
        # Option 2: Rainforest API
        # GET https://api.rainforestapi.com/request?api_key=xxx&engine=linkedin_jobs
        raise NotImplementedError("API call not yet implemented")

    def dry_run_mock(self) -> list[dict[str, Any]]:
        """Return 3 realistic mock LinkedIn Jobs signals for testing."""
        return [
            {
                "domain": "dubois-plomberie.fr",
                "linkedin_jobs_count": 2,
                "linkedin_hiring_status": "hiring_low",
                "open_positions": ["Plombier CVC", "Apprenti chauffagiste"],
                "hiring_marketing_roles": False,
                "signal_source": "linkedin_jobs",
            },
            {
                "domain": "vdm-installaties.be",
                "linkedin_jobs_count": 0,
                "linkedin_hiring_status": "not_hiring",
                "open_positions": [],
                "hiring_marketing_roles": False,
                "signal_source": "linkedin_jobs",
            },
            {
                "domain": "ecohaif-expert.be",
                "linkedin_jobs_count": 8,
                "linkedin_hiring_status": "hiring_high",
                "open_positions": [
                    "Commercial B2B",
                    "Technicien frigoriste",
                    "Responsable marketing digital",
                ],
                "hiring_marketing_roles": True,
                "signal_source": "linkedin_jobs",
            },
        ]
