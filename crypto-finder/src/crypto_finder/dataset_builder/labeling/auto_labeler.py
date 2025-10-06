"""
Automatic labeling system for dataset creation

Assigns labels to extracted functions based on:
- Function name (from compilation metadata)
- Source file location
- Parent library
"""

from pathlib import Path
from typing import Dict, List, Optional
import json

from crypto_finder.common.logging import setup_logging

logger = setup_logging(__name__)


class AutoLabeler:
    """
    Automatically labels functions for training dataset
    """
    
    # Algorithm categories
    ALGORITHM_MAP = {
        # Symmetric encryption
        'aes': 'AES',
        'des': 'DES',
        '3des': '3DES',
        'chacha': 'ChaCha20',
        'blowfish': 'Blowfish',
        'twofish': 'Twofish',
        
        # Asymmetric encryption
        'rsa': 'RSA',
        'dsa': 'DSA',
        'dh': 'DH',
        'ecdh': 'ECDH',
        'ecdsa': 'ECDSA',
        'ecc': 'ECC',
        
        # Hash functions
        'sha1': 'SHA-1',
        'sha224': 'SHA-224',
        'sha256': 'SHA-256',
        'sha384': 'SHA-384',
        'sha512': 'SHA-512',
        'sha3': 'SHA-3',
        'md5': 'MD5',
        'blake': 'BLAKE',
        
        # MAC
        'hmac': 'HMAC',
        'cmac': 'CMAC',
        'gmac': 'GMAC',
        
        # Key derivation
        'pbkdf2': 'PBKDF2',
        'hkdf': 'HKDF',
        'scrypt': 'Scrypt',
    }
    
    def __init__(self, compilation_metadata: Optional[str] = None):
        """
        Initialize auto-labeler
        
        Args:
            compilation_metadata: Path to compilation metadata JSON
        """
        self.metadata: Dict = {}
        
        if compilation_metadata and Path(compilation_metadata).exists():
            with open(compilation_metadata, 'r') as f:
                self.metadata = json.load(f)
    
    def label_function(
        self,
        binary_path: str,
        function_info: Dict
    ) -> Dict:
        """
        Assign label to a function
        
        Args:
            binary_path: Path to binary containing function
            function_info: Function metadata dict
        
        Returns:
            Function info with added 'label' field
        """
        # Extract metadata from binary filename
        # Format: library_function_arch_opt.bin
        binary_name = Path(binary_path).stem
        parts = binary_name.split('_')
        
        if len(parts) >= 4:
            library = parts[0]
            func_name = parts[1]
            architecture = parts[2]
            optimization = parts[3]
            
            # Determine algorithm
            algorithm = self._detect_algorithm(func_name)
            
            function_info['label'] = {
                'algorithm': algorithm,
                'library': library,
                'architecture': architecture,
                'optimization': optimization,
                'function_name': func_name,
                'is_crypto': True
            }
        else:
            # Unknown format
            function_info['label'] = {
                'algorithm': 'Unknown',
                'is_crypto': False
            }
        
        return function_info
    
    def _detect_algorithm(self, function_name: str) -> str:
        """
        Detect crypto algorithm from function name
        
        Args:
            function_name: Name of the function
        
        Returns:
            Algorithm name or 'Unknown'
        """
        func_lower = function_name.lower()
        
        for key, value in self.ALGORITHM_MAP.items():
            if key in func_lower:
                return value
        
        return 'Unknown'
    
    def label_batch(
        self,
        functions: List[Dict],
        binary_path: str
    ) -> List[Dict]:
        """
        Label multiple functions from same binary
        
        Args:
            functions: List of function dicts
            binary_path: Path to source binary
        
        Returns:
            Labeled functions
        """
        return [self.label_function(binary_path, func.copy()) for func in functions]


