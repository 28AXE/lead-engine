"""Cache manager for API responses and enrichment data."""

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Optional


class CacheManager:
    """JSON cache with TTL support for API responses."""

    def __init__(self, cache_dir: str | Path = ".cache", ttl_hours: int = 24, enabled: bool = True, dry_run: bool = False):
        self.cache_dir = Path(cache_dir)
        self.ttl_seconds = ttl_hours * 3600
        self.enabled = enabled and not dry_run
        self.dry_run = dry_run

        if self.enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _make_key(self, params: Any) -> str:
        """Generate MD5 hash from parameters as cache key."""
        params_str = json.dumps(params, sort_keys=True, default=str)
        return hashlib.md5(params_str.encode()).hexdigest()

    def _get_cache_path(self, key: str) -> Path:
        """Get path to cache file for given key."""
        return self.cache_dir / f"{key}.json"

    def _is_expired(self, cache_file: Path) -> bool:
        """Check if cache file has expired based on TTL."""
        if not cache_file.exists():
            return True

        mtime = cache_file.stat().st_mtime
        age = time.time() - mtime
        return age > self.ttl_seconds

    def get(self, key: str | Any) -> Optional[Any]:
        """Get cached data by key or parameters."""
        if not self.enabled:
            return None

        cache_key = key if isinstance(key, str) else self._make_key(key)
        cache_file = self._get_cache_path(cache_key)

        if self._is_expired(cache_file):
            cache_file.unlink(missing_ok=True)
            return None

        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("value")
        except (json.JSONDecodeError, IOError):
            return None

    def set(self, key: str | Any, data: Any) -> None:
        """Store data in cache with current timestamp."""
        if not self.enabled:
            return

        cache_key = key if isinstance(key, str) else self._make_key(key)
        cache_file = self._get_cache_path(cache_key)

        cache_data = {
            "value": data,
            "timestamp": time.time(),
        }

        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=2, default=str)

    def clear_expired(self) -> int:
        """Remove all expired cache files. Returns count of removed files."""
        if not self.cache_dir.exists():
            return 0

        removed = 0
        for cache_file in self.cache_dir.glob("*.json"):
            if self._is_expired(cache_file):
                cache_file.unlink()
                removed += 1

        return removed

    def clear_all(self) -> int:
        """Remove all cache files. Returns count of removed files."""
        if not self.cache_dir.exists():
            return 0

        removed = 0
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
            removed += 1

        return removed

    def stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        if not self.cache_dir.exists():
            return {"files": 0, "total_size_bytes": 0}

        files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in files)

        return {
            "files": len(files),
            "total_size_bytes": total_size,
            "enabled": self.enabled,
            "dry_run": self.dry_run,
            "ttl_hours": self.ttl_seconds // 3600,
        }

    def __repr__(self) -> str:
        mode = "dry_run" if self.dry_run else ("enabled" if self.enabled else "disabled")
        return f"CacheManager(mode={mode}, ttl={self.ttl_seconds // 3600}h, dir={self.cache_dir})"
