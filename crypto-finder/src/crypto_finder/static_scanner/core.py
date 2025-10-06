# Hinglish: Static scanner ka core logic, jo YARA rules ka use karke binary scan karta hai.

from pathlib import Path
import yara
from typing import List, Dict, Any

from crypto_finder.common.logging import log

class StaticScanner:
    """YARA ka use karke binary files me cryptographic signatures dhundhta hai."""

    def __init__(self, rules_path: Path):
        """
        Scanner ko YARA rules ke path ke saath initialize karta hai.
        """
        if not rules_path.exists():
            log.error(f"YARA rules file not found at: {rules_path}")
            raise FileNotFoundError(f"YARA rules file not found at: {rules_path}")
        
        try:
            log.info(f"YARA rules file '{rules_path.name}' ko compile kiya ja raha hai...")
            self.rules = yara.compile(filepath=str(rules_path))
            log.success("YARA rules successfully compiled.")
        except yara.Error as e:
            log.error(f"YARA rules ko compile karne me error: {e}")
            raise

    def scan(self, binary_path: Path) -> List[Dict[str, Any]]:
        """
        Ek binary file ko scan karke saare matches return karta hai.
        """
        if not binary_path.exists():
            log.error(f"Binary file not found: {binary_path}")
            raise FileNotFoundError(f"Binary file not found: {binary_path}")

        log.info(f"'{binary_path.name}' ko crypto signatures ke liye scan kiya ja raha hai...")
        matches = self.rules.match(filepath=str(binary_path))
        
        results = []
        for match in matches:
            result = {
                "rule": match.rule,
                "crypto_name": match.meta.get("crypto_name", "Unknown"),
                "description": match.meta.get("description", "No description"),
                "matches": [
                    {
                        "offset": offset,
                        "identifier": identifier,
                        "data": data.hex(),
                    }
                    for offset, identifier, data in match.strings
                ],
            }
            results.append(result)

        if results:
            log.success(f"Scan complete. Found {len(results)} matching rule(s).")
        else:
            log.warning("Scan complete. No matching crypto signatures found.")
            
        return results