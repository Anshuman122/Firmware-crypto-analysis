# Hinglish: Lifter ke core logic ke liye ek test file.
# Yeh 'test_binary' fixture ka use karke ek real binary par test run karta hai.

import pytest
from pathlib import Path
import json
from crypto_finder.lifter.core import Lifter

# Is test ko by default skip kiya gaya hai kyunki yeh ek live Ghidra instance maangta hai aur slow ho sakta hai.
# Local machine par test karne ke liye aap is line ko comment out kar sakte hain.
@pytest.mark.skip(reason="Requires a live Ghidra instance and proper config. For local validation only.")
def test_process_binary_real(test_binary: Path, tmp_path: Path):
    """
    Ek real test jo GhidraAdapter ko call karke lifter ko test karta hai.
    'test_binary' fixture se hamein compiled C program ka path milta hai.
    'tmp_path' fixture ek temporary directory provide karta hai output ke liye.
    """
    # Arrange (Test setup)
    lifter = Lifter()
    output_dir = tmp_path

    # Act (Asli operation ko run karo)
    result_path = lifter.process_binary(test_binary, output_dir)

    # Assert (Check karo ki result sahi hai ya nahi)
    assert result_path is not None, "Lifter ne koi output file path return nahi kiya."
    assert result_path.exists(), "Output JSON file create nahi hui."
    assert result_path.name == f"{test_binary.name}.ghidra.json", "Output file ka naam galat hai."
    
    # JSON content ko bhi check karo.
    with open(result_path, 'r') as f:
        data = json.load(f)
    
    assert data["binary_name"] == test_binary.name, "Binary ka naam JSON me aana chahiye."
    assert len(data["functions"]) >= 2, "Kam se kam 'main' aur 'add' function milne chahiye the."
    
    function_names = {f["name"] for f in data["functions"]}
    assert "main" in function_names, "'main' function nahi mila."
    assert "add" in function_names, "'add' function nahi mila."