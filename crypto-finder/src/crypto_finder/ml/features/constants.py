"""
Constant-based features (e.g., S-boxes, IVs) presence indicators
"""

from typing import Dict

WELL_KNOWN_CONSTANTS = {
    'aes_sbox_head': bytes([0x63, 0x7c, 0x77, 0x7b]),
    'md5_iv': bytes.fromhex('67452301efcdab8998badcfe10325476'),
}


def constant_hits(data: bytes) -> Dict[str, int]:
    hits: Dict[str, int] = {}
    for name, pattern in WELL_KNOWN_CONSTANTS.items():
        hits[f'const_{name}'] = int(pattern in data)
    return hits
