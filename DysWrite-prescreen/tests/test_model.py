"""
Module Name : test_model.py
Project     : DysWrite Pre-Screening Engine
Created     : 2026-08-17
Author      : DysWrite Research Group (DMMMSU-SLUC College of Computer Science)
Summary     : Unit tests for src/model.py -- verifies build_model() produces
              the expected output shape and that load_checkpoint() fails
              defensively (rather than crashing uncontrolled) on a missing
              checkpoint file.
Usage       : python -m unittest discover -s tests
"""

import shutil
import tempfile
import unittest
from pathlib import Path

import torch

from src.exceptions import ModelCheckpointError
from src.model import build_model, load_checkpoint, save_checkpoint


class TestModel(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_build_model_rejects_invalid_num_classes(self):
        with self.assertRaises(ValueError):
            build_model(num_classes=1)

    def test_build_model_output_shape_matches_num_classes(self):
        model = build_model(num_classes=3)
        model.eval()
        dummy_input = torch.randn(1, 3, 224, 224)
        with torch.no_grad():
            output = model(dummy_input)
        self.assertEqual(output.shape, (1, 3))

    def test_build_model_without_pretrained_weights(self):
        model = build_model(num_classes=3, weights=None)
        model.eval()
        dummy_input = torch.randn(1, 3, 224, 224)
        with torch.no_grad():
            output = model(dummy_input)
        self.assertEqual(output.shape, (1, 3))

    def test_load_checkpoint_missing_file_raises_custom_error(self):
        model = build_model(num_classes=3)
        missing_path = self.tmp_dir / "does_not_exist.pth"
        with self.assertRaises(ModelCheckpointError):
            load_checkpoint(model, missing_path, torch.device("cpu"))

    def test_save_then_load_checkpoint_round_trip(self):
        model = build_model(num_classes=3)
        ckpt_path = self.tmp_dir / "checkpoints" / "test_model.pth"
        save_checkpoint(model, ckpt_path)
        self.assertTrue(ckpt_path.exists())

        reloaded = build_model(num_classes=3)
        reloaded = load_checkpoint(reloaded, ckpt_path, torch.device("cpu"))
        self.assertIsNotNone(reloaded)


if __name__ == "__main__":
    unittest.main()
