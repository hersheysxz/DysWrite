"""
Module Name : exceptions.py
Project     : DysWrite Pre-Screening Engine
Created     : 2026-08-17
Author      : DysWrite Research Group (DMMMSU-SLUC College of Computer Science)
Summary     : Defines a small, well-defined exception hierarchy for this
              project instead of letting every failure surface as a generic
              built-in exception. This lets calling code (train.py, infer.py)
              catch specific, meaningful error types rather than bare
              `except Exception`.
Functions   : none (exception classes only)
"""


class DysWriteError(Exception):
    """Base class for all custom exceptions raised by this project."""


class DatasetError(DysWriteError):
    """Raised when the dataset directory is missing, empty, or malformed."""


class ClassMismatchError(DysWriteError):
    """
    Raised when the number/names of class folders discovered on disk do not
    match config.CLASS_NAMES. Prevents silently training or running
    inference against the wrong label space.
    """


class ModelCheckpointError(DysWriteError):
    """Raised when a model checkpoint file is missing, unreadable, or corrupt."""


class InvalidImageError(DysWriteError):
    """Raised when an input image cannot be opened or decoded."""
