"""
Module Name : dataset.py
Project     : DysWrite Pre-Screening Engine
Created     : 2026-08-17
Author      : DysWrite Research Group (DMMMSU-SLUC College of Computer Science)
Summary     : Loads handwriting sample images from disk into a PyTorch
              Dataset. Applies defensive checks (folder existence, class-name
              consistency against config.CLASS_NAMES, per-image validity)
              rather than assuming the dataset directory is always well
              formed.
Functions   : build_transform()
Classes     : HandwritingDataset(Dataset)
"""

from pathlib import Path
from typing import List, Optional, Tuple

import torch
from torch.utils.data import Dataset
from torchvision import transforms

from src import config
from src.exceptions import ClassMismatchError, DatasetError, InvalidImageError
from src.utils import get_logger, safe_open_image

logger = get_logger(__name__)


def build_transform() -> transforms.Compose:
    """Return the standard preprocessing pipeline used for train/val/test/inference."""
    return transforms.Compose([
        transforms.Resize(config.IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=config.IMAGENET_MEAN, std=config.IMAGENET_STD),
    ])


class HandwritingDataset(Dataset):
    """
    PyTorch Dataset over a directory of handwriting sample images, organized
    as:

        root_folder/
            normal/       *.png|*.jpg
            reversal/     *.png|*.jpg
            corrected/    *.png|*.jpg

    Defensive checks performed at construction time (fail fast, with a clear
    message, instead of failing much later inside the training loop):
      1. root_folder must exist.
      2. The class subfolders discovered on disk must exactly match
         config.CLASS_NAMES (prevents a silent train/inference label
         mismatch if a folder is renamed, added, or removed).
      3. root_folder must contain at least one image.

    Per-image validity is handled defensively in __getitem__: a corrupted or
    unreadable image is logged and skipped by substituting a sentinel label
    of -1, which calling code (see train.py) must filter out before use.
    """

    def __init__(self, root_folder: str, transform: Optional[transforms.Compose] = None):
        self.root_folder = Path(root_folder)
        self.transform = transform or build_transform()

        if not self.root_folder.exists():
            raise DatasetError(f"Dataset root folder does not exist: {self.root_folder}")

        discovered = sorted(
            p.name for p in self.root_folder.iterdir() if p.is_dir()
        )
        if set(discovered) != set(config.CLASS_NAMES):
            raise ClassMismatchError(
                f"Class folders discovered on disk {discovered} do not match "
                f"config.CLASS_NAMES {config.CLASS_NAMES}. Update config.py or "
                f"fix the dataset folder structure before continuing."
            )

        self.classes: List[str] = config.CLASS_NAMES
        self.class_to_idx = {cls: i for i, cls in enumerate(self.classes)}
        self.samples: List[Tuple[Path, int]] = self._index_samples()

        if len(self.samples) == 0:
            raise DatasetError(
                f"No images found under {self.root_folder}. Populate the "
                f"class subfolders before training."
            )

        logger.info(
            "Loaded dataset: %d images across %d classes (%s)",
            len(self.samples), len(self.classes), ", ".join(self.classes),
        )

    def _index_samples(self) -> List[Tuple[Path, int]]:
        samples = []
        valid_extensions = {".png", ".jpg", ".jpeg", ".bmp"}
        for cls in self.classes:
            class_dir = self.root_folder / cls
            for image_path in class_dir.iterdir():
                if image_path.suffix.lower() in valid_extensions:
                    samples.append((image_path, self.class_to_idx[cls]))
        return samples

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, index: int):
        image_path, label = self.samples[index]
        try:
            image = safe_open_image(image_path)
        except InvalidImageError as exc:
            logger.warning("Skipping unreadable sample: %s", exc)
            image = transforms.functional.to_pil_image(
                torch.zeros(3, *config.IMAGE_SIZE)
            )
            label = -1  # sentinel: caller MUST filter this out before training

        if self.transform:
            image = self.transform(image)

        return image, label
