# DysWrite Project Repository

This repository contains the DysWrite dyslexia handwriting pre-screening system.

## Folder Structure

```
DysWrite/
├── DysWrite-prescreen/          ← Main pre-screening engine code & documentation
│   ├── README.md                ← Project overview
│   ├── src/                     ← Source code (MobileNetV3, Grad-CAM, training, inference)
│   ├── tests/                   ← Unit tests
│   ├── requirements.txt         ← Python dependencies
│   ├── DEPLOYMENT.md            ← Setup instructions for all platforms
│   ├── CONTRIBUTING.md          ← Code standards and Git workflow
│   ├── QUALITY_AUDIT.md         ← Code quality analysis
│   └── [other directories]      ← checkpoints, outputs, logs, sample_data
│
└── graphs-and-charts/           ← System design documentation
    ├── 01_DFD/                  ← Data Flow Diagrams
    ├── 02_Structured_Chart/     ← Structure Charts
    ├── 03_HIPO_Diagram/         ← HIPO Diagrams
    ├── 04_Structured_English/   ← Structured English specifications
    ├── 05_Pseudo_Code/          ← Pseudo code documentation
    ├── 06_ERD/                  ← Entity Relationship Diagrams
    └── 07_Data_Dictionary/      ← Data Dictionary
```

## Quick Start

To set up and run the pre-screening engine:

```bash
cd DysWrite-prescreen
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python -m unittest discover -s tests  # Verify installation
```

See [DysWrite-prescreen/DEPLOYMENT.md](DysWrite-prescreen/DEPLOYMENT.md) for complete setup instructions.

## Documentation

- **[DysWrite-prescreen/README.md](DysWrite-prescreen/README.md)**  Project overview
- **[DysWrite-prescreen/QUALITY_AUDIT.md](DysWrite-prescreen/QUALITY_AUDIT.md)**  Code quality analysis (where code implements professional standards, defensive programming, error handling)
- **[DysWrite-prescreen/DEPLOYMENT.md](DysWrite-prescreen/DEPLOYMENT.md)**  How to set up and run
- **[DysWrite-prescreen/CONTRIBUTING.md](DysWrite-prescreen/CONTRIBUTING.md)**  Code style guide and Git workflow
- **[graphs-and-charts/](graphs-and-charts/)**  System design documentation (DFD, ERD, HIPO, etc.)

## Project Overview

The DysWrite Pre-Screening Engine is a machine learning system that:
- Fine-tunes a MobileNetV3-Small model for dyslexia handwriting classification
- Generates Grad-CAM explainability overlays for predictions
- Implements professional coding standards and defensive programming
- Includes comprehensive unit tests

## Code Quality

This project demonstrates:
- Professional Coding Standards (PEP 8/257/484, type hints, docstrings)
- 15 Principles of Quality Software
- Defensive Programming (early validation, fail-fast)
- Error Exception Handling (custom exceptions, comprehensive testing)

See [QUALITY_AUDIT.md](DysWrite-prescreen/QUALITY_AUDIT.md) for detailed analysis.

##  Getting Help

- **Setup issues:** See [DysWrite-prescreen/DEPLOYMENT.md](DysWrite-prescreen/DEPLOYMENT.md#troubleshooting)
- **Code contribution:** See [DysWrite-prescreen/CONTRIBUTING.md](DysWrite-prescreen/CONTRIBUTING.md)
- **Understanding the code quality:** See [DysWrite-prescreen/QUALITY_AUDIT.md](DysWrite-prescreen/QUALITY_AUDIT.md)

---
*Rachel A. Regacho,*
*Regine J. Velasquez,*
*Angeline G. Garcia,*
*John Albert C. Lachica,*
*Gerrald A. Bicera*
*DysWrite Pre-Screening Engine | DMMMSU-SLUC College of Computer Science | 2026*
