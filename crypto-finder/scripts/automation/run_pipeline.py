# Hinglish: Yeh hamara master pipeline script hai.
# Yeh ek binary leta hai, uspar saare analysis (lifter, scanner) run karta hai, aur results database me save karta hai.

import typer
from pathlib import Path

from crypto_finder.common.logging import log
from crypto_finder.common.db import SessionLocal, Binary, AnalysisResult, create_db_and_tables
from crypto_finder.static_scanner.core import StaticScanner
# Lifter ko import karo, lekin use abhi comment out rakho
# from crypto_finder.lifter.core import Lifter

# YARA rules ka default path
DEFAULT_RULES_PATH = Path(__file__).parent.parent / "src" / "crypto_finder" / "static_scanner" / "signatures" / "findcrypt.yar"

app = typer.Typer()

@app.command()
def run(
    binary_path: Path = typer.Option(..., "--binary-path", "-b", help="The binary file to analyze.", exists=True),
):
    """Runs the full analysis pipeline on a single binary file."""
    log.info(f"Full pipeline run for '{binary_path.name}' shuru ho raha hai.")
    
    # Step 1: Database session create karo
    db = SessionLocal()
    create_db_and_tables() # Ensure tables exist
    
    try:
        # Step 2: Check karo ki binary DB me pehle se hai ya nahi
        db_binary = db.query(Binary).filter(Binary.filepath == str(binary_path)).first()
        if not db_binary:
            log.info("Yeh naya binary hai. Isse database me add kiya ja raha hai.")
            db_binary = Binary(
                filename=binary_path.name,
                filepath=str(binary_path),
                filesize=binary_path.stat().st_size
            )
            db.add(db_binary)
            db.commit()
            db.refresh(db_binary)

        # Step 3: Static Scan run karo
        log.info("--- Static Analysis Stage ---")
        scanner = StaticScanner(rules_path=DEFAULT_RULES_PATH)
        static_results = scanner.scan(binary_path)
        
        # Static analysis ke result ko DB me save karo
        scan_result_entry = AnalysisResult(
            binary_id=db_binary.id,
            analysis_type="static_scan",
            result_data={"signatures": static_results}
        )
        db.add(scan_result_entry)
        
        # Step 4: Lifter run karo (Abhi ke liye commented out)
        # log.info("--- Lifter Stage (SKIPPED) ---")
        # lifter = Lifter()
        # lifter_output_path = lifter.process_binary(binary_path, some_output_dir)
        # Add to DB...

        # Saare changes ko database me commit karo
        db.commit()
        log.success("Pipeline finished. Saare results database me save ho gaye hain.")
        
    except Exception as e:
        log.error(f"Pipeline ke dauran ek error aaya: {e}")
        db.rollback() # Agar error aaye to changes ko undo karo
    finally:
        db.close() # Hamesha session ko close karo


if __name__ == "__main__":
    app()