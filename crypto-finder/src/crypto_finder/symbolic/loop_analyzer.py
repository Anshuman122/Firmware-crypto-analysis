# Hinglish: Symbolic analyzer ka core logic, jo 'angr' ka use karke loops ko dhoondhta hai.

from pathlib import Path
import angr
from typing import List, Dict, Any

from crypto_finder.common.logging import log

class SymbolicAnalyzer:
    """angr ka use karke binary me complex code structures (jaise loops) ko analyze karta hai."""

    def __init__(self, binary_path: Path):
        if not binary_path.exists():
            log.error(f"Binary file not found: {binary_path}")
            raise FileNotFoundError(f"Binary file not found: {binary_path}")

        log.info(f"'{binary_path.name}' ko angr project me load kiya ja raha hai...")
        # auto_load_libs=False se analysis fast hota hai.
        self.project = angr.Project(str(binary_path), auto_load_libs=False)
        log.success("Angr project successfully loaded.")

    def find_loops(self, function_address: int = None) -> List[Dict[str, Any]]:
        """
        Binary me saare loops ko dhoondhta hai.
        Agar function_address diya hai, to sirf us function me dhoondhega.
        """
        log.info("Loop finding analysis start ho raha hai...")

        try:
            # Control-Flow Graph (CFG) build karo. Yeh program ka map hai.
            # fail_fast=True se analysis jaldi ho jaata hai agar koi problem ho.
            cfg = self.project.analyses.CFG(fail_fast=True)

            # LoopFinder analysis run karo.
            loop_finder = self.project.analyses.LoopFinder(kb=cfg.kb)
            
            results = []
            for loop in loop_finder.loops:
                # Sirf unhi loops ko consider karo jo hamare target function me hain (agar specified hai).
                if function_address and loop.entry.addr not in self.project.kb.functions[function_address].block_addrs:
                    continue
                
                loop_info = {
                    "entry_address": hex(loop.entry.addr),
                    "node_count": len(loop.body_nodes),
                }
                results.append(loop_info)
            
            log.success(f"Loop analysis complete. Found {len(results)} loop(s).")
            return results
        except Exception as e:
            log.error(f"Angr analysis ke dauran ek error aaya: {e}")
            return []