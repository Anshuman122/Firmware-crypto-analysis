"""
Model inference utilities
"""

from typing import Any, Dict, List


class CryptoDetector:
    def __init__(self, model_path: Any = None):
        self.model_path = model_path

    def detect_batch(self, functions: List[Dict]) -> List[Dict]:
        # Placeholder inference: mark all as non-crypto
        detections: List[Dict] = []
        for f in functions:
            detections.append({
                'function': f,
                'label': 'non-crypto',
                'confidence': 0.0,
            })
        return detections


