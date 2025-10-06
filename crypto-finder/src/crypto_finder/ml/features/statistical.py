"""
Statistical features for function representations
"""

from typing import List, Dict
import math


def compute_byte_histogram(data: bytes, num_bins: int = 16) -> List[float]:
    bin_size = 256 // num_bins
    counts = [0] * num_bins
    for b in data:
        counts[b // bin_size] += 1
    total = len(data) or 1
    return [c / total for c in counts]


def shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    freq = [0] * 256
    for b in data:
        freq[b] += 1
    total = len(data)
    entropy = 0.0
    for c in freq:
        if c == 0:
            continue
        p = c / total
        entropy -= p * math.log2(p)
    return entropy


def summarize_bytes(data: bytes) -> Dict[str, float]:
    return {
        'len': float(len(data)),
        'mean': float(sum(data) / (len(data) or 1)),
        'entropy': shannon_entropy(data),
    }
