# DysWrite Pre-Screening Engine

Minimal, runnable inference/training pipeline for DysWrite's dyslexia
handwriting pre-screening feature. Fine-tunes a MobileNetV3-Small model
(architecture choice follows Robaa et al., adapted here to DysWrite's own
3-class label space) and generates a Grad-CAM explainability overlay for
every prediction.

This is the project code referenced in our Module 2 code-quality audit
report.

---

## 📚 Documentation

- **🚀 [GITHUB_UPLOAD_GUIDE.md](GITHUB_UPLOAD_GUIDE.md)** — How to upload this project to GitHub and invite team members
- **💻 [DEPLOYMENT.md](DEPLOYMENT.md)** — How to install and run the project (for all team members)
- **✅ [QUALITY_AUDIT.md](QUALITY_AUDIT.md)** — **WHERE THE CODE IMPLEMENTS**:
  - Professional Coding Standards and Practices
  - 15 Principles of Quality Software
  - Defensive Programming
  - Error Exception Handling
- **🤝 [CONTRIBUTING.md](CONTRIBUTING.md)** — Code style guide and Git workflow for team members

---

## 1. Project Structure

```
dyswrite-prescreen/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── config.py        # all constants (paths, classes, hyperparameters)
│   ├── exceptions.py     # project-specific exception hierarchy
│   ├── utils.py          # logging + defensive image loading
│   ├── dataset.py        # HandwritingDataset (PyTorch Dataset)
│   ├── model.py           # MobileNetV3-Small builder + checkpoint I/O
│   ├── gradcam.py         # Grad-CAM explainability wrapper
│   ├── train.py           # training script with early stopping
│   └── infer.py           # CLI: run pre-screening on one image
├── tests/
│   ├── test_dataset.py
│   └── test_model.py
├── sample_data/           # put your class-labeled training images here
├── checkpoints/           # trained model weights are saved here (gitignored)
└── outputs/                # annotated Grad-CAM results are saved here
```

## 2. Setup (every group member should run this on their own machine)

**Start here: [DEPLOYMENT.md](DEPLOYMENT.md)** contains complete setup instructions for all team members.

Quick summary:

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_GROUP/dyswrite-prescreen.git
cd dyswrite-prescreen

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run tests to verify installation
python -m unittest discover -s tests
```

Requires Python 3.9+. A GPU is optional — the code automatically falls
back to CPU (see `src/train.py` / `src/infer.py`, `torch.cuda.is_available()`).

See [DEPLOYMENT.md](DEPLOYMENT.md#troubleshooting) for common issues and solutions.

## 3. Preparing the Dataset

Place labeled handwriting images under `sample_data/`, matching the class
names in `src/config.py` (`CLASS_NAMES`):

```
sample_data/
├── normal/
├── reversal/
└── corrected/
```

If your folder names don't match `CLASS_NAMES` exactly, `dataset.py` will
raise a `ClassMismatchError` at startup rather than training silently
against the wrong labels — this is intentional (see Defensive Programming
section of the audit report).

## 4. Training

```bash
python -m src.train
```

- Trains with an 80/10/10 train/val/test split (`config.TRAIN_SPLIT`,
  `config.VAL_SPLIT`).
- Uses real early stopping: training halts once validation loss stops
  improving for `config.EARLY_STOPPING_PATIENCE` epochs.
- Saves the best-performing checkpoint to `checkpoints/best_model.pth`.

## 5. Running Pre-Screening on a Single Image

```bash
python -m src.infer --image path/to/handwriting_sample.jpg \
                     --checkpoint checkpoints/best_model.pth \
                     --output outputs/result.png
```

This prints the predicted class and confidence to the console/log, and
saves a side-by-side image (original + Grad-CAM heatmap overlay) to
`outputs/result.png`.

## 6. Running the Tests

```bash
python -m unittest discover -s tests
```

All tests should pass without needing a trained checkpoint or GPU — they
use small synthetic images and a freshly-initialized model.

## 7. Code Quality & Development

This project demonstrates professional software engineering practices:

### Professional Coding Standards
- Module documentation headers, type hints, comprehensive docstrings
- Centralized configuration (no hardcoded magic numbers)
- Consistent naming conventions (PEP 8)
- Unified logging system

### Quality Software Principles
- Early validation and error detection ("fail fast")
- Robust handling of edge cases (corrupted images, missing files)
- Reliable training with early stopping and checkpointing
- Comprehensive test coverage (success and error cases)

### Defensive Programming
- Input validation at earliest point
- Custom exception hierarchy (not generic `Exception`)
- Graceful degradation (skip corrupted samples instead of crashing)

### Error Exception Handling
- Custom exception types for project-specific errors
- Try/except blocks in all main loops
- Clear, actionable error messages

**Read [QUALITY_AUDIT.md](QUALITY_AUDIT.md) for detailed examples of each principle and where they appear in the code.**

### Contributing to the Project

All team members should read [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style guidelines and naming conventions
- How to write tests
- Git workflow and pull request process
- Common development tasks

## 8. Notes for Group Members

- All configuration values (paths, class names, image size, hyperparameters)
  live in `src/config.py` — change values there, not inside individual
  scripts.
- If you hit a `ModelCheckpointError`, `DatasetError`, or
  `ClassMismatchError`, the printed message explains exactly what's wrong
  and where — see `src/exceptions.py`.
- Logs are printed to the console via `src/utils.get_logger()`; no need to
  add `print()` statements when debugging — use `logger.info(...)` /
  `logger.warning(...)` instead so output stays consistent.
- **[Read CONTRIBUTING.md for code contribution guidelines](CONTRIBUTING.md)**
