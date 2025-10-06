"""
Structural features such as size and simple heuristics
"""

from typing import Dict


def basic_structural_features(function_bytes: bytes) -> Dict[str, float]:
    length = len(function_bytes)
    return {
        'size_bytes': float(length),
        'is_tiny': float(length < 32),
        'is_large': float(length > 4096),
    }
