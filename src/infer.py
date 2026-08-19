"""
Module Name : infer.py
Project     : DysWrite Pre-Screening Engine
Created     : 2026-08-17
Author      : DysWrite Research Group (DMMMSU-SLUC College of Computer Science)
Summary     : Command-line entry point. Given a path to a handwriting sample
              image and a trained checkpoint, runs the full pre-screening
              pipeline: load model -> preprocess image -> predict class ->
              generate Grad-CAM explanation -> save an annotated result image.
              This is the script other group members run to test the project.
Functions   : main()
Usage       : python -m src.infer --image path/to/sample.jpg
                                   --checkpoint checkpoints/best_model.pth
"""

import argparse
import sys

import matplotlib.pyplot as plt
import numpy as np
import torch

from src import config
from src.dataset import build_transform
from src.exceptions import DysWriteError, InvalidImageError, ModelCheckpointError
from src.gradcam import generate_gradcam_overlay
from src.model import build_model, load_checkpoint
from src.utils import get_logger, safe_open_image

logger = get_logger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="DysWrite dyslexia handwriting pre-screening (single image)."
    )
    parser.add_argument("--image", required=True, help="Path to a handwriting sample image.")
    parser.add_argument(
        "--checkpoint", default=str(config.CHECKPOINT_DIR / "best_model.pth"),
        help="Path to a trained model checkpoint (.pth).",
    )
    parser.add_argument(
        "--output", default=str(config.OUTPUT_DIR / "result.png"),
        help="Where to save the annotated Grad-CAM result image.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # --- Load model -------------------------------------------------------
    try:
        model = build_model()
        model = load_checkpoint(model, args.checkpoint, device)
    except ModelCheckpointError as exc:
        logger.error("Could not load model: %s", exc)
        return 1

    # --- Load and validate the input image ---------------------------------
    try:
        original_image = safe_open_image(args.image)
    except InvalidImageError as exc:
        logger.error("Could not read input image: %s", exc)
        return 1

    transform = build_transform()
    image_tensor = transform(original_image).unsqueeze(0).to(device)

    # --- Run prediction + Grad-CAM -----------------------------------------
    try:
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = torch.softmax(outputs, dim=1)[0]
        predicted_idx = int(torch.argmax(probabilities).item())
        confidence = float(probabilities[predicted_idx].item())

        heatmap, _ = generate_gradcam_overlay(model, image_tensor, original_image)
    except DysWriteError as exc:
        logger.error("Pre-screening failed: %s", exc)
        return 1
    except RuntimeError as exc:
        # Covers unexpected PyTorch runtime failures (e.g. shape mismatches,
        # out-of-memory) that are outside this project's control but should
        # still be reported clearly instead of a raw traceback.
        logger.error("An unexpected model error occurred: %s", exc)
        return 1

    predicted_label = config.CLASS_NAMES[predicted_idx]

    if confidence < config.MIN_CONFIDENCE_THRESHOLD:
        logger.warning(
            "Prediction confidence (%.1f%%) is below the %.0f%% threshold. "
            "Treat this result as inconclusive.",
            confidence * 100, config.MIN_CONFIDENCE_THRESHOLD * 100,
        )

    logger.info("Predicted class: %s (confidence: %.1f%%)", predicted_label, confidence * 100)

    # --- Save annotated output ----------------------------------------------
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(original_image)
    axes[0].set_title("Input Sample")
    axes[0].axis("off")

    axes[1].imshow(original_image)
    axes[1].imshow(heatmap, cmap="jet", alpha=0.5)
    axes[1].set_title(f"Predicted: {predicted_label} ({confidence * 100:.1f}%)")
    axes[1].axis("off")

    plt.tight_layout()
    plt.savefig(args.output, dpi=150)
    plt.close(fig)
    logger.info("Saved annotated result to %s", args.output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
