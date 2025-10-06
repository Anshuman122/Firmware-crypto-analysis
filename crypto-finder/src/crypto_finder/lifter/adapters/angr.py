"""
Angr adapter for lifting/analyzing binaries (stubbed if angr not installed)
"""

from pathlib import Path
from typing import List, Dict

from crypto_finder.common.logging import log


class AngrAdapter:
    def __init__(self):
        try:
            import angr  # noqa: F401
            self.available = True
        except Exception:
            self.available = False

    def list_functions(self, binary_path: Path) -> List[Dict]:
        if not self.available:
            log.warning("angr not available; returning empty function list")
            return []
        try:
            import angr
            proj = angr.Project(str(binary_path), auto_load_libs=False)
            cfg = proj.analyses.CFGFast()
            funcs = []
            for f in cfg.kb.functions.values():
                funcs.append({
                    'name': f.name,
                    'address': f.addr,
                    'size': getattr(f, 'size', 0) or 0,
                })
            return funcs
        except Exception as e:
            log.error(f"angr analysis failed: {e}")
            return []


