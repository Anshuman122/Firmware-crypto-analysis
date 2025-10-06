"""
Basic triage utilities for extracted firmware content
"""

from pathlib import Path
from typing import Dict, List


def group_by_directory(binaries: List[Dict]) -> Dict[str, List[Dict]]:
    groups: Dict[str, List[Dict]] = {}
    for b in binaries:
        parent = str(Path(b['path']).parent)
        groups.setdefault(parent, []).append(b)
    return groups


def top_n_largest(binaries: List[Dict], n: int = 50) -> List[Dict]:
    return sorted(binaries, key=lambda x: x.get('size', 0), reverse=True)[:n]
