"""
Custom exceptions for Argus.

All domain-specific errors should inherit from ArgusError.
This allows consistent error handling and logging across the system.
"""


class ArgusError(Exception):
    """Base exception for all Argus-related errors."""
    pass


# -----------------------------
# Configuration errors
# -----------------------------

class ConfigError(ArgusError):
    """Raised when configuration is invalid or missing."""
    pass


# -----------------------------
# Camera / stream errors
# -----------------------------

class CameraError(ArgusError):
    """Base exception for camera-related issues."""
    pass


class CameraConnectionError(CameraError):
    """Raised when a camera cannot be connected."""
    pass


class CameraReadError(CameraError):
    """Raised when a frame cannot be read from a camera."""
    pass


# -----------------------------
# Model / inference errors
# -----------------------------

class InferenceError(ArgusError):
    """Raised when model inference fails."""
    pass


class ModelLoadError(InferenceError):
    """Raised when a model fails to load."""
    pass


# -----------------------------
# Pipeline / system errors
# -----------------------------

class PipelineError(ArgusError):
    """Raised when a pipeline component fails."""
    pass
