"""Tests"""
from fastapi_sa import __version__


def test_version():
    """Test version"""
    assert __version__ == '0.0.1.dev0'
