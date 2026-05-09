"""Webhook notifier for sending leads to external systems."""

import json
import logging
from typing import Any, Optional

import requests

from ..core.config_loader import ConfigLoader


logger = logging.getLogger(__name__)


class WebhookNotifier:
    """Sends lead notifications to Slack and Discord webhooks."""

    def __init__(self, config: ConfigLoader):
        self.config = config
        self.notify_on = config.notifications.get("notify_on", ["HOT"])
        self.slack_webhook = config.notifications.get("slack_webhook", "")
        self.discord_webhook = config.notifications.get("discord_webhook", "")

    def should_notify(self, verdict: str) -> bool:
        """Check if this verdict should trigger a notification."""
        return verdict in self.notify_on

    def notify(self, lead: dict[str, Any]) -> dict[str, bool]:
        """
        Send notification for a lead to configured webhooks.
        Returns {slack: success, discord: success}.
        Silently handles errors to never block the pipeline.
        """
        verdict = lead.get("verdict", "COLD")

        if not self.should_notify(verdict):
            return {"slack": False, "discord": False}

        results = {"slack": False, "discord": False}

        if self.slack_webhook:
            results["slack"] = self._send_slack(lead)

        if self.discord_webhook:
            results["discord"] = self._send_discord(lead)

        return results

    def _send_slack(self, lead: dict[str, Any]) -> bool:
        """Send formatted message to Slack webhook."""
        verdict = lead.get("verdict", "COLD")
        score = lead.get("score", 0)
        signals = lead.get("signals", [])

        color = {
            "HOT": "#e74c3c",
            "WARM": "#f39c12",
            "COLD": "#3498db",
        }.get(verdict, "#95a5a6")

        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{'🔥' if verdict == 'HOT' else '🟡'} Nouveau lead {verdict}",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Nom:*\n{lead.get('name', 'N/A')}"},
                    {"type": "mrkdwn", "text": f"*Domaine:*\n{lead.get('domain', 'N/A')}"},
                    {"type": "mrkdwn", "text": f"*Score:*\n{score}/40"},
                    {"type": "mrkdwn", "text": f"*Email:*\n{lead.get('email', '-')}"},
                ],
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Signaux détectés:*\n{', '.join(signals) if signals else 'Aucun'}",
                },
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": "Powered by Lead Engine",
                        "emoji": True,
                    }
                ],
            },
        ]

        payload = {"blocks": blocks}

        try:
            response = requests.post(
                self.slack_webhook,
                json=payload,
                timeout=10,
            )
            return response.status_code == 200
        except requests.RequestException as e:
            logger.warning(f"Slack notification failed: {e}")
            return False

    def _send_discord(self, lead: dict[str, Any]) -> bool:
        """Send embed message to Discord webhook."""
        verdict = lead.get("verdict", "COLD")
        score = lead.get("score", 0)
        signals = lead.get("signals", [])

        color = {
            "HOT": 14835708,  # #e74c3c
            "WARM": 15938354,  # #f39c12
            "COLD": 3447003,  # #3498db
        }.get(verdict, 9807270)

        embed = {
            "title": f"{'🔥' if verdict == 'HOT' else '🟡'} Nouveau lead {verdict}",
            "color": color,
            "fields": [
                {"name": "Nom", "value": lead.get("name", "N/A"), "inline": True},
                {"name": "Domaine", "value": lead.get("domain", "N/A"), "inline": True},
                {"name": "Score", "value": f"{score}/40", "inline": True},
                {"name": "Email", "value": lead.get("email", "-"), "inline": True},
                {"name": "Signaux", "value": ", ".join(signals) if signals else "Aucun", "inline": False},
            ],
            "footer": {"text": "Powered by Lead Engine"},
        }

        payload = {"embeds": [embed]}

        try:
            response = requests.post(
                self.discord_webhook,
                json=payload,
                timeout=10,
            )
            return response.status_code in (200, 204)
        except requests.RequestException as e:
            logger.warning(f"Discord notification failed: {e}")
            return False

    def test_connection(self) -> dict[str, bool]:
        """Test webhook connections with a sample message."""
        test_lead = {
            "name": "Test Lead",
            "domain": "test.example.com",
            "score": 35,
            "verdict": "HOT",
            "email": "test@example.com",
            "signals": ["google_maps", "pappers"],
        }

        return self.notify(test_lead)
