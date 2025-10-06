# Hinglish: Yeh lifter module ka core logic hai. Yeh adapters ka use karke اصل lifting ka kaam karta hai.

from pathlib import Path
from crypto_finder.lifter.adapters.ghidra import GhidraAdapter
from crypto_finder.common.logging import log

class Lifter:
    """Binary code ko high-level IR me convert karne ke liye main class."""

    def __init__(self):
        self.ghidra_adapter = GhidraAdapter()

    def process_binary(self, binary_path: Path, output_dir: Path):
        """
        Ek single binary ko process karta hai aur result ko JSON file me save karta hai.
        
        :param binary_path: Process ki jaane wali file.
        :param output_dir: JSON output save karne ke liye directory.
        """
        log.info(f"Processing binary: {binary_path.name}")
        
        try:
            # Ghidra adapter ka use karke lifting karo.
            lifted_data = self.ghidra_adapter.lift(binary_path)

            # Output file ka path banao.
            output_path = output_dir / f"{binary_path.name}.ghidra.json"
            
            # Result ko save karo.
            with open(output_path, 'w') as f:
                import json
                json.dump(lifted_data, f, indent=4)

            log.success(f"Successfully lifted binary. Output saved to {output_path}")
            return output_path

        except Exception as e:
            log.error(f"Failed to process {binary_path.name}: {e}")
            return None