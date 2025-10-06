"""
Main entry point for Crypto Finder CLI

Usage:
    crypto-finder analyze firmware.bin
    crypto-finder build-dataset --config config.yaml
    crypto-finder train --model-type rf
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from crypto_finder.common.logging import setup_logging
from crypto_finder.common.config import load_config

logger = setup_logging(__name__)


def analyze_firmware(firmware_path: str, output_dir: str, config: dict):
    """
    Analyze a firmware binary for cryptographic functions
    
    Args:
        firmware_path: Path to firmware binary
        output_dir: Where to save results
        config: Configuration dictionary
    """
    logger.info(f"Analyzing firmware: {firmware_path}")
    
    # Step 1: Unpack firmware
    logger.info("Step 1/5: Unpacking firmware...")
    try:
        from crypto_finder.firmware_processor.unpacker.binwalk_wrapper import FirmwareUnpacker  # type: ignore
    except Exception:  # Module may not exist yet
        raise ImportError("FirmwareUnpacker is not implemented. Please add firmware unpacker module.")
    unpacker = FirmwareUnpacker(firmware_path)
    extracted_dir = unpacker.unpack()
    
    # Step 2: Discover binaries
    logger.info("Step 2/5: Discovering binaries...")
    try:
        from crypto_finder.firmware_processor.binary_discovery.elf_finder import ElfFinder  # type: ignore
    except Exception:
        raise ImportError("ElfFinder is not implemented. Please add binary discovery module.")
    finder = ElfFinder(extracted_dir)
    binaries = finder.find_all()
    logger.info(f"Found {len(binaries)} ELF binaries")
    
    # Step 3: Extract functions
    logger.info("Step 3/5: Extracting functions...")
    try:
        # Prefer FunctionLifter if available, otherwise fallback to existing Lifter API
        from crypto_finder.lifter.core import FunctionLifter  # type: ignore
    except Exception:
        from crypto_finder.lifter.core import Lifter as FunctionLifter  # type: ignore
    lifter = FunctionLifter()
    all_functions = []
    for binary in binaries:
        binary_path = binary["path"] if isinstance(binary, dict) else binary
        extract = getattr(lifter, "extract_functions", None)
        if extract is None:
            # Fallback to a generic process method if present
            process_method = getattr(lifter, "process_binary", None)
            if process_method is None:
                raise AttributeError("Function extraction API not available in lifter.")
            result = process_method(Path(binary_path), Path(output_dir))
            if result is not None:
                all_functions.append({"binary": binary_path, "artifact": str(result)})
        else:
            functions = extract(binary_path)
            all_functions.extend(functions)
    logger.info(f"Extracted {len(all_functions)} functions")
    
    # Step 4: Run ML detection
    logger.info("Step 4/5: Running crypto detection...")
    try:
        from crypto_finder.ml.inference import CryptoDetector  # type: ignore
    except Exception:
        raise ImportError("CryptoDetector is not implemented. Please add ml.inference module.")
    model_path = config.get("model_path") if isinstance(config, dict) else None
    detector = CryptoDetector(model_path)
    detections = detector.detect_batch(all_functions)
    logger.info(f"Detected {len(detections)} crypto functions")
    
    # Step 5: Generate report
    logger.info("Step 5/5: Generating report...")
    from crypto_finder.reporter.core import ReportGenerator
    reporter = ReportGenerator(output_dir)
    reporter.generate_report(detections, firmware_path)
    
    logger.info(f"Analysis complete! Report saved to {output_dir}")
    return detections


def build_dataset(config_path: str, output_dir: str):
    """
    Build training dataset from crypto libraries
    
    Args:
        config_path: Path to dataset configuration YAML
        output_dir: Where to save compiled binaries
    """
    logger.info("Building dataset...")
    
    config = load_config(config_path)
    try:
        from crypto_finder.dataset_builder.compiler.cross_compiler import DatasetCompiler  # type: ignore
    except Exception:
        raise ImportError("DatasetCompiler is not implemented. Please add dataset_builder compiler module.")
    compiler = DatasetCompiler(config, output_dir)
    
    # Compile all crypto libraries for all architectures
    compiler.compile_all()
    
    logger.info("Dataset building complete!")


def train(model_type: str, data_dir: str, output_dir: str):
    """
    Train ML model on dataset
    
    Args:
        model_type: Type of model (rf, gb, neural)
        data_dir: Directory containing training data
        output_dir: Where to save trained model
    """
    logger.info(f"Training {model_type} model...")
    
    from crypto_finder.ml.train import train_model
    train_model(
        model_type=model_type,
        data_dir=data_dir,
        output_dir=output_dir
    )
    
    logger.info("Training complete!")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Crypto Finder - Automated Cryptographic Function Detection"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze firmware binary')
    analyze_parser.add_argument('firmware', help='Path to firmware binary')
    analyze_parser.add_argument('--output', '-o', default='results/', help='Output directory')
    analyze_parser.add_argument('--config', '-c', default='config/base.yaml', help='Config file')
    
    # Build-dataset command
    dataset_parser = subparsers.add_parser('build-dataset', help='Build training dataset')
    dataset_parser.add_argument('--config', '-c', required=True, help='Dataset config YAML')
    dataset_parser.add_argument('--output', '-o', default='data/01_compiled/', help='Output directory')
    
    # Train command
    train_parser = subparsers.add_parser('train', help='Train ML model')
    train_parser.add_argument('--model-type', '-m', default='rf', choices=['rf', 'gb', 'neural'])
    train_parser.add_argument('--data', '-d', default='data/04_datasets/', help='Training data directory')
    train_parser.add_argument('--output', '-o', default='data/06_models/', help='Model output directory')
    
    args = parser.parse_args()
    
    if args.command == 'analyze':
        config = load_config(args.config)
        analyze_firmware(args.firmware, args.output, config)
    
    elif args.command == 'build-dataset':
        build_dataset(args.config, args.output)
    
    elif args.command == 'train':
        train(args.model_type, args.data, args.output)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

# Hinglish: Hum yahan main.py ko update kar rahe hain taaki naya 'dynamic-run' command add ho sake.

import typer
from crypto_finder.common.logging import log

# Lifter, Static Scanner, Symbolic, aur Dynamic se unke CLI functions ko import karo.
from crypto_finder.lifter.cli import lift
from crypto_finder.static_scanner.cli import scan
from crypto_finder.symbolic.cli import analyze_loops
from crypto_finder.dynamic_runner.cli import dynamic_run

# Main Typer application object.
app = typer.Typer(
    name="crypto-finder",
    help="A robust framework for finding cryptographic primitives in firmware. 🚀",
    add_completion=False,
)

# Har function ko ek alag command ke roop me register karo.
app.command(name="lift")(lift)
app.command(name="scan")(scan)
app.command(name="symbolic-loops")(analyze_loops)
app.command(name="dynamic-run")(dynamic_run)


@app.callback()
def main_callback():
    """
    Crypto Finder CLI - Use a command like 'lift', 'scan', 'dynamic-run' etc. to get started.
    """
    log.info("Crypto Finder main CLI invoked.")

if __name__ == "__main__":
    app()