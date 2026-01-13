"""
Pytest configuration and shared fixtures for the test suite.

This module provides common fixtures, configuration, and utilities used across
all test modules following pytest best practices and 2026 standards.
"""
from unittest.mock import MagicMock, patch
import os
import pytest
from typing import Generator
import customtkinter as ctk
from main import VariantGeneratorDemoApp


# Test constants - centralized for consistency
DISPLAY_START: str = "0.0"
DISPLAY_END: str = "end"
DEFAULT_MOT_FILENAME: str = "VariantGenerator_Output.mot"
TEST_LOG_FILENAME: str = "test_ChangeLog.txt"


@pytest.fixture
def mock_app() -> VariantGeneratorDemoApp:
    """Create minimal VariantGeneratorDemoApp for unit testing."""
    with patch.object(VariantGeneratorDemoApp, '__init__', lambda x: None):
        app: VariantGeneratorDemoApp = VariantGeneratorDemoApp()
        app.display_box = MagicMock()
        app.project_dir = os.getcwd()
        app.default_file_name = "VariantGenerator_Output.mot"
        app.eep_file_name = None
        app.generated_mot_path = None
        return app


@pytest.fixture
def full_app() -> VariantGeneratorDemoApp:
    """
    Create a fully initialized VariantGeneratorDemoApp for integration testing.

    This fixture provides a complete app instance with all UI components mocked,
    suitable for integration and workflow testing.

    Returns:
        VariantGeneratorDemoApp: Fully initialized application instance
    """
    with patch.object(VariantGeneratorDemoApp, '__init__', lambda x: None):
        app: VariantGeneratorDemoApp = VariantGeneratorDemoApp()

        # Set all required attributes
        app.display_box = MagicMock()
        app.location_box = MagicMock()
        app.button_open_file = MagicMock()
        app.variant_option_menu = MagicMock()
        app.major_entry = MagicMock()
        app.minor_entry = MagicMock()
        app.revision_entry = MagicMock()
        app.project_dir = os.getcwd()
        app.default_file_name = DEFAULT_MOT_FILENAME
        app.eep_file_name = None
        app.generated_mot_path = None

        return app


@pytest.fixture
def mock_ctk_entry() -> MagicMock:
    """
    Create a mock CustomTkinter entry widget.

    Returns:
        MagicMock: Mock CTkEntry instance
    """
    return MagicMock(spec=ctk.CTkEntry)


@pytest.fixture
def temp_test_file(tmp_path) -> Generator[str, None, None]:
    """
    Create a temporary test file for file operation tests.

    Args:
        tmp_path: Pytest temporary directory fixture

    Yields:
        str: Path to temporary test file
    """
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Initial content\n")
    yield str(test_file)


@pytest.fixture
def clean_log_file() -> Generator[None, None, None]:
    """
    Ensure clean state for log file testing.

    Removes test log file before and after test execution.

    Yields:
        None
    """
    # Cleanup before test
    if os.path.exists(TEST_LOG_FILENAME):
        os.remove(TEST_LOG_FILENAME)

    yield

    # Cleanup after test
    if os.path.exists(TEST_LOG_FILENAME):
        os.remove(TEST_LOG_FILENAME)


# pytest configuration
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: unit tests")
    config.addinivalue_line("markers", "integration: integration tests")
    config.addinivalue_line("markers", "ui: UI component tests")
