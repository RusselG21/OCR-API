import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
    print(f"Added {project_root} to Python path")

try:
    import pytest
    print(f"Pytest version: {pytest.__version__}")
except ImportError:
    print("WARNING: pytest is not available in the current Python environment")
    print(f"Current Python path: {sys.path}")
    print(f"Current Python executable: {sys.executable}")


@pytest.fixture(scope="class")
def mock_files():
    """Fixture to provide mock file data"""
    return {"file": ("document.pdf", b"test content", "application/pdf")}


@pytest.fixture(scope="class")
def mock_headers():
    """Fixture to provide mock request headers"""
    return {"Authorization": "Bearer test_token"}
