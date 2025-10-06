"""
Loop detection heuristic placeholder
"""

from typing import List, Dict


def detect_simple_loops(opcodes: List[int]) -> List[Dict]:
    # Placeholder: detect back-edges in a fake linear CFG using jumps
    loops: List[Dict] = []
    for i, op in enumerate(opcodes):
        if op == 0xE9:  # x86 jmp rel32 (placeholder)
            # Fake a loop
            loops.append({'at': i, 'type': 'backedge'})
    return loops


