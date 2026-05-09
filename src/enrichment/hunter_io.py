"""Hunter.io API integration for email discovery."""

from typing import Any

from .base import BaseEnrichment


class HunterIOEnrichment(BaseEnrichment):
    """
    Hunter.io API for email discovery and verification.

    TODO: Implement API integration
    - Official docs: https://hunter.io/api-documentation
    - Endpoints:
      - /v2/domain-search: Find emails for a domain
      - /v2/email-verifier: Verify an email
    - Auth: API Key in query param (api_key=)
    - Pricing: Free tier 25 searches/month
    """

    def __init__(self, api_key: str | None = None, dry_run: bool = False):
        # TODO: Load API key from environment HUNTER_IO_API_KEY
        super().__init__(api_key, dry_run)

    def enrich(self, lead: dict[str, Any]) -> dict[str, Any]:
        """
        Enrich lead with contact emails.

        TODO: Implement API call
        1. Extract domain from lead
        2. GET /v2/domain-search with domain filter
        3. Parse emails and find decision-maker contacts
        4. Optionally verify email with /v2/email-verifier
        """
        if not self.api_key:
            raise ValueError(
                "Hunter.io API key required. "
                "Set HUNTER_IO_API_KEY env var or use dry_run=True."
            )

        domain = lead.get("domain", "")
        if not domain:
            raise ValueError("Lead must have a domain field")

        # TODO: Implement actual API call
        # response = requests.get(
        #     "https://api.hunter.io/v2/domain-search",
        #     params={"domain": domain, "api_key": self.api_key}
        # )
        raise NotImplementedError("API call not yet implemented")

    def dry_run_mock(self) -> dict[str, Any]:
        """Return realistic mock enrichment data for testing."""
        return {
            "email": "contact@dubois-plomberie.fr",
            "email_position": "owner",
            "email_confidence": 92,
            "phone": "+33 1 23 45 67 89",
            "linkedin_url": "https://linkedin.com/company/dubois-plomberie",
            "enrichment_source": "hunter_io",
        }
