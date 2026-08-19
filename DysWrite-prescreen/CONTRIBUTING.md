# Contributing to DysWrite Pre-Screening

This document outlines guidelines for all team members contributing to the DysWrite pre-screening project.

## Code Quality Standards

Before committing code, ensure it meets these standards (see [QUALITY_AUDIT.md](QUALITY_AUDIT.md) for detailed examples):

### 1. **Module Documentation**
- Every `.py` file must have a header with: Module Name, Project, Created date, Author, Summary, Functions/Classes
- Example:
```python
"""
Module Name : my_module.py
Project     : DysWrite Pre-Screening Engine
Created     : 2026-08-19
Author      : Your Name (DMMMSU-SLUC College of Computer Science)
Summary     : Brief description of what this module does.
Functions   : function1(), function2()
Classes     : MyClass
"""
```

### 2. **Naming Conventions**
- Use `snake_case` for functions and variables: `train_model()`, `best_accuracy`
- Use `PascalCase` for classes: `HandwritingDataset`, `DysWriteError`
- Use `UPPER_CASE` for constants: `BATCH_SIZE`, `CLASS_NAMES`
- Prefix private functions with underscore: `_internal_helper()`

### 3. **Type Hints**
All functions must include type hints:
```python
def process_image(path: str, size: Tuple[int, int]) -> Image.Image:
    """..."""
```

### 4. **Docstrings**
Use Google/NumPy style docstrings with Args, Returns, and Raises sections:
```python
def load_checkpoint(model: nn.Module, path: str, device: torch.device) -> nn.Module:
    """
    Load model weights from checkpoint.

    Args:
        model: the PyTorch model to load weights into.
        path: path to the checkpoint file.
        device: torch device (cpu or cuda).

    Returns:
        The loaded model.

    Raises:
        ModelCheckpointError: if the checkpoint file does not exist or is corrupt.
    """
```

### 5. **No Hardcoded Magic Numbers**
All constants go into `src/config.py`:
```python
# ✓ CORRECT
from src import config
batch_size = config.BATCH_SIZE

# ✗ WRONG
batch_size = 16  # hardcoded!
```

### 6. **Use Logging, Not Print**
```python
# ✓ CORRECT
from src.utils import get_logger
logger = get_logger(__name__)
logger.info("Training epoch %d", epoch)

# ✗ WRONG
print(f"Training epoch {epoch}")
```

### 7. **Error Handling**
Raise custom exceptions instead of generic ones:
```python
# ✓ CORRECT
from src.exceptions import DatasetError
if not folder.exists():
    raise DatasetError(f"Dataset folder not found: {folder}")

# ✗ WRONG
if not folder.exists():
    raise Exception("Dataset folder not found")
```

### 8. **Defensive Programming**
- Validate inputs at the earliest point
- Fail fast with clear error messages
- Handle edge cases (empty datasets, corrupted files, etc.)

## Testing

### Unit Tests
All new functions should have corresponding unit tests:

```bash
# Run all tests
python -m unittest discover -s tests -v

# Run a specific test file
python -m unittest tests.test_model

# Run a specific test
python -m unittest tests.test_model.TestModel.test_build_model_output_shape_matches_num_classes
```

### Test Guidelines
- Tests should NOT require a trained checkpoint or GPU
- Use temporary directories for file I/O tests
- Test both success and error cases
- Example test structure:
```python
class TestMyFeature(unittest.TestCase):
    def setUp(self):
        # Setup code (runs before each test)
        self.tmp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        # Cleanup code (runs after each test)
        shutil.rmtree(self.tmp_dir, ignore_errors=True)
    
    def test_success_case(self):
        # Test that feature works correctly
        result = my_function(valid_input)
        self.assertEqual(result, expected_output)
    
    def test_error_case(self):
        # Test that errors are raised appropriately
        with self.assertRaises(CustomError):
            my_function(invalid_input)
```

## Git Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/descriptive-name
```

Use descriptive names:
- ✓ `feature/add-data-augmentation`
- ✓ `fix/class-mismatch-detection`
- ✗ `feature/fix` (too vague)

### 2. Make Changes and Commit
```bash
git add .
git commit -m "Add descriptive message"
```

**Commit Message Guidelines:**
- Start with a verb: "Add", "Fix", "Improve", "Refactor"
- Reference issue numbers if applicable: "Fix #42: ..."
- Keep messages clear and concise

Examples:
- ✓ `Add data augmentation transforms to improve model robustness`
- ✓ `Fix: ClassMismatchError should trigger on import, not during training`
- ✗ `update stuff` (vague)
- ✗ `asdf` (meaningless)

### 3. Push to GitHub
```bash
git push origin feature/descriptive-name
```

### 4. Create a Pull Request (PR)

On GitHub:
1. Click **Compare & pull request**
2. Write a clear PR title and description
3. Link related issues (if any)
4. Request code review from team members

**PR Description Template:**
```markdown
## Description
What does this PR do? Why?

## Changes
- Bullet 1
- Bullet 2

## Testing
How should reviewers test this?

## Checklist
- [ ] Code follows style guidelines
- [ ] New tests added (if applicable)
- [ ] Documentation updated (if applicable)
- [ ] Tests pass locally
```

### 5. Code Review and Merge
- Address feedback from reviewers
- Resolve conflicts (if any)
- Once approved, merge the PR into `main`

## Common Development Tasks

### Add a New Feature

1. Create a feature branch
2. Write tests first (Test-Driven Development)
3. Implement the feature
4. Verify tests pass
5. Create PR and request review

### Fix a Bug

1. Create a bug-fix branch: `fix/issue-name`
2. Add a test that reproduces the bug
3. Fix the bug
4. Verify the test now passes
5. Create PR with clear description of the issue

### Update Configuration

1. Edit `src/config.py`
2. Update documentation if the change affects users
3. Test with `python -m unittest discover -s tests` to ensure validation passes

## Running Locally

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate          # macOS/Linux
.venv\Scripts\activate             # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m unittest discover -s tests -v

# Run training (requires sample_data/)
python -m src.train

# Run inference (requires trained checkpoint)
python -m src.infer \
    --image sample_data/normal/test.png \
    --checkpoint checkpoints/best_model.pth \
    --output outputs/result.png
```

## Reporting Issues

If you find a bug or have a feature request:

1. Check if it's already been reported (GitHub Issues)
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs. actual behavior
   - Python/PyTorch version info

## Questions?

- **Code quality questions:** See [QUALITY_AUDIT.md](QUALITY_AUDIT.md)
- **Setup/installation issues:** See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Project overview:** See [README.md](README.md)

---

**Happy coding! 🚀**
