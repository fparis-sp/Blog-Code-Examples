import pytest
from app import create_app


def test_app_creation():
    """Test that Flask app can be created."""
    app = create_app()
    assert app is not None
    assert app.config['TESTING'] is False


def test_app_test_config():
    """Test that app can be created with test config."""
    app = create_app({'TESTING': True})
    assert app.config['TESTING'] is True
