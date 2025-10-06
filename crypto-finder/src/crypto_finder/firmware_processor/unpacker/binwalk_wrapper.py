"""
Firmware unpacking using binwalk

Extracts filesystem and binaries from firmware images
"""

import subprocess
import shutil
from pathlib import Path
from typing import Optional, List
import tempfile

from crypto_finder.common.logging import setup_logging
from crypto_finder.common.exceptions import FirmwareExtractionError

logger = setup_logging(__name__)


class FirmwareUnpacker:
    """
    Unpacks firmware images using binwalk
    """
    
    def __init__(self, firmware_path: str):
        """
        Initialize unpacker
        
        Args:
            firmware_path: Path to firmware image
        """
        self.firmware_path = Path(firmware_path)
        
        if not self.firmware_path.exists():
            raise FileNotFoundError(f"Firmware not found: {firmware_path}")
        
        # Check if binwalk is available
        if not shutil.which('binwalk'):
            raise FirmwareExtractionError("binwalk not installed. Install with: sudo apt install binwalk")
        
        self.extracted_dir: Optional[Path] = None
    
    def unpack(self, output_dir: Optional[str] = None) -> str:
        """
        Unpack firmware image
        
        Args:
            output_dir: Optional output directory; defaults to a temporary directory if not provided
        
        Returns:
            Path to extracted directory
        """
        if output_dir is None:
            tempdir = tempfile.mkdtemp(prefix="firmware_extract_")
            output_path = Path(tempdir)
        else:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
        
        # Run binwalk extraction
        cmd = [
            'binwalk', '-e', '--dd=.*,"firmware.bin"',
            '-C', str(output_path),
            str(self.firmware_path)
        ]
        logger.info(f"Running binwalk: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
            if result.returncode != 0:
                logger.error(result.stderr)
                raise FirmwareExtractionError("Binwalk extraction failed")
        except subprocess.TimeoutExpired:
            raise FirmwareExtractionError("Binwalk extraction timed out")
        
        # Locate likely extraction directory created by binwalk
        extracted_candidates: List[Path] = list(output_path.glob("**/*_extracted"))
        if not extracted_candidates:
            # Fallback: if binwalk created files directly
            extracted_candidates = [output_path]
        
        self.extracted_dir = extracted_candidates[0]
        logger.info(f"Firmware extracted to: {self.extracted_dir}")
        return str(self.extracted_dir)
