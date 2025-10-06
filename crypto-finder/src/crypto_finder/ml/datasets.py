# Hinglish: Yeh file PyTorch ke liye ek custom Dataset banati hai.
# Yeh hamare JSON files ko read karti hai, features extract karti hai, aur training ke liye data taiyar karti hai.

import torch
from torch.utils.data import Dataset
from pathlib import Path
import json
import pandas as pd
from typing import List, Tuple

from crypto_finder.common.logging import log
from crypto_finder.ml.features import extract_features_from_function

class CryptoFuncDataset(Dataset):
    """Lifted functions ke JSON data se features aur labels load karne ke liye Dataset."""

    def __init__(self, data_dir: Path, annotations_file: Path):
        """
        Dataset ko initialize karta hai.
        :param data_dir: JSON files wali directory.
        :param annotations_file: Ek CSV file jisme (filename, label) ho.
        """
        self.data_dir = data_dir
        # CSV file ko read karo
        try:
            self.annotations = pd.read_csv(annotations_file)
        except FileNotFoundError:
            log.error(f"Annotations file not found: {annotations_file}")
            raise
        
        self.samples: List[Tuple[Dict, int]] = []
        self._load_data()

    def _load_data(self):
        """
        Saare JSON files se functions ko load karke samples banata hai.
        """
        log.info("Dataset load ho raha hai...")
        for idx, row in self.annotations.iterrows():
            json_filename = row['filename']
            label_str = row['label'] # e.g., "crypto" or "non-crypto"
            
            # Label ko integer me convert karo (0 for non-crypto, 1 for crypto)
            label = 1 if label_str == "crypto" else 0
            
            json_path = self.data_dir / json_filename
            if not json_path.exists():
                log.warning(f"JSON file not found, skipping: {json_path}")
                continue
            
            with open(json_path, 'r') as f:
                data = json.load(f)
                for func in data.get("functions", []):
                    self.samples.append((func, label))
        
        log.success(f"Dataset successfully load ho gaya. Total functions: {len(self.samples)}")

    def __len__(self) -> int:
        """Dataset me total samples (functions) ka count return karta hai."""
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """Ek single sample (feature vector aur label) return karta hai."""
        func_data, label = self.samples[idx]
        
        # Function data se feature vector banao
        features = extract_features_from_function(func_data)
        
        # NumPy array ko PyTorch tensors me convert karo
        feature_tensor = torch.from_numpy(features)
        label_tensor = torch.tensor(label, dtype=torch.long)
        
        return feature_tensor, label_tensor