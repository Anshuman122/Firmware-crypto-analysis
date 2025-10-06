"""
Custom exceptions for Crypto Finder

Provides specific exception types for different error scenarios
"""


class CryptoFinderException(Exception):
    """Base exception for all Crypto Finder errors"""
    pass


class FirmwareExtractionError(CryptoFinderException):
    """Error during firmware unpacking"""
    pass


class BinaryDiscoveryError(CryptoFinderException):
    """Error while discovering binaries in extracted firmware"""
    pass


class LiftingError(CryptoFinderException):
    """Errors raised during lifting or function extraction"""
    pass


class StaticScanError(CryptoFinderException):
    """Errors in static signature or heuristic scanning"""
    pass


class DynamicAnalysisError(CryptoFinderException):
    """Errors in dynamic execution or tracing"""
    pass


class SymbolicAnalysisError(CryptoFinderException):
    """Errors during symbolic execution or constraint solving"""
    pass


class ModelTrainingError(CryptoFinderException):
    """Errors during ML model training"""
    pass


class InferenceError(CryptoFinderException):
    """Errors during model inference"""
    pass

class CompilationError(CryptoFinderException):
    """Errors during cross-compilation or toolchain discovery"""
    pass


