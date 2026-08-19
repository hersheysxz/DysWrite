"""
Module Name : config.py
Project     : DysWrite Pre-Screening Engine
Created     : 2026-08-17
Author      : DysWrite Research Group (DMMMSU-SLUC College of Computer Science)
Summary     : Centralizes all configuration constants (paths, class labels, image
              size, training hyperparameters) so that no other module in this
              project hardcodes "magic numbers" or hardcoded strings. Any value
              that needs to change (e.g. dataset location, number of classes,
              batch size) is changed in exactly one place.
Functions   : none (constants + one validation helper)
Notes       : Values here mirror the MobileNetV3-Small + Grad-CAM approach
              referenced from Robaa et al. (used as this project's technical
              precedent), adapted for DysWrite's own pre-screening pipeline.
"""

from pathlib import Path

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "sample_data"
CHECKPOINT_DIR = PROJECT_ROOT / "checkpoints"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
LOG_DIR = PROJECT_ROOT / "logs"

# --------------------------------------------------------------------------- #
# Class labels (must match the subfolder names under DATA_DIR)
# --------------------------------------------------------------------------- #
CLASS_NAMES = ["normal", "reversal", "corrected"]
NUM_CLASSES = len(CLASS_NAMES)

# --------------------------------------------------------------------------- #
# Image / model settings
# --------------------------------------------------------------------------- #
IMAGE_SIZE = (224, 224)
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]
GRADCAM_TARGET_LAYER = "features.12"  # last conv block of MobileNetV3-Small

# --------------------------------------------------------------------------- #
# Training hyperparameters
# --------------------------------------------------------------------------- #
BATCH_SIZE = 16
LEARNING_RATE = 1e-4
NUM_EPOCHS = 15
TRAIN_SPLIT = 0.8
VAL_SPLIT = 0.1  # remainder (0.1) is used for test
EARLY_STOPPING_PATIENCE = 3          # epochs to wait for val-loss improvement
EARLY_STOPPING_MIN_DELTA = 1e-4      # minimum change counted as "improvement"
RANDOM_SEED = 42

# --------------------------------------------------------------------------- #
# Confidence threshold below which a prediction is flagged "uncertain"
# rather than shown to the end user as a confident pre-screening result.
# --------------------------------------------------------------------------- #
MIN_CONFIDENCE_THRESHOLD = 0.55


def validate_split_ratios() -> None:
    """
    Defensive check run at import time: ensures TRAIN_SPLIT + VAL_SPLIT never
    silently produces a negative or zero test split, which would otherwise
    fail much later inside the DataLoader with a confusing error.
    """
    test_split = 1.0 - TRAIN_SPLIT - VAL_SPLIT
    if test_split <= 0:
        raise ValueError(
            f"Invalid split configuration: TRAIN_SPLIT ({TRAIN_SPLIT}) + "
            f"VAL_SPLIT ({VAL_SPLIT}) leaves no room for a test split "
            f"({test_split:.2f}). Adjust config.py."
        )


validate_split_ratios()
