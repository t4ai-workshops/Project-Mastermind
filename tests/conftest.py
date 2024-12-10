"""Test configuration for Project MasterMind."""

import pytest

# Register the asyncio plugin
pytest_plugins = ['pytest_asyncio']

def pytest_configure(config):
    """Configure pytest for async testing."""
    config.addini(
        'asyncio_mode',
        'default mode for async fixtures',
        default='auto'
    )