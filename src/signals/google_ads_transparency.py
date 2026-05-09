"""Google Ads Transparency API integration for ad spend signals."""

from typing import Any

from .base import BaseSignal


class GoogleAdsTransparencySignal(BaseSignal):
    """
    Google Ads Transparency Center for ad activity signals.

    TODO: Implement API integration
    - Official docs: https://developers.google.com/ads/transparency-center/api
    - Note: Google provides limited API access
    - Alternative: Manual scraping or third-party tools
    - Use case: Detect if prospect runs Google Ads (budget signal)
    """

    def __init__(self, api_key: str | None = None, dry_run: bool = False):
        # TODO: Load API key from environment GOOGLE_ADS_API_KEY
        super().__init__(api_key, dry_run)

    def run(self, keywords: list[str], geo: list[str]) -> list[dict[str, Any]]:
        """
        Get ad activity signals from Google Ads Transparency.

        TODO: Implement API call or scraping
        1. Search advertiser by domain/brand
        2. Count active ads and campaigns
        3. Extract ad history and spend estimates
        """
        if not self.api_key:
            raise ValueError(
                "Google Ads API key required. "
                "Set GOOGLE_ADS_API_KEY env var or use dry_run=True. "
                "Note: Limited API access. Consider alternative data sources."
            )

        # TODO: Implement actual API call or scraping
        # Google's API is limited - may need to use third-party alternatives
        raise NotImplementedError("API call not yet implemented")

    def dry_run_mock(self) -> list[dict[str, Any]]:
        """Return 3 realistic mock Google Ads signals for testing."""
        return [
            {
                "domain": "dubois-plomberie.fr",
                "running_google_ads": True,
                "google_ads_count": 12,
                "google_ads_status": "active",
                "estimated_google_spend": "1000-3000 EUR/month",
                "signal_source": "google_ads_transparency",
            },
            {
                "domain": "vdm-installaties.be",
                "running_google_ads": False,
                "google_ads_count": 0,
                "google_ads_status": "inactive",
                "estimated_google_spend": "0 EUR/month",
                "signal_source": "google_ads_transparency",
            },
            {
                "domain": "ecohauf-expert.be",
                "running_google_ads": True,
                "google_ads_count": 25,
                "google_ads_status": "active_high",
                "estimated_google_spend": "5000+ EUR/month",
                "signal_source": "google_ads_transparency",
            },
        ]
