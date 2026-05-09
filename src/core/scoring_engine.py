"""40-point scoring engine for prospect qualification."""

from typing import Any

from .config_loader import ConfigLoader


class ScoringEngine:
    """Scores prospects using configurable weights and thresholds."""

    def __init__(self, config: ConfigLoader):
        self.config = config
        self.weights = config.scoring_weights
        self.thresholds = config.scoring_thresholds

    def score(self, lead: dict[str, Any]) -> dict[str, Any]:
        """Score a single lead and return detailed results."""
        breakdown = {
            "domain_age": self._score_domain_age(lead),
            "ad_activity": self._score_ad_activity(lead),
            "budget_signal": self._score_budget_signal(lead),
            "vertical_fit": self._score_vertical_fit(lead),
        }

        total_score = sum(breakdown.values())
        verdict = self._get_verdict(total_score)

        return {
            "score": total_score,
            "verdict": verdict,
            "breakdown": breakdown,
        }

    def _score_domain_age(self, lead: dict[str, Any]) -> int:
        """Score based on domain age (newer = higher score)."""
        domain_age_days = lead.get("domain_age_days", 365)

        if domain_age_days <= 90:
            return self.weights["domain_age"]
        elif domain_age_days <= 180:
            return int(self.weights["domain_age"] * 0.8)
        elif domain_age_days <= 365:
            return int(self.weights["domain_age"] * 0.6)
        elif domain_age_days <= 730:
            return int(self.weights["domain_age"] * 0.4)
        elif domain_age_days <= 1095:
            return int(self.weights["domain_age"] * 0.2)
        else:
            return 0

    def _score_ad_activity(self, lead: dict[str, Any]) -> int:
        """Score based on Meta ad activity (sweet spot: 0-10 ads)."""
        ad_count = lead.get("meta_ad_count", 0)

        if ad_count == 0:
            return self.weights["ad_activity"]
        elif ad_count <= 10:
            return int(self.weights["ad_activity"] * 0.9)
        elif ad_count <= 20:
            return int(self.weights["ad_activity"] * 0.7)
        elif ad_count <= 50:
            return int(self.weights["ad_activity"] * 0.4)
        else:
            return 0

    def _score_budget_signal(self, lead: dict[str, Any]) -> int:
        """Score based on budget signals (influencers, google ads, funding)."""
        score = 0
        max_score = self.weights["budget_signal"]

        influencer_count = lead.get("influencer_count", 0)
        if influencer_count >= 5:
            score += max_score * 0.5
        elif influencer_count >= 3:
            score += max_score * 0.35
        elif influencer_count >= 1:
            score += max_score * 0.2

        if lead.get("running_google_ads", False):
            score += max_score * 0.3

        funding_status = lead.get("funding_status", "")
        if funding_status in ("seed", "series_a", "series_b"):
            score += max_score * 0.2

        employee_count = lead.get("employee_count", 0)
        if employee_count >= 50:
            score += max_score * 0.1
        elif employee_count >= 10:
            score += max_score * 0.05

        return int(min(score, max_score))

    def _score_vertical_fit(self, lead: dict[str, Any]) -> int:
        """Score based on vertical fit."""
        vertical = lead.get("vertical", "").lower()
        keywords = [k.lower() for k in self.config.keywords]

        max_score = self.weights["vertical_fit"]

        lead_keywords = lead.get("keywords", [])
        matches = sum(1 for kw in keywords if any(kw in lw for lw in lead_keywords))

        if matches >= 2:
            return max_score
        elif matches == 1:
            return int(max_score * 0.7)
        else:
            return int(max_score * 0.3)

    def _get_verdict(self, score: int) -> str:
        """Determine verdict based on score and thresholds."""
        if score >= self.thresholds["hot"]:
            return "HOT"
        elif score >= self.thresholds["warm"]:
            return "WARM"
        elif score >= self.thresholds["cold"]:
            return "COLD"
        else:
            return "DISQUALIFIED"

    def batch_score(self, leads: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Score multiple leads and return sorted by score descending."""
        scored = []

        for lead in leads:
            result = self.score(lead)
            result["lead"] = lead
            scored.append(result)

        return sorted(scored, key=lambda x: x["score"], reverse=True)

    def get_hot_leads(self, leads: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Filter and return only HOT leads."""
        scored = self.batch_score(leads)
        return [r for r in scored if r["verdict"] == "HOT"]

    def __repr__(self) -> str:
        return f"ScoringEngine(weights={self.weights}, thresholds={self.thresholds})"
