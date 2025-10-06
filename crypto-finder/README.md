# 🤖 Crypto Finder: AI-Powered Cryptographic Analysis in Firmware  
### Team Loud ( Team ID 64517 )

---

## 📌 Introduction & Problem Context
The rapid proliferation of IoT and embedded systems has led to a security crisis. Billions of devices—from routers and cameras to industrial controllers—run on "black-box" firmware with undocumented or obfuscated code. Identifying the cryptographic functions within these binaries is a monumental challenge for security auditors, yet it is critical for ensuring confidentiality, integrity, and discovering vulnerabilities.

This project provides a unified, intelligent framework to automate this process. By integrating classic binary analysis techniques with modern **Machine Learning**, we transform the manual, architecture-specific task of reverse engineering into a scalable, automated pipeline. Our system dissects firmware binaries from heterogeneous architectures (x86, ARM, MIPS), identifies cryptographic primitives, and provides actionable intelligence.

---

## 🚀 Current Achievements & System Status

### Multi-Architecture Lifting Pipeline ⚙️  
- Integrated **Ghidra Headless** to lift binary code from multiple architectures into standardized P-Code.  

### Hybrid Analysis Engine 🔬  
- **Static Scanner:** `YARA`-based detection of cryptographic constants.  
- **Symbolic Analyzer:** `angr`-based CFG + loop detection.  
- **Dynamic Analyzer:** `Unicorn Engine` micro-emulation of code snippets.  

### Extensible Machine Learning Core 🧠  
- **PyTorch**-based MLP classifier for crypto vs non-crypto function detection.  

### Scalable Data & API Backend ☁️  
- Persistent storage with **SQLAlchemy**.  
- **FastAPI** server exposing ML predictions via REST.  

### Modular & Runnable Toolchain 🛠️  
- CLI built with **Typer**.  
- Independent modules (`lift`, `scan`, etc.) runnable as standalone tools.  

---

## 🏗 Technical Architecture: A Deep Dive

### I. Data Ingestion & Preprocessing
| Component | Technology | Role |
|-----------|------------|------|
| Firmware Corpus | Python + `requests` | Build local dataset of real-world firmware. |
| Controlled Dataset | Cross-compilation | Generate labeled crypto/non-crypto datasets across architectures. |
| Data Persistence | SQLAlchemy + SQLite/Postgres | Store metadata + analysis results. |

### II. Core Analysis Pipeline
| Component | Technology | Role |
|-----------|------------|------|
| Lifter | Ghidra Headless | Convert machine code → P-Code JSON. |
| Static Scanner | YARA | Detect crypto constants. |
| Symbolic Analyzer | angr | Explore CFGs, detect loops. |
| Dynamic Analyzer | Unicorn | Lightweight emulation for traces. |

### III. Machine Learning Core
| Step | Details |
|------|---------|
| Feature Extraction | `ml/features.py` extracts opcode counts, function size. |
| Data Handling | `ml/datasets.py` serves feature vectors + labels. |
| Classification Model | `CryptoClassifierMLP` (PyTorch MLP). |
| Training/Evaluation | `ml/train.py` + `ml/evaluate.py` with sklearn metrics. |

### IV. Service Layer & Deployment
| Component | Technology | Role |
|-----------|------------|------|
| API Layer | FastAPI | `/predict` endpoint for ML inference. |
| Data Validation | Pydantic | Schema validation + docs. |
| Deployment | Docker + Uvicorn | Containerized + reproducible builds. |
| User Interface | Typer CLI | CLI commands for all modules. |

---

## 🖼️ System Visuals
*(High-level architecture diagram placeholder)*  

---

## 🔒 Robustness & Reliability
| Module | Purpose | Mechanism |
|--------|---------|-----------|
| Config | Centralized settings | `common/config.py` + Pydantic validation. |
| Error Handling | Prevent crashes | Structured logging with Loguru. |
| Reproducibility | Stable builds | Docker + pyproject.toml. |
| Testing | Code correctness | Pytest fixtures and automated tests. |

---

# 🔐 Crypto Finder

Crypto Finder is a research & engineering toolkit for **detecting cryptographic primitives** inside binaries and firmware images.  
It combines **static analysis (Ghidra, Capstone, YARA), dynamic analysis (QEMU harnesses), symbolic execution (angr)**, and **ML-based detection** to classify and analyze crypto functions.

---

## 📸 Showcase & Demo

