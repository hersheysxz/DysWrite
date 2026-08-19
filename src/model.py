"""
Module Name : model.py
Project     : DysWrite Pre-Screening Engine
Created     : 2026-08-17
Author      : DysWrite Research Group (DMMMSU-SLUC College of Computer Science)
Summary     : Builds the MobileNetV3-Small transfer-learning model used for
              dyslexia handwriting pre-screening (architecture choice follows
              Robaa et al., adapted here to DysWrite's 3-class label space)
              and provides checkpoint save/load helpers with defensive
              existence checks.
Functions   : build_model(num_classes), save_checkpoint(model, path),
              load_checkpoint(model, path, device)
"""

from pathlib import Path
from typing import Union

import torch
from torch import nn
from torchvision import models

from src import config
from src.exceptions import ModelCheckpointError
from src.utils import get_logger

logger = get_logger(__name__)


def build_model(num_classes: int = config.NUM_CLASSES, weights=None) -> nn.Module:
    """
    Build a MobileNetV3-Small model, optionally initialized from ImageNet
    weights. By default, this project deliberately avoids requiring a
    download from the network so the repository can be run on any teammate's
    machine without depending on a cached model file.

    Args:
        num_classes: number of output classes. Defaults to config.NUM_CLASSES.
        weights: optional torchvision weights object. Pass None to initialize
            from scratch.

    Returns:
        A torchvision MobileNetV3-Small model ready for fine-tuning.
    """
    if num_classes < 2:
        raise ValueError(f"num_classes must be >= 2, got {num_classes}")

    if weights is None:
        model = models.mobilenet_v3_small(weights=None)
    else:
        model = models.mobilenet_v3_small(weights=weights)

    in_features = model.classifier[0].in_features
    model.classifier = nn.Sequential(
        nn.Linear(in_features, 128),
        nn.Hardswish(),
        nn.Dropout(p=0.2),
        nn.Linear(128, num_classes),
    )
    return model


def save_checkpoint(model: nn.Module, path: Union[str, Path]) -> None:
    """Save model weights, creating the parent directory if needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), path)
    logger.info("Saved checkpoint to %s", path)


def load_checkpoint(model: nn.Module, path: Union[str, Path], device: torch.device) -> nn.Module:
    """
    Load weights into `model` from `path`, with defensive checks instead of
    letting torch.load() raise a raw, unhandled FileNotFoundError deep inside
    calling code.

    Raises:
        ModelCheckpointError: if the checkpoint file does not exist or fails
            to load (corrupted file, architecture mismatch, etc.).
    """
    path = Path(path)
    if not path.exists():
        raise ModelCheckpointError(f"Checkpoint file not found: {path}")

    try:
        state_dict = torch.load(path, map_location=device)
        model.load_state_dict(state_dict)
    except (RuntimeError, EOFError, OSError) as exc:
        raise ModelCheckpointError(f"Failed to load checkpoint {path}: {exc}") from exc

    model.to(device)
    logger.info("Loaded checkpoint from %s", path)
    return model
