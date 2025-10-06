"""
Naive in-memory rate limiter dependency
"""

import time
from typing import Dict
from fastapi import HTTPException


_BUCKETS: Dict[str, float] = {}


async def rate_limit(client_id: str = "global", interval_s: float = 0.2):
    now = time.time()
    last = _BUCKETS.get(client_id, 0.0)
    if now - last < interval_s:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    _BUCKETS[client_id] = now


