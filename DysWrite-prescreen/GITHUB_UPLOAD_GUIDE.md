# GitHub Upload & Team Onboarding Guide

**Quick Summary:** This guide shows you exactly how to upload the DysWrite project to your group GitHub repository and how your team members can start using it.

---

## Prerequisites

Each team member needs:
1. **GitHub account** (sign up at https://github.com)
2. **Git installed** (download from https://git-scm.com)
3. **Python 3.9+** (download from https://www.python.org)
4. **Permissions** to create repositories in your group's GitHub organization (if using an org account)

---

## Step 1: Prepare the Project for GitHub

Navigate to the project folder in your terminal and run:

```bash
cd "d:\rachel's files\dyswrite-prescreen"

# Verify Git is set up
git status
```

If you see `fatal: not a git repository`, initialize Git:

```bash
git init
git add .
git commit -m "Initial commit: DysWrite pre-screening engine with quality audit"
git status
```

Expected output:
```
On branch master/main

nothing to commit, working tree clean
```

---

## Step 2: Create a GitHub Repository

### Option A: Personal GitHub Account

1. Log in to [GitHub](https://github.com)
2. Click the **+** icon (top right) → **New repository**
3. Fill in:
   - **Repository name:** `dyswrite-prescreen`
   - **Description:** `Dyslexia handwriting pre-screening engine with MobileNetV3 and Grad-CAM`
   - **Visibility:** Select **Private** (if it's a group project)
   - **Initialize repository:** Leave unchecked (you already have code)
4. Click **Create repository**

### Option B: GitHub Organization (Recommended for Group Projects)

1. Ask your group to create a GitHub Organization (or ask the admin)
2. Goto the organization's page
3. Click **New repository** and follow the same steps as Option A
4. Invite team members to the organization

---

## Step 3: Connect Local Repository to GitHub

After creating the GitHub repo, you'll see setup instructions. Copy these commands and run them:

```bash
git remote add origin https://github.com/YOUR_USERNAME/dyswrite-prescreen.git
git branch -M main
git push -u origin main
```

Replace:
- `YOUR_USERNAME` with your actual GitHub username
- If using an organization, use: `https://github.com/YOUR_ORG/dyswrite-prescreen.git`

**Example:**
```bash
git remote add origin https://github.com/team-dyswrite/dyswrite-prescreen.git
git branch -M main
git push -u origin main
```

---

## Step 4: Verify Upload

Go to your GitHub repository URL in your browser. You should see:
- ✓ All your `.py` files
- ✓ `README.md`, `DEPLOYMENT.md`, `CONTRIBUTING.md`, `QUALITY_AUDIT.md`
- ✓ `requirements.txt`
- ✓ Folders: `src/`, `tests/`, `sample_data/`, `checkpoints/`, `outputs/`, `logs/`

---

## Step 5: Invite Team Members

1. Go to your GitHub repository
2. Click **Settings** (top right) → **Collaborators**
3. Click **Add people**
4. Type each teammate's GitHub username
5. Select **Maintainer** or **Write** access (allow them to push code)
6. Send them the repository URL

---

## For Team Members: Getting Started

Each teammate should follow this once they have access:

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_ORG/dyswrite-prescreen.git
cd dyswrite-prescreen
```

### 2. Create Virtual Environment and Install Dependencies

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Verify Installation

```bash
python -m unittest discover -s tests -v
```

All tests should pass ✓

### 4. Ready to Code!

Read the documentation:
- **Setup:** [DEPLOYMENT.md](DEPLOYMENT.md) - How to run training and inference
- **Coding Standards:** [CONTRIBUTING.md](CONTRIBUTING.md) - Code style and Git workflow
- **Quality Analysis:** [QUALITY_AUDIT.md](QUALITY_AUDIT.md) - Where code implements quality principles
- **Overview:** [README.md](README.md) - Project background and architecture

---

## Common GitHub Commands for the Team

```bash
# Pull latest changes from team
git pull origin main

# Create a feature branch
git checkout -b feature/your-feature-name

# Make changes, then commit
git add .
git commit -m "Descriptive message"

# Push to GitHub
git push origin feature/your-feature-name

# On GitHub: Create Pull Request (PR) for code review
# (After approval and merge, your code goes to main)
```

See [CONTRIBUTING.md](CONTRIBUTING.md#git-workflow) for detailed Git workflow.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `error: Repository not found` | Check your GitHub URL and permissions |
| `fatal: not a git repository` | Run `git init` and retry |
| `Nothing to commit` after `git pull` | You're already up to date |
| `Merge conflict` | See [Git Conflict Resolution](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/about-merge-conflicts) (GitHub docs) |
| Tests fail with `ModuleNotFoundError` | Make sure virtual environment is activated |
| `pip install` fails | See [DEPLOYMENT.md](DEPLOYMENT.md#troubleshooting) for build tool setup |

---

## Repository Structure (After Upload)

Your GitHub repository will show:

```
dyswrite-prescreen/
├── README.md                 ← Project overview
├── DEPLOYMENT.md            ← Setup & run instructions (this helps teammates)
├── CONTRIBUTING.md          ← Code style & Git workflow
├── QUALITY_AUDIT.md         ← Where code implements quality principles
├── requirements.txt         ← Python dependencies
├── .gitignore               ← Files NOT uploaded (venv, .pth, etc.)
├── src/
│   ├── __init__.py
│   ├── config.py            ← All constants (edit here, not in code)
│   ├── exceptions.py        ← Custom exception classes
│   ├── utils.py             ← Shared logging and helpers
│   ├── dataset.py           ← PyTorch Dataset implementation
│   ├── model.py             ← MobileNetV3-Small builder
│   ├── gradcam.py           ← Explainability overlay
│   ├── train.py             ← Training script (python -m src.train)
│   └── infer.py             ← Inference CLI (python -m src.infer ...)
├── tests/
│   ├── __init__.py
│   ├── test_dataset.py      ← Unit tests for dataset handling
│   └── test_model.py        ← Unit tests for model loading
├── sample_data/             ← (Empty initially) Your training images go here
├── checkpoints/             ← Trained model weights (excluded from Git)
├── outputs/                 ← Inference results (excluded from Git)
└── logs/                    ← Training logs (excluded from Git)
```

---

## Next Steps

1. **Upload to GitHub** (follow Steps 1-5 above)
2. **Invite teammates** (Step 5)
3. **Send them this guide** (or the repository README)
4. **Teammates read:** [DEPLOYMENT.md](DEPLOYMENT.md) to set up locally
5. **Teammates read:** [CONTRIBUTING.md](CONTRIBUTING.md) to understand coding standards
6. **Review together:** [QUALITY_AUDIT.md](QUALITY_AUDIT.md) for code quality discussion
7. **Start collaborating** using the Git workflow in [CONTRIBUTING.md#git-workflow](CONTRIBUTING.md#git-workflow)

---

## Quick Links for Your Team

- 📖 **Project Overview:** [README.md](README.md)
- 🚀 **How to Run:** [DEPLOYMENT.md](DEPLOYMENT.md)
- 💻 **Code Contribution Guide:** [CONTRIBUTING.md](CONTRIBUTING.md)
- ✅ **Quality Audit Report:** [QUALITY_AUDIT.md](QUALITY_AUDIT.md)
- 🔗 **Your GitHub Repo:** `https://github.com/YOUR_ORG/dyswrite-prescreen` ← Replace with your actual URL

---

## Questions?

- **GitHub Help:** https://docs.github.com (official GitHub documentation)
- **Git Help:** https://git-scm.com/doc (official Git documentation)
- **Python Help:** https://docs.python.org/3/ (official Python documentation)
- **Project Questions:** Refer to [QUALITY_AUDIT.md](QUALITY_AUDIT.md) or [CONTRIBUTING.md](CONTRIBUTING.md)

---

**You're all set! 🎉 Happy collaborating!**
