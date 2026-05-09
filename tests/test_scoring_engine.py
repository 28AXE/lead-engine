"""Unit tests for the 40-point scoring engine."""

import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.config_loader import ConfigLoader
from core.scoring_engine import ScoringEngine


@pytest.fixture
def config():
    """Load test configuration."""
    return ConfigLoader(Path(__file__).parent.parent / "config" / "vertical.config.yaml")


@pytest.fixture
def scoring(config):
    """Create scoring engine instance."""
    return ScoringEngine(config)


def test_score_hot_lead(scoring):
    """Test that a highly qualified lead scores as HOT."""
    lead = {
        "domain": "young-casino.com",
        "domain_age_days": 60,
        "meta_ad_count": 3,
        "influencer_count": 5,
        "running_google_ads": True,
        "funding_status": "seed",
        "employee_count": 25,
        "vertical": "casino",
        "keywords": ["online casino", "live dealer"],
    }

    result = scoring.score(lead)

    assert result["score"] >= scoring.thresholds["hot"]
    assert result["verdict"] == "HOT"
    assert "domain_age" in result["breakdown"]
    assert "ad_activity" in result["breakdown"]
    assert "budget_signal" in result["breakdown"]
    assert "vertical_fit" in result["breakdown"]


def test_score_warm_lead(scoring):
    """Test that a moderately qualified lead scores as WARM."""
    lead = {
        "domain": "established-plomberie.fr",
        "domain_age_days": 400,
        "meta_ad_count": 15,
        "influencer_count": 2,
        "running_google_ads": True,
        "funding_status": "",
        "employee_count": 15,
        "vertical": "plomberie",
        "keywords": ["plombier"],
    }

    result = scoring.score(lead)

    assert scoring.thresholds["warm"] <= result["score"] < scoring.thresholds["hot"]
    assert result["verdict"] == "WARM"


def test_score_cold_lead(scoring):
    """Test that a minimally qualified lead scores as COLD."""
    lead = {
        "domain": "old-business.com",
        "domain_age_days": 1500,
        "meta_ad_count": 60,
        "influencer_count": 0,
        "running_google_ads": False,
        "funding_status": "",
        "employee_count": 3,
        "vertical": "other",
        "keywords": ["unrelated"],
    }

    result = scoring.score(lead)

    assert scoring.thresholds["cold"] <= result["score"] < scoring.thresholds["warm"]
    assert result["verdict"] == "COLD"


def test_score_disqualified_lead(scoring):
    """Test that an unqualified lead is DISQUALIFIED."""
    lead = {
        "domain": "ancient-domain.com",
        "domain_age_days": 3000,
        "meta_ad_count": 100,
        "influencer_count": 0,
        "running_google_ads": False,
        "funding_status": "",
        "employee_count": 1,
        "vertical": "other",
        "keywords": ["unrelated"],
    }

    result = scoring.score(lead)

    assert result["score"] < scoring.thresholds["cold"]
    assert result["verdict"] == "DISQUALIFIED"


def test_batch_score_sorting(scoring):
    """Test that batch_score returns leads sorted by score descending."""
    leads = [
        {"domain": "cold.com", "domain_age_days": 2000, "meta_ad_count": 80,
         "influencer_count": 0, "running_google_ads": False, "vertical": "other", "keywords": []},
        {"domain": "hot.com", "domain_age_days": 50, "meta_ad_count": 2,
         "influencer_count": 5, "running_google_ads": True, "vertical": "casino", "keywords": ["casino"]},
        {"domain": "warm.com", "domain_age_days": 500, "meta_ad_count": 20,
         "influencer_count": 1, "running_google_ads": False, "vertical": "plomberie", "keywords": ["plombier"]},
    ]

    results = scoring.batch_score(leads)

    assert len(results) == 3
    assert results[0]["score"] >= results[1]["score"] >= results[2]["score"]
    assert results[0]["verdict"] == "HOT"


def test_dry_run_mode():
    """Test that dry run mode uses mock data without API calls."""
    # This test verifies the scoring engine works with mock data
    config = ConfigLoader(Path(__file__).parent.parent / "config" / "vertical.config.yaml")
    scoring = ScoringEngine(config)

    # Mock lead simulating dry_run output
    mock_lead = {
        "name": "Test Company",
        "domain": "test-company.fr",
        "domain_age_days": 180,
        "meta_ad_count": 5,
        "influencer_count": 2,
        "running_google_ads": True,
        "employee_count": 12,
        "vertical": "plomberie",
        "keywords": ["plombier"],
    }

    result = scoring.score(mock_lead)

    assert "score" in result
    assert "verdict" in result
    assert "breakdown" in result
    assert isinstance(result["score"], int)
    assert 0 <= result["score"] <= 40
