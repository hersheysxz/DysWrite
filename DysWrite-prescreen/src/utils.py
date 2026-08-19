"""
Module Name : utils.py
Project     : DysWrite Pre-Screening Engine
Created     : 2026-08-17
Author      : DysWrite Research Group (DMMMSU-SLUC College of Computer Science)
Summary     : Small, reusable helper functions shared across dataset.py,
              train.py, and infer.py, following the DRY principle instead of
              re-implementing logging setup or image loading in each script.
Functions   : get_logger(name), safe_open_image(path)
"""

import logging
import sys
from pathlib import Path
from typing import Union

from PIL import Image, UnidentifiedImageError

from src.exceptions import InvalidImageError


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger that writes to stdout with a consistent
    format. Centralized here so every module logs the same way instead of
    each file configuring (or forgetting to configure) logging on its own.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:  # avoid duplicate handlers on repeated calls
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def safe_open_image(path: Union[str, Path]) -> Image.Image:
    """
    Defensively open an image file and convert it to RGB.

    Unlike a bare `Image.open(path)`, this function eliminates the assumption
    that every file on disk is a valid, readable image (Defensive
    Programming: "eliminate assumptions"). Any failure is normalized into a
    single, well-defined InvalidImageError instead of leaking whichever raw
    exception PIL happened to raise (OSError, UnidentifiedImageError,
    FileNotFoundError, etc.), so callers only need to catch one exception
    type.

    Args:
        path: filesystem path to the image file.

    Returns:
        A PIL.Image.Image object in RGB mode.

    Raises:
        InvalidImageError: if the file does not exist or cannot be decoded
            as an image.
    """
    path = Path(path)
    if not path.exists():
        raise InvalidImageError(f"Image file does not exist: {path}")

    try:
        with Image.open(path) as img:
            return img.convert("RGB")
    except (OSError, UnidentifiedImageError) as exc:
        raise InvalidImageError(f"Could not decode image at {path}: {exc}") from exc
