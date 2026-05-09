"""WhoisXML API integration for domain age and ownership data."""

from typing import Any

from .base import BaseEnrichment


class WhoisXMLEnrichment(BaseEnrichment):
    """
    WhoisXML API for domain age and ownership data.

    TODO: Implement API integration
    - Official docs: https://whois.whoisxmlapi.com/api
    - Endpoint: GET /api?apiKey={}&domainName={}
    - Auth: API Key in query param
    - Pricing: Free tier 500 lookups/month
    """

    def __init__(self, api_key: str | None = None, dry_run: bool = False):
        # TODO: Load API key from environment WHOISXML_API_KEY
        super().__init__(api_key, dry_run)

    def enrich(self, lead: dict[str, Any]) -> dict[str, Any]:
        """
        Enrich lead with domain age and ownership data.

        TODO: Implement API call
        1. Extract domain from lead
        2. GET whois lookup
        3. Parse createdDate for domain_age_days
        4. Extract registrar and owner info
        """
        if not self.api_key:
            raise ValueError(
                "WhoisXML API key required. "
                "Set WHOISXML_API_KEY env var or use dry_run=True."
            )

        domain = lead.get("domain", "")
        if not domain:
            raise ValueError("Lead must have a domain field")

        # TODO: Implement actual API call
        # response = requests.get(
        #     f"https://whois.whoisxmlapi.com/api",
        #     params={"apiKey": self.api_key, "domainName": domain}
        # )
        raise NotImplementedError("API call not yet implemented")

    def dry_run_mock(self) -> dict[str, Any]:
        """Return realistic mock enrichment data for testing."""
        return {
            "domain_age_days": 180,
            "domain_created": "2024-06-15",
            "domain_registrar": "OVH",
            "owner_country": "FR",
            "privacy_protected": False,
            "enrichment_source": "whoisxml",
        }
