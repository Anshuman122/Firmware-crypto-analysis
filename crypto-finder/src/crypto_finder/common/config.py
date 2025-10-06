"""
Configuration management using YAML files

Loads and validates configuration from multiple sources:
- Base configuration
- Environment-specific overrides
- Command-line arguments
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import os

# Provide a project root and a simple settings container for compatibility
ROOT_DIR = Path(__file__).resolve().parents[3]


def load_config(config_path: str, environment: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to config file
        environment: Optional environment name (dev, prod, test)
    
    Returns:
        Configuration dictionary
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f) or {}
    
    # Load environment-specific config if specified
    if environment:
        env_config_path = config_file.parent / f"{environment}.yaml"
        if env_config_path.exists():
            with open(env_config_path, 'r') as f:
                env_config = yaml.safe_load(f) or {}
                config = merge_configs(config, env_config)
    
    # Override with environment variables if present
    config = apply_env_overrides(config)
    
    return config


def merge_configs(base: Dict, override: Dict) -> Dict:
    """
    Recursively merge two configuration dictionaries
    
    Args:
        base: Base configuration
        override: Configuration to merge in (takes precedence)
    
    Returns:
        Merged configuration
    """
    result = base.copy()
    
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value
    
    return result


def apply_env_overrides(config: Dict) -> Dict:
    """
    Apply environment variable overrides
    
    Environment variables in format: CRYPTO_FINDER_<SECTION>_<KEY>=value
    Example: CRYPTO_FINDER_MODEL_BATCH_SIZE=64
    
    Args:
        config: Configuration dictionary
    
    Returns:
        Configuration with environment overrides applied
    """
    prefix = "CRYPTO_FINDER_"
    
    for env_key, env_value in os.environ.items():
        if env_key.startswith(prefix):
            # Parse the key path
            key_path = env_key[len(prefix):].lower().split('_')
            
            # Navigate to the right place in config
            current = config
            for key in key_path[:-1]:
                if key not in current or not isinstance(current.get(key), dict):
                    current[key] = {}
                current = current[key]
            
            # Set the value (try to parse as appropriate type)
            final_key = key_path[-1]
            current[final_key] = parse_env_value(env_value)
    
    return config


def parse_env_value(value: str) -> Any:
    """
    Parse environment variable value to appropriate Python type
    
    Args:
        value: String value from environment
    
    Returns:
        Parsed value (str, int, float, bool, or list)
    """
    # Try boolean
    if value.lower() in ('true', 'yes', '1'):
        return True
    if value.lower() in ('false', 'no', '0'):
        return False
    
    # Try integer
    try:
        return int(value)
    except ValueError:
        pass
    
    # Try float
    try:
        return float(value)
    except ValueError:
        pass
    
    # Try list (comma-separated)
    if ',' in value:
        return [v.strip() for v in value.split(',')]
    
    # Return as string
    return value


def save_config(config: Dict, output_path: str):
    """
    Save configuration to YAML file
    
    Args:
        config: Configuration dictionary
        output_path: Where to save
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)


class SimpleNamespace:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


# Backwards-compatible settings singleton (paths only), used by existing modules
settings = SimpleNamespace(
    data_dir=ROOT_DIR / 'data',
    raw_data_dir=ROOT_DIR / 'data' / '01_raw',
    processed_data_dir=ROOT_DIR / 'data' / '03_processed',
    models_dir=ROOT_DIR / 'data' / '05_models',
)

# Hinglish: Pydantic ka use karke ek robust configuration setup.
# Yeh settings ko validate karta hai aur ensure karta hai ki sab aasaani se accessible ho.

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath
from pathlib import Path

# Project ka root directory find karo. Yeh ek global variable hai.
ROOT_DIR = Path(__file__).parent.parent.parent.parent

class GhidraSettings(BaseSettings):
    """Ghidra se related saari settings."""
    # Yahan ek default path diya gaya hai. Isse apne actual Ghidra path se replace karein.
    install_path: DirectoryPath = Path("C:/tools/ghidra_11.1.2_PUBLIC")

    @property
    def headless_path(self) -> Path:
        # Operating system ke hisab se headless script ka path return karo.
        if os.name == 'nt': # Windows
            return self.install_path / "support" / "analyzeHeadless.bat"
        return self.install_path / "support" / "analyzeHeadless"

class Settings(BaseSettings):
    """Project ki saari main settings."""
    model_config = SettingsConfigDict(env_file=ROOT_DIR / ".env", env_file_encoding='utf-8', extra='ignore')

    # Project Directories
    data_dir: DirectoryPath = ROOT_DIR / "data"
    raw_data_dir: DirectoryPath = data_dir / "01_raw"
    processed_data_dir: DirectoryPath = data_dir / "03_processed"
    models_dir: DirectoryPath = data_dir / "05_models"

    # Database
    database_url: str = f"sqlite:///{data_dir / 'crypto_finder.db'}"

    # Ghidra Settings
    ghidra: GhidraSettings = GhidraSettings()

    def __init__(self, **values):
        super().__init__(**values)
        # Yeh directories ensure karti hain ki exist karti hain.
        self.data_dir.mkdir(exist_ok=True)
        self.raw_data_dir.mkdir(exist_ok=True)
        self.processed_data_dir.mkdir(exist_ok=True)
        self.models_dir.mkdir(exist_ok=True)

# Ek global settings object jo pure application me use hoga.
settings = Settings()