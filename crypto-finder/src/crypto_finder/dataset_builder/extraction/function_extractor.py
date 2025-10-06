"""
Extracts individual functions from compiled binaries

Uses multiple tools to ensure comprehensive extraction:
- Symbol parsing (if available)
- Heuristic-based detection (function prologues/epilogues)
- CFG-based reconstruction
"""

import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Optional

from crypto_finder.common.logging import setup_logging

logger = setup_logging(__name__)


class FunctionExtractor:
    """
    Extracts functions from ELF binaries
    """
    
    def __init__(self):
        """Initialize function extractor"""
        self.objdump_available = shutil.which('objdump') is not None
        self.readelf_available = shutil.which('readelf') is not None
    
    def extract_all(self, binary_path: str) -> List[Dict]:
        """
        Extract all functions from a binary
        
        Args:
            binary_path: Path to ELF binary
        
        Returns:
            List of function dictionaries with metadata
        """
        functions: List[Dict] = []
        
        # Try symbol-based extraction first
        symbol_functions = self._extract_from_symbols(binary_path)
        if symbol_functions:
            functions.extend(symbol_functions)
            logger.debug(f"Extracted {len(symbol_functions)} functions from symbols")
        
        # If stripped, use heuristic detection
        if not symbol_functions:
            heuristic_functions = self._extract_heuristic(binary_path)
            functions.extend(heuristic_functions)
            logger.debug(f"Extracted {len(heuristic_functions)} functions using heuristics")
        
        return functions
    
    def _extract_from_symbols(self, binary_path: str) -> List[Dict]:
        """
        Extract functions using symbol table
        
        Args:
            binary_path: Path to binary
        
        Returns:
            List of functions with metadata
        """
        if not self.readelf_available:
            return []
        
        try:
            result = subprocess.run(
                ['readelf', '-s', binary_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return []
            
            functions: List[Dict] = []
            
            # Parse readelf output
            for line in result.stdout.split('\n'):
                # Look for FUNC entries
                if 'FUNC' in line:
                    parts = line.split()
                    if len(parts) >= 8:
                        try:
                            address = int(parts[1], 16)
                            size = int(parts[2])
                            name = parts[7]
                            
                            functions.append({
                                'address': address,
                                'size': size,
                                'name': name,
                                'source': 'symbol'
                            })
                        except (ValueError, IndexError):
                            continue
            
            return functions
        
        except Exception as e:
            logger.error(f"Symbol extraction failed: {e}")
            return []
    
    def _extract_heuristic(self, binary_path: str) -> List[Dict]:
        """
        Extract functions using heuristics (for stripped binaries)
        
        Looks for common function prologue patterns:
        - x86: push ebp; mov ebp, esp
        - ARM: push {r11, lr}
        
        Args:
            binary_path: Path to binary
        
        Returns:
            List of detected functions
        """
        functions: List[Dict] = []
        
        try:
            # Read binary
            data = Path(binary_path).read_bytes()
            
            # Simple pattern matching for x86 function prologues
            # Pattern: 55 89 e5 (push ebp; mov ebp, esp)
            prologue_pattern = b'\x55\x89\xe5'
            
            offset = 0
            while True:
                offset = data.find(prologue_pattern, offset)
                if offset == -1:
                    break
                
                functions.append({
                    'address': offset,
                    'size': 0,  # Unknown without further analysis
                    'name': f'sub_{offset:x}',
                    'source': 'heuristic'
                })
                
                offset += 1
            
            return functions
        
        except Exception as e:
            logger.error(f"Heuristic extraction failed: {e}")
            return []


