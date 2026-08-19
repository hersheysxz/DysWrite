"""
Module Name : train.py
Project     : DysWrite Pre-Screening Engine
Created     : 2026-08-17
Author      : DysWrite Research Group (DMMMSU-SLUC College of Computer Science)
Summary     : Fine-tunes the MobileNetV3-Small model on DysWrite's handwriting
              dataset with a real, working early-stopping implementation
              (unlike the reference notebook's unused early-stopping
              variables), per-epoch checkpointing of the best model, and
              defensive skipping of corrupted samples in BOTH the training
              and validation loops.
Functions   : run_training()
Usage       : python -m src.train
"""

import time

import torch
from torch import nn, optim
from torch.utils.data import DataLoader, random_split

from src import config
from src.dataset import HandwritingDataset, build_transform
from src.exceptions import DatasetError
from src.model import build_model, save_checkpoint
from src.utils import get_logger

logger = get_logger(__name__)


def _run_one_epoch(model, loader, criterion, optimizer, device, train: bool):
    """
    Shared epoch loop for both training and validation (DRY: avoids two
    near-identical copies of this loop, unlike the reference notebook where
    the corrupted-label guard existed only in the training branch).
    """
    model.train() if train else model.eval()
    running_loss, correct, total = 0.0, 0, 0

    context = torch.enable_grad() if train else torch.no_grad()
    with context:
        for inputs, labels in loader:
            valid_mask = labels != -1
            if valid_mask.sum() == 0:
                continue  # entire batch was corrupted/unreadable; skip safely
            inputs, labels = inputs[valid_mask].to(device), labels[valid_mask].to(device)

            if train:
                optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            if train:
                loss.backward()
                optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            _, predicted = torch.max(outputs, 1)
            correct += (predicted == labels).sum().item()
            total += labels.size(0)

    if total == 0:
        # Defensive guard: every sample in this split was unreadable.
        # Return neutral values instead of raising ZeroDivisionError.
        logger.warning("An entire %s split produced zero valid samples this epoch.",
                        "training" if train else "validation")
        return float("inf"), 0.0

    avg_loss = running_loss / total
    accuracy = correct / total
    return avg_loss, accuracy


def run_training() -> None:
    torch.manual_seed(config.RANDOM_SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info("Using device: %s", device)

    try:
        dataset = HandwritingDataset(config.DATA_DIR, transform=build_transform())
    except DatasetError as exc:
        logger.error("Cannot start training: %s", exc)
        return  # fail gracefully instead of an unhandled crash

    train_size = int(config.TRAIN_SPLIT * len(dataset))
    val_size = int(config.VAL_SPLIT * len(dataset))
    test_size = len(dataset) - train_size - val_size
    train_ds, val_ds, _test_ds = random_split(
        dataset, [train_size, val_size, test_size],
        generator=torch.Generator().manual_seed(config.RANDOM_SEED),
    )

    train_loader = DataLoader(train_ds, batch_size=config.BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=config.BATCH_SIZE, shuffle=False)

    model = build_model().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=config.LEARNING_RATE)

    best_val_loss = float("inf")
    epochs_without_improvement = 0
    start_time = time.time()

    try:
        for epoch in range(1, config.NUM_EPOCHS + 1):
            train_loss, train_acc = _run_one_epoch(model, train_loader, criterion, optimizer, device, train=True)
            val_loss, val_acc = _run_one_epoch(model, val_loader, criterion, optimizer, device, train=False)

            logger.info(
                "Epoch %d/%d | train_loss=%.4f train_acc=%.2f%% | val_loss=%.4f val_acc=%.2f%%",
                epoch, config.NUM_EPOCHS, train_loss, train_acc * 100, val_loss, val_acc * 100,
            )

            if val_loss < best_val_loss - config.EARLY_STOPPING_MIN_DELTA:
                best_val_loss = val_loss
                epochs_without_improvement = 0
                save_checkpoint(model, config.CHECKPOINT_DIR / "best_model.pth")
            else:
                epochs_without_improvement += 1
                logger.info(
                    "No improvement for %d/%d epochs.",
                    epochs_without_improvement, config.EARLY_STOPPING_PATIENCE,
                )
                if epochs_without_improvement >= config.EARLY_STOPPING_PATIENCE:
                    logger.info("Early stopping triggered at epoch %d.", epoch)
                    break
    finally:
        # Runs whether training finished normally, was early-stopped, or
        # crashed with an unexpected error -- guarantees timing is reported.
        duration_min = (time.time() - start_time) / 60
        logger.info("Training run finished after %.2f minutes.", duration_min)


if __name__ == "__main__":
    run_training()
