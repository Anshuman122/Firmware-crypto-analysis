"""
Manages downloading and organizing crypto library source code
"""

import requests
import tarfile
import zipfile
from pathlib import Path
from typing import Optional
import shutil

from crypto_finder.common.logging import setup_logging

logger = setup_logging(__name__)


class LibraryManager:
    """
    Downloads and manages crypto library source code
    """
    
    def __init__(self, sources_dir: str = "sources"):
        """
        Initialize library manager
        
        Args:
            sources_dir: Directory to store source code
        """
        self.sources_dir = Path(sources_dir)
        self.sources_dir.mkdir(parents=True, exist_ok=True)
    
    def get_library(
        self,
        name: str,
        version: Optional[str] = None,
        url: Optional[str] = None
    ) -> str:
        """
        Get crypto library source code (download if needed)
        
        Args:
            name: Library name
            version: Version string
            url: Download URL
        
        Returns:
            Path to extracted source directory
        """
        lib_dir = self.sources_dir / f"{name}-{version}" if version else self.sources_dir / name
        
        # Check if already downloaded
        if lib_dir.exists():
            logger.info(f"Library {name} already available at {lib_dir}")
            return str(lib_dir)
        
        # Download if URL provided
        if url:
            logger.info(f"Downloading {name} from {url}")
            archive_path = self._download_file(url)
            
            # Extract
            logger.info(f"Extracting {name}...")
            self._extract_archive(archive_path, lib_dir.parent)
            
            # Clean up archive
            archive_path.unlink()
            
            logger.info(f"✓ {name} ready at {lib_dir}")
            return str(lib_dir)
        
        else:
            raise ValueError(f"Library {name} not found and no URL provided")
    
    def _download_file(self, url: str) -> Path:
        """
        Download file from URL
        
        Args:
            url: URL to download from
        
        Returns:
            Path to downloaded file
        """
        filename = url.split('/')[-1]
        output_path = self.sources_dir / filename
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(output_path, 'wb') as f:
            if total_size == 0:
                f.write(response.content)
            else:
                from tqdm import tqdm
                with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        pbar.update(len(chunk))
        
        return output_path
    
    def _extract_archive(self, archive_path: Path, extract_to: Path):
        """
        Extract tar.gz or zip archive
        
        Args:
            archive_path: Path to archive
            extract_to: Where to extract
        """
        extract_to.mkdir(parents=True, exist_ok=True)
        
        if archive_path.suffix == '.gz' or archive_path.suffixes == ['.tar', '.gz']:
            with tarfile.open(archive_path, 'r:gz') as tar:
                tar.extractall(extract_to)
        
        elif archive_path.suffix == '.zip':
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
        
        else:
            raise ValueError(f"Unsupported archive format: {archive_path.suffix}")


