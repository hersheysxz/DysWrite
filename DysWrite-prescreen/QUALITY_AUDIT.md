# DysWrite Pre-Screening: Code Quality Analysis

This document identifies where the DysWrite pre-screening codebase implements professional coding standards, quality software principles, defensive programming, and error handling.

---

## 1. Professional Coding Standards and Practices

### 1.1 Module Documentation and Code Organization

**Location:** All `.py` files in `src/` and `tests/`

**Evidence:**
- Every module starts with a standardized header (Module Name, Project, Created date, Author, Summary, Functions)
- Example: [`src/dataset.py`](src/dataset.py#L1-L12)
- Example: [`src/exceptions.py`](src/exceptions.py#L1-L10)

**Standard Being Followed:**
- PEP 257: Docstring Conventions
- Clear separation of concerns (each file has a single responsibility)

### 1.2 Centralized Configuration

**Location:** [`src/config.py`](src/config.py)

**Evidence:**
- All "magic numbers" and constants are defined in ONE place
- Instead of hardcoding values in scripts, every module imports from `config`
- Comments explain the purpose of each constant group

**Code Example:**
```python
# From src/config.py (centralized)
CLASS_NAMES = ["normal", "reversal", "corrected"]
BATCH_SIZE = 16
LEARNING_RATE = 1e-4

# Instead of (anti-pattern - hardcoded everywhere):
# BATCH_SIZE = 16  # in train.py
# BATCH_SIZE = 16  # in test_model.py
# BATCH_SIZE = 16  # in infer.py (inconsistent!)
```

**Standard:** DRY Principle (Don't Repeat Yourself)

### 1.3 Consistent Naming Conventions

**Locations:** All files

**Evidence:**
- Variable names are descriptive: `train_loss`, `val_acc`, `predicted_label` (not `x`, `y`, `loss1`)
- Function names use snake_case: `build_transform()`, `safe_open_image()`, `_run_one_epoch()`
- Class names use PascalCase: `HandwritingDataset`, `DysWriteError`
- Private/internal functions prefixed with `_`: `_run_one_epoch()`, `_index_samples()`

**Standard:** PEP 8 Python Naming Conventions

### 1.4 Type Hints (Optional Static Typing)

**Location:** All `.py` files

**Evidence:**
```python
# From src/dataset.py
def build_transform() -> transforms.Compose:
    """..."""

def __init__(self, root_folder: str, transform: Optional[transforms.Compose] = None):
    """..."""

def _index_samples(self) -> List[Tuple[Path, int]]:
    """..."""
```

**Benefit:** Code is self-documenting; IDEs can catch type errors before runtime

**Standard:** PEP 484 Type Hints

### 1.5 Comprehensive Docstrings

**Location:** All functions and classes

**Example from** [`src/utils.py`](src/utils.py#L24-L46):
```python
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
```

**Standard:** Google/NumPy Docstring Format

### 1.6 Logging Instead of Print Statements

**Location:** All production code (`src/train.py`, `src/infer.py`, `src/dataset.py`)

**Evidence:**
```python
# From src/train.py
logger = get_logger(__name__)
logger.info("Using device: %s", device)
logger.info("Epoch %d/%d | train_loss=%.4f ...", epoch, config.NUM_EPOCHS, train_loss, ...)
```

**Benefit:** Consistent output format, can easily redirect to file or change verbosity without code changes

**Standard:** Python Logging Best Practices

---

## 2. 15 Principles of Quality Software

### 2.1 Correctness

**Implementations:**
- **Early validation**: [`src/dataset.py`](src/dataset.py#L72-L77) validates that class folders match `config.CLASS_NAMES` at construction time
- **Unit tests**: [`tests/test_dataset.py`](tests/test_dataset.py) and [`tests/test_model.py`](tests/test_model.py) verify correct behavior
- **Example test:** [`tests/test_dataset.py#L50-L57`](tests/test_dataset.py#L50-L57) ensures class mismatch is caught early

### 2.2 Robustness

**Implementations:**
- **Corrupted image handling**: [`src/dataset.py#L119-L129`](src/dataset.py#L119-L129) gracefully skips unreadable images instead of crashing
- **Sentinel labels**: Corrupted images are assigned label `-1` for upstream filtering
- **Defensive checkpoint loading**: [`src/model.py#L60-L75`](src/model.py#L60-L75) validates file exists before attempting load

**Example:**
```python
# From src/dataset.py - handles corruption gracefully
try:
    image = safe_open_image(image_path)
except InvalidImageError as exc:
    logger.warning("Skipping unreadable sample: %s", exc)
    image = transforms.functional.to_pil_image(torch.zeros(3, *config.IMAGE_SIZE))
    label = -1  # sentinel: caller MUST filter this out before training
```

### 2.3 Reliability

**Implementations:**
- **Early stopping**: [`src/train.py#L73-L99`](src/train.py#L73-L99) real, working implementation (unlike reference notebook)
- **Per-epoch checkpointing**: Best model is saved as validation improves
- **Test split validation**: [`src/config.py#L42-L56`](src/config.py#L42-L56) prevents invalid train/val/test splits at import time

**Example:**
```python
# From src/config.py - caught BEFORE training starts
def validate_split_ratios() -> None:
    test_split = 1.0 - TRAIN_SPLIT - VAL_SPLIT
    if test_split <= 0:
        raise ValueError(f"Invalid split configuration: ... Adjust config.py.")

validate_split_ratios()  # runs at import time
```

### 2.4 Usability

**Implementations:**
- **Clear error messages**: All custom exceptions include actionable guidance
- **CLI with defaults**: [`src/infer.py#L32-L49`](src/infer.py#L32-L49) has sensible defaults for checkpoint path and output location
- **Logging output**: [`src/utils.py#L12-L23`](src/utils.py#L12-L23) unified logging format across all modules

**Example error message:**
```python
# From src/dataset.py
if set(discovered) != set(config.CLASS_NAMES):
    raise ClassMismatchError(
        f"Class folders discovered on disk {discovered} do not match "
        f"config.CLASS_NAMES {config.CLASS_NAMES}. Update config.py or "
        f"fix the dataset folder structure before continuing."
    )
# ↑ Tells user EXACTLY what's wrong and how to fix it
```

### 2.5 Efficiency

**Implementations:**
- **MobileNetV3-Small**: Lightweight model suitable for edge devices (per Robaa et al.)
- **Transfer learning**: Reuses ImageNet pretraining instead of training from scratch
- **Batch processing**: Uses PyTorch DataLoader for efficient batching

### 2.6 Portability

**Implementations:**
- **Cross-platform paths**: All paths use `pathlib.Path` (Windows/Mac/Linux compatible)
- **Device detection**: [`src/train.py#L54`](src/train.py#L54) and [`src/infer.py#L56`](src/infer.py#L56) auto-detect GPU vs CPU
- **Virtual environment isolation**: `.gitignore` excludes environment folder; instructions use `venv`

**Example:**
```python
# From src/model.py - works on Windows/Mac/Linux
from pathlib import Path

def save_checkpoint(model: nn.Module, path: Union[str, Path]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)  # cross-platform
```

### 2.7 Maintainability

**Implementations:**
- **Centralized config**: [`src/config.py`](src/config.py) is the single source of truth
- **Utility functions**: [`src/utils.py`](src/utils.py) avoids code duplication (DRY principle)
- **Clear module boundaries**: Each file has one responsibility
- **No magic strings/numbers**: Everything is named and documented

### 2.8 Testability

**Implementations:**
- **Unit tests** [`tests/test_model.py`](tests/test_model.py) and [`tests/test_dataset.py`](tests/test_dataset.py)
- **Dependency isolation**: Tests use temporary directories and synthetic data (no external dependencies)
- **Test coverage**: Tests verify both success paths AND error paths

**Example:**
```python
# From tests/test_dataset.py - tests the error case
def test_class_mismatch_raises_class_mismatch_error(self):
    root = self.tmp_dir / "wrong_classes"
    (root / "cat").mkdir(parents=True)
    (root / "dog").mkdir(parents=True)
    with self.assertRaises(ClassMismatchError):
        HandwritingDataset(str(root))
```

### 2.9 Analyzability

**Implementations:**
- **Grad-CAM explainability**: [`src/gradcam.py`](src/gradcam.py) generates visual explanations for every prediction
- **Structured output**: [`src/infer.py#L103-L121`](src/infer.py#L103-L121) saves side-by-side visualizations (input + heatmap)
- **Logging of decisions**: Every training epoch and inference run logs metrics

### 2.10 Modifiability

**Implementations:**
- **Centralized config**: Change `BATCH_SIZE`, learning rate, etc. in one place
- **Pluggable transforms**: [`src/dataset.py#L29-L36`](src/dataset.py#L29-L36) can pass custom preprocessing pipeline
- **Optional weights parameter**: [`src/model.py#L26-L36`](src/model.py#L26-L36) allows training from scratch or with pretrained weights

### 2.11 Compliance

**Implementations:**
- **Follows academic precedent**: Robaa et al. architecture as reference
- **Standards compliance**: PEP 8, PEP 257, PEP 484 (Python style, docstrings, type hints)
- **License-ready**: Code structure ready for open-source publication

### 2.12 Flexibility

**Implementations:**
- **Model configuration**: Can be adapted to different number of classes
- **Transform pipeline**: Easy to add data augmentation to `build_transform()`
- **Device flexibility**: GPU/CPU auto-detection; no hardcoded device assumptions

### 2.13 Interoperability

**Implementations:**
- **Standard PyTorch format**: Checkpoints saved as `.pth` (PyTorch standard)
- **Standard image formats**: Supports PNG, JPG, JPEG, BMP
- **CLI interface**: Can be integrated into larger systems as subprocess

### 2.14 Safety

**Implementations:**
- **No arbitrary code execution**: Config is just Python constants, not JSON/YAML eval
- **Type hints**: Reduces type-confusion bugs
- **Explicit error types**: Custom exception hierarchy prevents swallowing errors

### 2.15 Elegance

**Implementations:**
- **Pythonic code**: Uses context managers (`with`), list comprehensions, pathlib
- **Clear intent**: Function names and variable names express what code does
- **Minimal coupling**: Modules import only what they need

---

## 3. Defensive Programming

### 3.1 Eliminate Assumptions

**Pattern:** Never assume input is valid. Verify at the earliest possible point.

**Location:** [`src/dataset.py#L72-L88`](src/dataset.py#L72-L88)

```python
# DEFENSIVE: Verify folder exists BEFORE trying to use it
if not self.root_folder.exists():
    raise DatasetError(f"Dataset root folder does not exist: {self.root_folder}")

# DEFENSIVE: Verify class folders match config BEFORE training starts
discovered = sorted(p.name for p in self.root_folder.iterdir() if p.is_dir())
if set(discovered) != set(config.CLASS_NAMES):
    raise ClassMismatchError(
        f"Class folders discovered on disk {discovered} do not match "
        f"config.CLASS_NAMES {config.CLASS_NAMES}. Update config.py or "
        f"fix the dataset folder structure before continuing."
    )

# DEFENSIVE: Verify dataset is non-empty BEFORE training starts
if len(self.samples) == 0:
    raise DatasetError(
        f"No images found under {self.root_folder}. Populate the "
        f"class subfolders before training."
    )
```

**Anti-pattern avoided:** Silently proceeding with empty dataset, then crashing deep inside training loop with confusing error.

### 3.2 Fail Fast, Fail Clearly

**Location:** [`src/config.py#L42-L56`](src/config.py#L42-L56)

```python
# DEFENSIVE: Split validation runs at import time
def validate_split_ratios() -> None:
    test_split = 1.0 - TRAIN_SPLIT - VAL_SPLIT
    if test_split <= 0:
        raise ValueError(
            f"Invalid split configuration: TRAIN_SPLIT ({TRAIN_SPLIT}) + "
            f"VAL_SPLIT ({VAL_SPLIT}) leaves no room for a test split "
            f"({test_split:.2f}). Adjust config.py."
        )

validate_split_ratios()  # ← runs immediately at import, before any training code
```

**Benefit:** If config is wrong, it's caught when running the script (not 2 hours into training).

### 3.3 Normalize Exceptions

**Location:** [`src/utils.py#L24-L49`](src/utils.py#L24-L49)

```python
def safe_open_image(path: Union[str, Path]) -> Image.Image:
    # DEFENSIVE: Don't let PIL's exceptions leak out
    path = Path(path)
    if not path.exists():
        raise InvalidImageError(f"Image file does not exist: {path}")

    try:
        with Image.open(path) as img:
            return img.convert("RGB")
    except (OSError, UnidentifiedImageError) as exc:
        # DEFENSIVE: Convert all PIL exceptions to ONE custom exception type
        # Caller only needs: except InvalidImageError
        raise InvalidImageError(f"Could not decode image at {path}: {exc}") from exc
```

**Benefit:** Caller code doesn't need to know about PIL internals. One exception type to catch.

### 3.4 Handle Corrupted Data Gracefully

**Location:** [`src/dataset.py#L119-L129`](src/dataset.py#L119-L129)

```python
def __getitem__(self, index: int):
    image_path, label = self.samples[index]
    try:
        image = safe_open_image(image_path)
    except InvalidImageError as exc:
        # DEFENSIVE: Corrupted image doesn't crash training
        logger.warning("Skipping unreadable sample: %s", exc)
        image = transforms.functional.to_pil_image(torch.zeros(3, *config.IMAGE_SIZE))
        label = -1  # sentinel: caller MUST filter this out before training
    
    # ... rest of method
```

**Why it matters:** One corrupted JPEG shouldn't crash a training run on 10,000 images.

### 3.5 Validate Before Deep Operations

**Location:** [`src/model.py#L60-L75`](src/model.py#L60-L75)

```python
def load_checkpoint(model: nn.Module, path: Union[str, Path], device: torch.device) -> nn.Module:
    path = Path(path)
    
    # DEFENSIVE: Check file exists BEFORE attempting expensive torch.load()
    if not path.exists():
        raise ModelCheckpointError(f"Checkpoint file not found: {path}")
    
    try:
        state_dict = torch.load(path, map_location=device)
        model.load_state_dict(state_dict)
    except (RuntimeError, EOFError, OSError) as exc:
        # DEFENSIVE: Catch and re-raise as custom exception
        raise ModelCheckpointError(f"Failed to load checkpoint {path}: {exc}") from exc
    
    model.to(device)
    logger.info("Loaded checkpoint from %s", path)
    return model
```

**Benefit:** Fast, clear error message (checkpoint doesn't exist) instead of torch.load() hanging/crashing mysteriously.

### 3.6 Defensive Loop Guards

**Location:** [`src/train.py#L43-L53`](src/train.py#L43-L53)

```python
def _run_one_epoch(model, loader, criterion, optimizer, device, train: bool):
    model.train() if train else model.eval()
    running_loss, correct, total = 0.0, 0, 0

    context = torch.enable_grad() if train else torch.no_grad()
    with context:
        for inputs, labels in loader:
            # DEFENSIVE: Filter out sentinel labels (corrupted images)
            valid_mask = labels != -1
            if valid_mask.sum() == 0:
                # DEFENSIVE: Entire batch was corrupted; skip safely
                continue
            
            inputs, labels = inputs[valid_mask].to(device), labels[valid_mask].to(device)
            # ... training code
```

**Benefit:** If entire batch is corrupted, skip instead of crashing with shape mismatch.

### 3.7 Final-Block Guarantees

**Location:** [`src/train.py#L91-X`](src/train.py#L91-X)

```python
try:
    for epoch in range(1, config.NUM_EPOCHS + 1):
        # ... training loop
finally:
    # DEFENSIVE: Guaranteed to run, even if crash occurs
    duration_min = (time.time() - start_time) / 60
    logger.info("Training run finished after %.2f minutes.", duration_min)
```

**Benefit:** You always know how long training took, even if it crashed.

---

## 4. Error Exception Handling

### 4.1 Custom Exception Hierarchy

**Location:** [`src/exceptions.py`](src/exceptions.py)

```python
class DysWriteError(Exception):
    """Base class for all custom exceptions raised by this project."""

class DatasetError(DysWriteError):
    """Raised when the dataset directory is missing, empty, or malformed."""

class ClassMismatchError(DysWriteError):
    """Raised when class folders don't match config.CLASS_NAMES."""

class ModelCheckpointError(DysWriteError):
    """Raised when a checkpoint file is missing, unreadable, or corrupt."""

class InvalidImageError(DysWriteError):
    """Raised when an input image cannot be opened or decoded."""
```

**Benefit:** Code can catch `DysWriteError` to handle all project errors, or catch specific error types:

```python
try:
    dataset = HandwritingDataset(config.DATA_DIR, ...)
except ClassMismatchError:
    # Handle class mismatch specifically
except DatasetError:
    # Handle other dataset issues
except DysWriteError:
    # Handle any project error
```

### 4.2 Exception Handling in Main Loops

**Location:** [`src/train.py#L71-L95`](src/train.py#L71-L95)

```python
def run_training() -> None:
    # ...
    try:
        dataset = HandwritingDataset(config.DATA_DIR, transform=build_transform())
    except DatasetError as exc:
        # EXCEPTION HANDLING: Catch known error and exit gracefully
        logger.error("Cannot start training: %s", exc)
        return  # fail gracefully instead of an unhandled crash
    
    # ... more training code ...
    
    try:
        for epoch in range(1, config.NUM_EPOCHS + 1):
            # ... epoch loop ...
    finally:
        # EXCEPTION HANDLING: Cleanup runs even if training crashes
        duration_min = (time.time() - start_time) / 60
        logger.info("Training run finished after %.2f minutes.", duration_min)
```

### 4.3 Exception Handling in Inference

**Location:** [`src/infer.py#L63-L87`](src/infer.py#L63-L87)

```python
def main() -> int:
    # ...
    # Load model with exception handling
    try:
        model = build_model()
        model = load_checkpoint(model, args.checkpoint, device)
    except ModelCheckpointError as exc:
        logger.error("Could not load model: %s", exc)
        return 1  # exit with error code
    
    # Load image with exception handling
    try:
        original_image = safe_open_image(args.image)
    except InvalidImageError as exc:
        logger.error("Could not read input image: %s", exc)
        return 1

    # Run inference with exception handling
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
        # EXCEPTION HANDLING: Catch unexpected PyTorch errors
        logger.error("An unexpected model error occurred: %s", exc)
        return 1
```

### 4.4 Validation Exceptions

**Location:** [`src/model.py#L26-L35`](src/model.py#L26-L35)

```python
def build_model(num_classes: int = config.NUM_CLASSES, weights=None) -> nn.Module:
    # EXCEPTION HANDLING: Validate inputs early
    if num_classes < 2:
        raise ValueError(f"num_classes must be >= 2, got {num_classes}")
    
    # ... build model ...
```

### 4.5 Test Coverage for Exception Cases

**Location:** [`tests/test_dataset.py`](tests/test_dataset.py) and [`tests/test_model.py`](tests/test_model.py)

```python
# EXCEPTION HANDLING TEST: Ensure custom exceptions are raised as expected
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

def test_load_checkpoint_missing_file_raises_custom_error(self):
    model = build_model(num_classes=3)
    missing_path = self.tmp_dir / "does_not_exist.pth"
    with self.assertRaises(ModelCheckpointError):
        load_checkpoint(model, missing_path, torch.device("cpu"))

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
```

---

## Summary: Quality Metrics

| Aspect | Coverage | Evidence |
|--------|----------|----------|
| **Professional Coding Standards** | ✓ Excellent | PEP 8/257/484 compliance; module headers; centralized config |
| **Quality Software Principles** | ✓ Excellent | 15/15 principles demonstrated (correctness, robustness, reliability, etc.) |
| **Defensive Programming** | ✓ Excellent | Early validation, fail-fast, exception normalization, corrupted data handling |
| **Error Exception Handling** | ✓ Excellent | Custom exception hierarchy; comprehensive try/except blocks; test coverage for error paths |
| **Test Coverage** | ✓ Good | Unit tests for both success and error cases; no external dependencies in tests |
| **Documentation** | ✓ Excellent | Module docstrings, inline comments, Google-style function docstrings |
| **Code Organization** | ✓ Excellent | Clear separation of concerns; single responsibility per module |

---

## Code Review Checklist

Use this checklist when reviewing code contributions:

- [ ] New functions have type hints and docstrings
- [ ] New constants go into `src/config.py`, not hardcoded
- [ ] Errors raise custom exceptions, not generic `Exception`
- [ ] Logging is used instead of `print()`
- [ ] Pathlib is used for file paths (cross-platform)
- [ ] No bare `except:` clauses (always specify exception type)
- [ ] Unit tests cover both success AND error cases
- [ ] Code follows PEP 8 naming conventions (snake_case, PascalCase, etc.)

