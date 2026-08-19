"""
Module Name : gradcam.py
Project     : DysWrite Pre-Screening Engine
Created     : 2026-08-17
Author      : DysWrite Research Group (DMMMSU-SLUC College of Computer Science)
Summary     : Wraps torchcam's GradCAM to produce an explainability heatmap
              for a single prediction, and overlays it on the original image
              for display in the DysWrite app / CLI output. This is the XAI
              component referenced in the DysWrite thesis (Grad-CAM).
Functions   : generate_gradcam_overlay(model, image_tensor, original_image, target_layer)
"""

from typing import Tuple

import numpy as np
import torch
from PIL import Image
from torchcam.methods import GradCAM

from src import config
from src.utils import get_logger

logger = get_logger(__name__)


def generate_gradcam_overlay(
    model: torch.nn.Module,
    image_tensor: torch.Tensor,
    original_image: Image.Image,
    target_layer: str = config.GRADCAM_TARGET_LAYER,
) -> Tuple[np.ndarray, int]:
    """
    Run Grad-CAM on a single preprocessed image tensor and return a heatmap
    overlay ready for display, plus the predicted class index.

    Args:
        model: a model already moved to the correct device, in eval mode is
            NOT required here because Grad-CAM needs gradients enabled.
        image_tensor: a single preprocessed image, shape (1, 3, H, W).
        original_image: the corresponding un-normalized PIL image, used only
            to size the returned heatmap for overlay.
        target_layer: name of the convolutional layer to extract activations
            from. Defaults to config.GRADCAM_TARGET_LAYER instead of a
            hardcoded string, so the layer name lives in exactly one place.

    Returns:
        (heatmap, predicted_class_index)

    Raises:
        RuntimeError: re-raised with additional context if `target_layer`
            does not exist on `model` (a common, easy-to-make mistake when
            swapping architectures).
    """
    try:
        cam_extractor = GradCAM(model, target_layer=target_layer)
    except ValueError as exc:
        raise RuntimeError(
            f"Grad-CAM target layer '{target_layer}' was not found on the "
            f"model. Check config.GRADCAM_TARGET_LAYER against the model's "
            f"actual layer names."
        ) from exc

    outputs = model(image_tensor)
    predicted_class = int(outputs.argmax(dim=1)[0].item())

    activation_map = cam_extractor(predicted_class, outputs)
    heatmap = activation_map[0].mean(dim=0).detach().cpu().numpy()

    # Resize heatmap to match the original image dimensions for a clean overlay.
    heatmap_img = Image.fromarray(np.uint8(255 * heatmap / (heatmap.max() + 1e-8)))
    heatmap_img = heatmap_img.resize(original_image.size)
    heatmap_resized = np.array(heatmap_img) / 255.0

    cam_extractor.remove_hooks()
    return heatmap_resized, predicted_class
