"""Google Maps API integration for local business discovery."""

from typing import Any

from .base import BaseSourcing


class GoogleMapsSourcing(BaseSourcing):
    """
    Google Maps Places API for local business sourcing.

    TODO: Implement API integration
    - Official docs: https://developers.google.com/maps/documentation/places/web-service
    - Endpoint: GET /maps/api/place/nearbysearch/json
    - Auth: API Key in query param (key=)
    """

    def __init__(self, api_key: str | None = None, dry_run: bool = False):
        # TODO: Load API key from environment GOOGLE_MAPS_API_KEY
        super().__init__(api_key, dry_run)

    def search(self, keywords: list[str], geo: list[str]) -> list[dict[str, Any]]:
        """
        Search local businesses using Google Maps Places API.

        TODO: Implement API call
        1. Convert geo codes to lat/lng coordinates
        2. Build search query with keyword and location
        3. GET /maps/api/place/nearbysearch/json
        4. Parse place details and extract business info
        """
        if not self.api_key:
            raise ValueError(
                "Google Maps API key required. "
                "Set GOOGLE_MAPS_API_KEY env var or use dry_run=True."
            )

        # TODO: Implement actual API call
        # response = requests.get(
        #     "https://maps.googleapis.com/maps/api/place/nearbysearch/json",
        #     params={"keyword": keywords[0], "location": lat_lng, "radius": 50000, "key": self.api_key}
        # )
        raise NotImplementedError("API call not yet implemented")

    def dry_run_mock(self) -> list[dict[str, Any]]:
        """Return 3 realistic mock local businesses for testing."""
        return [
            {
                "name": "Dubois Plomberie SARL",
                "domain": "dubois-plomberie.fr",
                "industry": "Plomberie",
                "employees": 5,
                "location": "Paris 15ème, France",
                "geo": "FR",
                "keywords": ["plombier", "réparation", "installation"],
                "source": "google_maps",
                "rating": 4.7,
                "reviews_count": 89,
            },
            {
                "name": "Van Der Meer Installaties",
                "domain": "vdm-installaties.be",
                "industry": "Installations sanitaires",
                "employees": 15,
                "location": "Anvers, Belgique",
                "geo": "BE",
                "keywords": ["plombier", "sanitaire", "rénovation"],
                "source": "google_maps",
                "rating": 4.5,
                "reviews_count": 124,
            },
            {
                "name": "Méditerranée Chauffage",
                "domain": "med-chauffage.fr",
                "industry": "Chauffage et climatisation",
                "employees": 20,
                "location": "Nice, France",
                "geo": "FR",
                "keywords": ["chauffagiste", "climatisation", "entretien"],
                "source": "google_maps",
                "rating": 4.8,
                "reviews_count": 203,
            },
        ]
