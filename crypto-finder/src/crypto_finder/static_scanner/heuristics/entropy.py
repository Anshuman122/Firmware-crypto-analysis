"""
Entropy heuristic: flag high-entropy regions likely to be keys/ciphertext
"""

import math
from typing import List, Tuple


def window_entropy(data: bytes, window: int = 256, step: int = 64, threshold: float = 7.5) -> List[Tuple[int, float]]:
    hits: List[Tuple[int, float]] = []
    n = len(data)
    for start in range(0, max(0, n - window + 1), step):
        chunk = data[start:start+window]
        freq = [0] * 256
        for b in chunk:
            freq[b] += 1
        ent = 0.0
        for c in freq:
            if c == 0:
                continue
            p = c / window
            ent -= p * math.log2(p)
        if ent >= threshold:
            hits.append((start, ent))
    return hits


