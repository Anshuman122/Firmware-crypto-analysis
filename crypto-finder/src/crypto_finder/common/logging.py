"""
Centralized logging configuration

Provides consistent logging across all modules with:
- Colored console output
- File logging with rotation
- Structured logging for analysis
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


# ANSI color codes for terminal output
class LogColors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support"""
    
    COLORS = {
        'DEBUG': LogColors.CYAN,
        'INFO': LogColors.GREEN,
        'WARNING': LogColors.YELLOW,
        'ERROR': LogColors.RED,
        'CRITICAL': LogColors.MAGENTA,
    }
    
    def format(self, record):
        # Add color to level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{LogColors.RESET}"
        
        return super().format(record)


def setup_logging(
    name: str,
    level: str = "INFO",
    log_dir: Optional[str] = "logs",
    console: bool = True,
    file_logging: bool = True
) -> logging.Logger:
    """
    Setup logging for a module
    
    Args:
        name: Logger name (usually __name__)
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_dir: Directory for log files
        console: Enable console output
        file_logging: Enable file logging
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Format string
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Console handler with colors
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_formatter = ColoredFormatter(log_format, datefmt=date_format)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # File handler with rotation
    if file_logging and log_dir:
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        
        # General log file
        file_handler = RotatingFileHandler(
            log_path / 'crypto_finder.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(log_format, datefmt=date_format)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Error-specific log file
        error_handler = RotatingFileHandler(
            log_path / 'errors.log',
            maxBytes=10*1024*1024,
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        logger.addHandler(error_handler)
    
    return logger


# Provide a global logger with a custom SUCCESS level for compatibility
SUCCESS_LEVEL_NUM = 25  # Between INFO (20) and WARNING (30)
if not hasattr(logging, 'SUCCESS'):
    logging.addLevelName(SUCCESS_LEVEL_NUM, 'SUCCESS')


def _success(self, message, *args, **kws):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kws)


logging.Logger.success = _success  # type: ignore[attr-defined]

# Global logger used by modules that import `log`
log = setup_logging("crypto_finder")

# Hinglish: Loguru ka use karke ek behtar aur modern logging setup.
# Isse logging karna aasaan aur powerful ho jaata hai.

import sys
from loguru import logger

def setup_logging():
    """Application ke liye logging ko configure karta hai."""
    # Pehle se मौजूद saare handlers ko remove karo.
    logger.remove()

    # Console (terminal) me log karne ke liye ek naya handler add karo.
    # Iska format behtar readability ke liye set kiya gaya hai.
    logger.add(
        sys.stderr,
        level="DEBUG",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
    )
    
    # File me log karne ke liye ek handler (optional, agar zaroorat pade).
    # logger.add(
    #     "logs/app.log",
    #     level="DEBUG",
    #     rotation="10 MB", # Har 10 MB ke baad nayi file.
    #     retention="10 days", # 10 din purane logs delete.
    #     format="{time} {level} {message}",
    # )

    logger.info("Logger successfully configured.")
    return logger

# Ek global logger object jo pure application me use hoga.
log = setup_logging()
