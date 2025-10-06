"""
Neural embeddings utilities placeholder
"""

from typing import Dict


def byte_ngram_embedding(function_bytes: bytes, n: int = 2) -> Dict[str, float]:
    # Simple n-gram counts normalized
    if not function_bytes:
        return {}
    counts: Dict[bytes, int] = {}
    for i in range(len(function_bytes) - n + 1):
        g = function_bytes[i:i+n]
        counts[g] = counts.get(g, 0) + 1
    total = sum(counts.values()) or 1
    return {f"ng_{g.hex()}": c / total for g, c in counts.items()}
