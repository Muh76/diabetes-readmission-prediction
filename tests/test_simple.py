"""
Super simple test to isolate CI issues
"""
import pytest


def test_basic():
    """Basic test that should always pass"""
    assert True
    print("✅ Basic test passed")


def test_math():
    """Simple math test"""
    assert 1 + 1 == 2
    print("✅ Math test passed")


def test_import():
    """Test if we can import basic modules"""
    try:
        import os
        import sys

        # Use the imports to avoid ruff warnings
        assert sys.version_info >= (3, 8)
        assert os.path.exists(".")
        print("✅ Basic imports work")
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


if __name__ == "__main__":
    print("Running simple tests...")
    test_basic()
    test_math()
    test_import()
    print("✅ All simple tests passed!")
