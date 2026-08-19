# GitHub Deployment Instructions

This document explains how to upload the DysWrite Pre-Screening project to your group's GitHub repository and how all team members can run it.

## Step 1: Initialize Git (If Not Already Done)

```bash
cd dyswrite-prescreen
git init
git add .
git commit -m "Initial commit: DysWrite pre-screening engine with quality assurance audit"
```

## Step 2: Create a Repository on GitHub

1. Go to [GitHub](https://github.com) and log in
2. Click the **+** icon in the top-right corner → **New repository**
3. Name it: `dyswrite-prescreen` (or your group's naming convention)
4. Set visibility to **Private** (if this is a group-only project)
5. Do NOT initialize with README (you already have one)
6. Click **Create repository**

## Step 3: Connect Local Repo to GitHub

GitHub will show you these commands after creating the repo. Copy and run them:

```bash
git remote add origin https://github.com/YOUR_GROUP/dyswrite-prescreen.git
git branch -M main
git push -u origin main
```

Replace `YOUR_GROUP` with your actual GitHub organization/username.

## Step 4: Add Team Members as Collaborators

1. Go to your repository on GitHub
2. Click **Settings** → **Collaborators** (or **Collaborators and teams**)
3. Click **Add people**
4. Type each team member's GitHub username and grant them **Maintainer** or **Write** access

---

## For Each Team Member: Running the Project

After receiving repository access, each team member should:

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_GROUP/dyswrite-prescreen.git
cd dyswrite-prescreen
```

### 2. Create and Activate a Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note on Build Tools:** If you encounter a numpy build error on Windows, install the Microsoft C++ Build Tools:
- Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Run the installer and select "Desktop development with C++"
- Then retry: `pip install -r requirements.txt`

### 4. Verify Installation

```bash
python -c "from src import config, exceptions, utils, dataset, model; print(' Installation successful')"
```

### 5. Run the Unit Tests

```bash
python -m unittest discover -s tests -v
```

All tests should pass. If they do not, check your virtual environment and dependencies.

---

## Dataset Setup (All Members)

Before training, prepare your dataset:

```
sample_data/
├── normal/        (handwriting samples without dyslexia markers)
├── reversal/      (handwriting with letter/word reversals)
└── corrected/     (handwriting with correction marks)
```

Each class folder must contain `.jpg` or `.png` files.

### Minimal Test Dataset

For testing the pipeline without real data:

```bash
mkdir -p sample_data/normal sample_data/reversal sample_data/corrected

# Create small test images (32x32 pixels)
python -c "
from PIL import Image
import os

for cls in ['normal', 'reversal', 'corrected']:
    for i in range(3):
        img = Image.new('RGB', (224, 224), color=(i*50, i*50, i*50))
        img.save(f'sample_data/{cls}/test_{i}.png')
    print(f'Created 3 test images in sample_data/{cls}')
"
```

---

## Training the Model

```bash
python -m src.train
```

- Trains for up to 15 epochs with early stopping
- Saves the best checkpoint to `checkpoints/best_model.pth`
- Logs validation metrics to stdout

### Expected Output

```
2026-08-19 14:22:30 | INFO    | src.train | Loaded dataset: 9 images across 3 classes (normal, reversal, corrected)
2026-08-19 14:22:45 | INFO    | src.train | Using device: cpu
Epoch 1/15 | train_loss=1.0523 train_acc=33.33% | val_loss=0.9821 val_acc=33.33%
...
Epoch 3/15 | Saved checkpoint to checkpoints/best_model.pth
2026-08-19 14:23:15 | INFO    | src.train | Training run finished after 0.75 minutes.
```

---

## Running Pre-Screening (Inference)

To run inference on a single image:

```bash
python -m src.infer \
    --image path/to/handwriting_sample.jpg \
    --checkpoint checkpoints/best_model.pth \
    --output outputs/result.png
```

**Example:**

```bash
python -m src.infer \
    --image sample_data/normal/test_0.png \
    --checkpoint checkpoints/best_model.pth \
    --output outputs/demo_result.png
```

Output:
```
2026-08-19 14:25:10 | INFO    | src.infer | Loaded checkpoint from checkpoints/best_model.pth
2026-08-19 14:25:10 | INFO    | src.infer | Predicted class: normal (confidence: 45.2%)
2026-08-19 14:25:10 | INFO    | src.infer | Saved annotated result to outputs/demo_result.png
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'torch'` | Ensure virtual environment is activated: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux) |
| `ClassMismatchError: Class folders ... do not match` | Verify `sample_data/` contains exactly these folders: `normal/`, `reversal/`, `corrected/` |
| `DatasetError: No images found under` | Add training images to the class folders |
| Tests hang during model import | This is normal on first run (downloading pretrained ImageNet weights). Let it complete. Subsequent runs are faster. |
| `numpy` build fails on Windows | Install Microsoft C++ Build Tools (see Step 3 above) |

---

## Git Workflow for Team Members

When multiple members work on the code:

```bash
# Pull latest changes
git pull origin main

# Create a feature branch
git checkout -b feature/your-feature-name

# Make changes and test
# ...

# Commit your work
git add .
git commit -m "Descriptive message about your changes"

# Push to GitHub
git push origin feature/your-feature-name

# Create a Pull Request on GitHub for code review
```

---

## Questions?

Refer to the [main README.md](README.md) for project overview, or see [QUALITY_AUDIT.md](QUALITY_AUDIT.md) for code quality analysis.
