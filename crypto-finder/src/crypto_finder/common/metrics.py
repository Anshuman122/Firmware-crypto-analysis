"""
Common metrics helpers
"""

from typing import Dict, List


def classification_report(counts: Dict[str, int]) -> str:
    total = sum(counts.values()) or 1
    lines: List[str] = ["Metric\tCount\tPct"]
    for k, v in counts.items():
        pct = 100.0 * v / total
        lines.append(f"{k}\t{v}\t{pct:.2f}%")
    lines.append(f"TOTAL\t{total}\t100.00%")
    return "\n".join(lines)


