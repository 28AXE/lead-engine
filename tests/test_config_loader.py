"""Unit tests for configuration loading."""

import pytest
import tempfile
import os
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.config_loader import ConfigLoader, ConfigError


VALID_CONFIG = """
vertical: "test_vertical"
description: "Test vertical for unit tests"
dry_run: true

geo:
  - "FR"
  - "BE"

keywords:
  - "test"
  - "demo"

signals:
  - vibe_api
  - pappers

scoring_weights:
  domain_age: 10
  ad_activity: 9
  budget_signal: 9
  vertical_fit: 12

scoring_thresholds:
  hot: 30
  warm: 22
  cold: 15

outreach:
  tone: "professional"
  value_prop: "test value"

notifications:
  slack_webhook: ""
  discord_webhook: ""
  notify_on: ["HOT"]

cache:
  enabled: true
  ttl_hours: 24
"""


def test_valid_yaml_loads():
    """Test that a valid YAML config loads successfully."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(VALID_CONFIG)
        f.flush()

        config = ConfigLoader(f.name)

        assert config.vertical == "test_vertical"
        assert config.description == "Test vertical for unit tests"
        assert config.dry_run is True
        assert "FR" in config.geo
        assert "test" in config.keywords
        assert "vibe_api" in config.signals
        assert config.scoring_weights["domain_age"] == 10
        assert config.scoring_thresholds["hot"] == 30

        os.unlink(f.name)


def test_missing_required_field():
    """Test that missing required fields raise ConfigError."""
    invalid_config = """
vertical: "incomplete"
description: "Missing fields"
geo:
  - "FR"
keywords:
  - "test"
signals:
  - vibe_api
"""
    # Missing: scoring_weights, scoring_thresholds, outreach, notifications, cache

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(invalid_config)
        f.flush()

        with pytest.raises(ConfigError) as exc_info:
            ConfigLoader(f.name)

        assert "Missing required configuration fields" in str(exc_info.value)

        os.unlink(f.name)


def test_missing_scoring_weights():
    """Test that missing scoring weights raise ConfigError."""
    invalid_config = """
vertical: "test"
description: "Test"
geo: ["FR"]
keywords: ["test"]
signals: ["vibe_api"]
scoring_weights:
  domain_age: 10
  # Missing: ad_activity, budget_signal, vertical_fit
scoring_thresholds:
  hot: 30
  warm: 22
  cold: 15
outreach:
  tone: "test"
  value_prop: "test"
notifications:
  slack_webhook: ""
  discord_webhook: ""
  notify_on: ["HOT"]
cache:
  enabled: true
  ttl_hours: 24
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(invalid_config)
        f.flush()

        with pytest.raises(ConfigError) as exc_info:
            ConfigLoader(f.name)

        assert "Missing scoring weights" in str(exc_info.value)

        os.unlink(f.name)


def test_missing_thresholds():
    """Test that missing scoring thresholds raise ConfigError."""
    invalid_config = """
vertical: "test"
description: "Test"
geo: ["FR"]
keywords: ["test"]
signals: ["vibe_api"]
scoring_weights:
  domain_age: 10
  ad_activity: 9
  budget_signal: 9
  vertical_fit: 12
scoring_thresholds:
  hot: 30
  # Missing: warm, cold
outreach:
  tone: "test"
  value_prop: "test"
notifications:
  slack_webhook: ""
  discord_webhook: ""
  notify_on: ["HOT"]
cache:
  enabled: true
  ttl_hours: 24
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(invalid_config)
        f.flush()

        with pytest.raises(ConfigError) as exc_info:
            ConfigLoader(f.name)

        assert "Missing scoring thresholds" in str(exc_info.value)

        os.unlink(f.name)


def test_is_signal_enabled():
    """Test the is_signal_enabled method."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(VALID_CONFIG)
        f.flush()

        config = ConfigLoader(f.name)

        assert config.is_signal_enabled("vibe_api") is True
        assert config.is_signal_enabled("pappers") is True
        assert config.is_signal_enabled("google_maps") is False
        assert config.is_signal_enabled("nonexistent_signal") is False

        os.unlink(f.name)


def test_config_file_not_found():
    """Test that non-existent config file raises ConfigError."""
    with pytest.raises(ConfigError) as exc_info:
        ConfigLoader("/nonexistent/path/config.yaml")

    assert "Configuration file not found" in str(exc_info.value)


def test_empty_config_file():
    """Test that empty config file raises ConfigError."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("")
        f.flush()

        with pytest.raises(ConfigError) as exc_info:
            ConfigLoader(f.name)

        assert "empty" in str(exc_info.value).lower()

        os.unlink(f.name)


def test_cache_properties():
    """Test cache-related property accessors."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(VALID_CONFIG)
        f.flush()

        config = ConfigLoader(f.name)

        assert config.cache_enabled is True
        assert config.cache_ttl_hours == 24

        os.unlink(f.name)
