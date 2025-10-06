"""
Semantic features (e.g., opcode patterns, calling conventions)
"""

from typing import Dict


def placeholder_semantic_features(function_bytes: bytes) -> Dict[str, float]:
    # Placeholder until disassembly features are integrated
    return {
        'semantic_placeholder': 1.0 if function_bytes else 0.0
    }
