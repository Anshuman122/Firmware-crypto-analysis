"""
Simple API key auth middleware for FastAPI
"""

from fastapi import Header, HTTPException


async def require_api_key(x_api_key: str = Header(default="", alias="X-API-Key")):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing API key")
    # Placeholder validation
    if x_api_key != "dev-key":
        raise HTTPException(status_code=403, detail="Invalid API key")


