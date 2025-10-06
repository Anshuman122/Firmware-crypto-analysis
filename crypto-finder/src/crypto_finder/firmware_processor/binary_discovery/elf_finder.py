"""
ELF binary discovery within extracted firmware trees
"""

import os
import stat
from pathlib import Path
from typing import List, Dict

from crypto_finder.common.logging import setup_logging

logger = setup_logging(__name__)


def _is_elf(file_path: Path) -> bool:
    try:
        with open(file_path, 'rb') as f:
            magic = f.read(4)
            return magic == b"\x7fELF"
    except Exception:
        return False


class ElfFinder:
    """
    Recursively find ELF binaries under a directory
    """

    def __init__(self, root_dir: str):
        self.root = Path(root_dir)

    def find_all(self) -> List[Dict]:
        results: List[Dict] = []
        for dirpath, _, filenames in os.walk(self.root):
            for name in filenames:
                p = Path(dirpath) / name
                try:
                    if _is_elf(p):
                        st = p.stat()
                        is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
                        results.append({
                            'path': str(p),
                            'size': st.st_size,
                            'executable': is_executable,
                        })
                except Exception:
                    continue
        logger.info(f"Discovered {len(results)} ELF binaries under {self.root}")
        return results
