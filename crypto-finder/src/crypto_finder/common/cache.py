"""
Lightweight caching utilities

- In-memory LRU cache decorator
- File-based cache for expensive computations
"""

import functools
import hashlib
import json
from pathlib import Path
from typing import Any, Callable, Optional

CACHE_DIR = Path(".cache/crypto_finder")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _hash_key(*args: Any, **kwargs: Any) -> str:
    raw = json.dumps([args, sorted(kwargs.items())], default=str, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()


def file_cache(namespace: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Cache function results on disk using args as a key.
    """
    ns_dir = CACHE_DIR / namespace
    ns_dir.mkdir(parents=True, exist_ok=True)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = _hash_key(*args, **kwargs)
            fp = ns_dir / f"{key}.json"
            if fp.exists():
                try:
                    return json.loads(fp.read_text())
                except Exception:
                    pass
            result = func(*args, **kwargs)
            try:
                fp.write_text(json.dumps(result, default=str))
            except Exception:
                pass
            return result
        return wrapper
    return decorator


def lru_cache(maxsize: int = 128) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    return functools.lru_cache(maxsize=maxsize)