### CLI in Action
```powershell
# Scan binary for constants
crypto-finder scan --binary-path C:\Windows\System32\bcrypt.dll

# Symbolic loop detection
crypto-finder symbolic-loops --binary-path ./sample.exe

# Dynamic emulation of shellcode
crypto-finder dynamic-run --shellcode "554889e5c3"

```
###API Prediction Example
```
{
  "function_name": "AES_encrypt_block",
  "prediction": {
    "label": "crypto",
    "confidence": 0.9875
  }
}
```

##🛣 Future Roadmap

GNNs & Transformers for CFG/P-Code sequences.

Protocol-level detection (TLS handshakes, key exchanges).

Full-system emulation with FirmAE
.

Web Dashboard for visualization of analysis results.
```text
## 📂 Repository Structure
crypto-finder/

├─ config/
│  ├─ base.yaml
│  ├─ datasets/            # (reserved for dataset-specific configs)
│  ├─ models/              # (reserved for model/inference configs)
│  └─ analysis/            # (reserved for analysis pipeline configs)
|     
├─ data/
│  ├─ 00_sources/          # Original sources (downloaded crypto libs)
│  ├─ 01_compiled/         # Cross-compiled binaries (per arch/opt)
│  ├─ 02_extracted/        # Extracted artifacts from firmware
│  ├─ 03_features/         # Extracted feature vectors
│  ├─ 04_datasets/         # Train/val/test datasets
│  ├─ 05_firmware/         # Raw firmware images
│  └─ 06_models/           # Trained model files
|     
├─ docker/
│  ├─ Dockerfile.api
│  ├─ Dockerfile.worker
│  ├─ Dockerfile.dataset_builder
│  └─ docker-compose.yml
|     
├─ notebooks/
│  ├─ 01-dataset-exploration.ipynb
│  ├─ 02-feature-engineering.ipynb
│  └─ 03-model-prototyping.ipynb
|     
├─ scripts/
|  |   
│  ├─ setup/
│  │  ├─ install_toolchains.sh     # Installs cross-compilers/tooling
│  │  └─ setup_environment.sh      # Project env/bootstrap
|  |
│  ├─ dataset/
│  │  ├─ build_controlled_dataset.py   # Build synthetic dataset
│  │  ├─ download_libraries.py         # Download crypto libs
│  │  ├─ compile_all.py                # Batch compile libs
│  │  └─ validate_dataset.py           # Sanity checks for dataset
|  |
│  ├─ firmware/
│  │  ├─ download_firmware.py          # Fetch firmware images
│  │  ├─ extract_firmware.py           # Batch unpack/extract
│  │  └─ batch_process.py              # End-to-end firmware processing
|  |
│  └─ automation/
│     ├─ run_pipeline.py               # Orchestrates overall pipeline
│     └─ continuous_training.py        # Periodic re-training job
|     
├─ src/
│  └─ crypto_finder/
│     ├─ __init__.py
│     ├─ main.py                   # CLI entrypoint: analyze/build-dataset/train
|     |
│     ├─ common/
│     │  ├─ __init__.py
│     │  ├─ config.py              # YAML config loader + settings (paths)
│     │  ├─ logging.py             # Colored console + rotating file logs; global `log` with SUCCESS level
│     │  ├─ db.py                  # Database helpers (SQLAlchemy)
│     │  ├─ metrics.py             # Small metrics helpers
│     │  ├─ cache.py               # LRU and filesystem cache decorators
│     │  └─ exceptions.py          # Typed exceptions (incl. FirmwareExtractionError, CompilationError)
|     |
│     ├─ dataset_builder/          # CRITICAL: build labeled crypto datasets
│     │  ├─ compiler/
│     │  │  ├─ cross_compiler.py   # Cross-compile crypto libs (multi-arch/opt)
│     │  │  └─ library_manager.py  # Download/extract library sources
│     │  ├─ extraction/
│     │  │  └─ function_extractor.py   # Extract funcs from binaries (symbols/heuristics)
│     │  └─ labeling/
│     │     └─ auto_labeler.py         # Auto-label based on names/library
|     |
│     ├─ firmware_processor/       # Real-world firmware processing
│     │  ├─ unpacker/
│     │  │  └─ binwalk_wrapper.py  # Unpack images via binwalk
│     │  ├─ binary_discovery/
│     │  │  └─ elf_finder.py       # Recursively find ELF binaries
│     │  └─ triage/
│     │     └─ basic_triage.py     # Grouping & Top-N selection for binaries
|     |
│     ├─ lifter/
│     │  ├─ cli.py                 # CLI for lifting (legacy)
│     │  ├─ core.py                # Lifter wrapper (Ghidra/Capstone integration)
│     │  └─ adapters/
│     │     ├─ ghidra.py           # Ghidra headless adapter
│     │     ├─ capstone.py         # Disassembly helpers
│     │     └─ angr.py             # Angr adapter
|     |
│     ├─ static_scanner/
│     │  ├─ cli.py                 # CLI to run static scans
│     │  ├─ core.py                # YARA/constant scan core
│     │  ├─ signatures/
│     │  │  ├─ findcrypt.yar
│     │  │  └─ crypto_constants.json
│     │  └─ heuristics/
│     │     ├─ entropy.py          # High-entropy region finder
│     │     └─ loop_detector.py    # Simple loop/backedge heuristic placeholder
|     |
│     ├─ dynamic_runner/
│     │  ├─ cli.py                 # CLI for micro-emulation/tracing
│     │  ├─ core.py                # Unicorn/QEMU emulation scaffolding
│     │  ├─ harnesses/
│     │  │  └─ qemu_harness.py     # QEMU invocation helper
│     │  └─ tracers/
│     │     ├─ pin_tracer.py       # Intel PIN tracer placeholder
│     │     └─ dynamorio_tracer.py # DynamoRIO tracer placeholder
|     |
│     ├─ symbolic/
│     │  ├─ cli.py                 # CLI for symbolic analyses
│     │  ├─ loop_analyzer.py       # CFG + loop analysis with angr
|     |
│     ├─ ml/
│     │  ├─ datasets.py            # Dataset utilities
│     │  ├─ features.py            # Legacy feature extractor
│     │  ├─ features/              # New modular feature extractors
│     │  │  ├─ statistical.py      # Histograms, entropy, basic stats
│     │  │  ├─ constants.py        # S-box/IV signature presence
│     │  │  ├─ structural.py       # Size/shape heuristics
│     │  │  ├─ semantic.py         # Placeholder semantic features
│     │  │  └─ embeddings.py       # n-gram byte embeddings
│     │  ├─ models.py              # Legacy model definitions
│     │  ├─ models/                # New model namespace (stubs to be implemented)
│     │  │  ├─ binary_classifier.py
│     │  │  ├─ algorithm_classifier.py
│     │  │  ├─ ensemble.py
│     │  │  └─ gnn_model.py
│     │  ├─ train.py               # Training routine (uses models/features)
│     │  ├─ evaluate.py            # Evaluation metrics
│     │  └─ inference.py           # CryptoDetector stub (batch predictions)
|     |
│     ├─ api/                      # FastAPI service layer
│     │  ├─ main.py                # App factory/mounting (existing legacy)
│     │  ├─ models.py              # API pydantic models (legacy)
│     │  ├─ endpoints.py           # Legacy endpoints
│     │  ├─ endpoints/
│     │  │  ├─ analysis.py         # Health/status + analysis endpoints (stub)
│     │  │  ├─ datasets.py         # Dataset endpoints (stub)
│     │  │  └─ models.py           # Model registry endpoints (stub)
│     │  └─ middleware/
│     │     ├─ auth.py             # Simple API-key guard
│     │     └─ rate_limit.py       # Naive rate limiting dependency
|     |
│     ├─ reporter/
│     │  ├─ core.py                # Builds HTML report + detections.json
│     │  ├─ formats/               # (reserved for alt outputs, e.g., PDF/CSV)
│     │  ├─ visualizations/        # (reserved for charts/plots)
│     │  └─ templates/
│     │     └─ report_template.html# 
|     |
│     ├─ protocol_analyzer/        #  Protocol-level analysis
│     │  ├─ call_graph/
│     │  ├─ patterns/
│     │  └─ sequence_analyzer/
│     └─ validation/               #  Ground truth/validators
│        ├─ validators/
│        ├─ confidence/
│        └─ ground_truth/
├─ tests/
│  ├─ unit/            # Unit tests
│  ├─ integration/     # Multi-module tests
│  ├─ end_to_end/      # Full-pipeline tests
│  ├─ fixtures/        # Test data/fixtures
│  └─ benchmarks/      # Performance tests
|
└─ docs/
|   ├─ api/             # API reference
|   ├─ architecture/    # System diagrams/ADR
|   ├─ tutorials/       # Guides/how-tos
|   └─ deployment/      # Deploy/runbooks
|
├─ README.md
├─ pyproject.toml
├─ .gitignore
├─ .dockerignore
├─ LICENSE
├─ CONTRIBUTING.md
```
#🤝 Contact

Project – Crypto Finder
Team - Loud 
