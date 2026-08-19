"""
Module Name : test_dataset.py
Project     : DysWrite Pre-Screening Engine
Created     : 2026-08-17
Author      : DysWrite Research Group (DMMMSU-SLUC College of Computer Science)
Summary     : Unit tests for src/dataset.py. Verifies the defensive checks
              (missing folder, class-name mismatch, empty dataset, corrupted
              image handling) actually behave as documented, instead of only
              being tested manually and informally.
Usage       : python -m unittest discover -s tests
"""

import shutil
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from src import config
from src.dataset import HandwritingDataset
from src.exceptions import ClassMismatchError, DatasetError


class TestHandwritingDataset(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def _make_valid_dataset_dir(self, images_per_class: int = 2) -> Path:
        root = self.tmp_dir / "valid_dataset"
        for cls in config.CLASS_NAMES:
            class_dir = root / cls
            class_dir.mkdir(parents=True)
            for i in range(images_per_class):
                img = Image.new("RGB", (32, 32), color=(i * 10, 0, 0))
                img.save(class_dir / f"sample_{i}.png")
        return root

    def test_missing_root_folder_raises_dataset_error(self):
        missing_path = self.tmp_dir / "does_not_exist"
        with self.assertRaises(DatasetError):
            HandwritingDataset(str(missing_path))

    def test_class_mismatch_raises_class_mismatch_error(self):
        root = self.tmp_dir / "wrong_classes"
        (root / "cat").mkdir(parents=True)
        (root / "dog").mkdir(parents=True)
        with self.assertRaises(ClassMismatchError):
            HandwritingDataset(str(root))

    def test_empty_dataset_raises_dataset_error(self):
        root = self.tmp_dir / "empty_dataset"
        for cls in config.CLASS_NAMES:
            (root / cls).mkdir(parents=True)
        with self.assertRaises(DatasetError):
            HandwritingDataset(str(root))

    def test_valid_dataset_loads_expected_sample_count(self):
        root = self._make_valid_dataset_dir(images_per_class=3)
        dataset = HandwritingDataset(str(root))
        self.assertEqual(len(dataset), 3 * len(config.CLASS_NAMES))

    def test_corrupted_image_yields_sentinel_label(self):
        root = self._make_valid_dataset_dir(images_per_class=1)
        # Corrupt one file by overwriting it with garbage bytes.
        corrupted_path = next((root / config.CLASS_NAMES[0]).iterdir())
        corrupted_path.write_bytes(b"not a real image")

        dataset = HandwritingDataset(str(root))
        found_sentinel = False
        for i in range(len(dataset)):
            _, label = dataset[i]
            if label == -1:
                found_sentinel = True
                break
        self.assertTrue(found_sentinel, "Corrupted image should yield sentinel label -1")


if __name__ == "__main__":
    unittest.main()
