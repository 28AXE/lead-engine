"""Pipeline tracker for managing leads through outreach stages."""

import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Optional


VALID_STATUSES = ["sourced", "enriched", "scored", "contacted", "replied"]


class PipelineTracker:
    """Tracks leads through outreach pipeline stages."""

    def __init__(self, db_path: str | Path = "outputs/leads_db.json"):
        self.db_path = Path(db_path)
        self._leads: dict[str, dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        """Load leads from JSON file if it exists."""
        if self.db_path.exists():
            with open(self.db_path, "r", encoding="utf-8") as f:
                self._leads = json.load(f)

    def _save(self) -> None:
        """Persist leads to JSON file."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self._leads, f, indent=2, default=str)

    def _make_lead_id(self, lead: dict[str, Any]) -> str:
        """Generate unique ID from domain + email hash."""
        domain = lead.get("domain", "").lower().strip()
        email = lead.get("email", "").lower().strip()
        key = f"{domain}:{email}"
        return hashlib.md5(key.encode()).hexdigest()

    def add_lead(self, lead: dict[str, Any]) -> tuple[bool, str]:
        """
        Add a lead to the pipeline.
        Returns (success, message) - False if duplicate.
        """
        lead_id = self._make_lead_id(lead)

        if lead_id in self._leads:
            return (False, f"Duplicate lead: {lead.get('domain', 'unknown')}")

        lead["_id"] = lead_id
        lead["_status"] = "sourced"
        lead["_created_at"] = self._get_timestamp()

        self._leads[lead_id] = lead
        self._save()

        return (True, f"Lead added: {lead.get('domain', 'unknown')}")

    def update_status(self, lead_id: str, new_status: str) -> tuple[bool, str]:
        """
        Update lead status.
        Returns (success, message).
        """
        if new_status not in VALID_STATUSES:
            return (False, f"Invalid status: {new_status}. Valid: {VALID_STATUSES}")

        if lead_id not in self._leads:
            return (False, f"Lead not found: {lead_id}")

        old_status = self._leads[lead_id]["_status"]
        self._leads[lead_id]["_status"] = new_status
        self._leads[lead_id]["_updated_at"] = self._get_timestamp()
        self._save()

        return (True, f"Status updated: {old_status} → {new_status}")

    def get_by_status(self, status: str) -> list[dict[str, Any]]:
        """Get all leads with a specific status."""
        if status not in VALID_STATUSES:
            return []

        return [
            lead for lead in self._leads.values()
            if lead.get("_status") == status
        ]

    def get_all(self) -> list[dict[str, Any]]:
        """Get all leads in the pipeline."""
        return list(self._leads.values())

    def get_by_id(self, lead_id: str) -> Optional[dict[str, Any]]:
        """Get a specific lead by ID."""
        return self._leads.get(lead_id)

    def delete_lead(self, lead_id: str) -> tuple[bool, str]:
        """Remove a lead from the pipeline."""
        if lead_id not in self._leads:
            return (False, f"Lead not found: {lead_id}")

        del self._leads[lead_id]
        self._save()

        return (True, f"Lead deleted: {lead_id}")

    def export_csv(self, filepath: str | Path) -> int:
        """
        Export all leads to CSV.
        Returns count of exported rows.
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        leads = self.get_all()
        if not leads:
            return 0

        all_keys = set()
        for lead in leads:
            all_keys.update(lead.keys())

        fieldnames = sorted(all_keys)

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(leads)

        return len(leads)

    def stats(self) -> dict[str, Any]:
        """Get pipeline statistics."""
        leads = self.get_all()
        status_counts = {status: 0 for status in VALID_STATUSES}

        for lead in leads:
            status = lead.get("_status", "sourced")
            if status in status_counts:
                status_counts[status] += 1

        return {
            "total_leads": len(leads),
            "by_status": status_counts,
            "hot_leads": sum(1 for l in leads if l.get("verdict") == "HOT"),
            "warm_leads": sum(1 for l in leads if l.get("verdict") == "WARM"),
        }

    def clear_all(self) -> int:
        """Remove all leads. Returns count of removed leads."""
        count = len(self._leads)
        self._leads = {}
        self._save()
        return count

    @staticmethod
    def _get_timestamp() -> str:
        """Get current ISO timestamp."""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()

    def __len__(self) -> int:
        return len(self._leads)

    def __repr__(self) -> str:
        stats = self.stats()
        return f"PipelineTracker(total={stats['total_leads']}, db={self.db_path})"
