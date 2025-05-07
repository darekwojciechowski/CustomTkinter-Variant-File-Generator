from unittest.mock import MagicMock, patch
import os
import pytest
from main import VariantGeneratorDemoApp

# Constants for readability
DISPLAY_START = "0.0"
DISPLAY_END = "end"


@pytest.fixture
def app():
    """Fixture creating an instance of VariantGeneratorDemoApp with a mocked display_box."""
    app = VariantGeneratorDemoApp()
    app.display_box = MagicMock()
    return app


@patch("os.path.exists", return_value=True)
@patch("subprocess.run")
def test_open_folder_highlights_existing_file(mock_subprocess, mock_exists, app):
    """
    Checks if open_folder_and_select_file highlights the file when it exists.

    Mocks:
    - os.path.exists: Returns True, simulating the file exists.
    - subprocess.run: Checks if explorer is called with the correct path.
    """
    app.generated_mot_path = "test_file.mot"
    app.open_folder_and_select_file()
    mock_subprocess.assert_called_once_with(
        ["explorer", "/select,", "test_file.mot"]
    )


@patch("os.path.exists", return_value=False)
def test_open_folder_shows_error_when_file_missing(mock_exists, app):
    """
    Checks if open_folder_and_select_file displays an error when the file does not exist.

    Mocks:
    - os.path.exists: Returns False, simulating the file does not exist.
    """
    app.generated_mot_path = "test_file.mot"
    app.open_folder_and_select_file()
    app.display_box.delete.assert_called_once_with(DISPLAY_START, DISPLAY_END)
    app.display_box.insert.assert_called_once_with(
        DISPLAY_START, "Error: No valid MOT file found."
    )


def test_validate_and_get_input_valid_number(app):
    """
    Checks if validate_and_get_input returns the correct value for a valid number.

    Mocks:
    - app.major_entry.get: Returns a valid number.
    """
    app.major_entry = MagicMock()
    app.major_entry.get.return_value = "10"
    result = app.validate_and_get_input("major")
    assert result == 10.0


def test_validate_and_get_input_invalid_number(app):
    """
    Checks if validate_and_get_input handles invalid (non-numeric) input.

    Mocks:
    - app.major_entry.get: Returns a string that is not a number.
    """
    app.major_entry = MagicMock()
    app.major_entry.get.return_value = "invalid"
    result = app.validate_and_get_input("major")
    assert result is None
    app.display_box.insert.assert_called_with(
        DISPLAY_START, "Error: Major must be a valid number."
    )


def test_validate_and_get_input_invalid_extension(app):
    """
    Checks if validate_and_get_input handles a string that is not a number (e.g., a filename).

    Mocks:
    - app.major_entry.get: Returns a string with an invalid extension.
    """
    app.major_entry = MagicMock()
    app.major_entry.get.return_value = "invalid_file.txt"
    result = app.validate_and_get_input("major")
    assert result is None
    app.display_box.insert.assert_called_with(
        DISPLAY_START, "Error: Major must be a valid number."
    )


@patch("os.rename")
@patch("os.path.exists")
def test_find_and_set_mot_file_success(mock_exists, mock_rename, app):
    """
    Checks if find_and_set_mot_file correctly finds and renames the file.

    Mocks:
    - os.path.exists: Returns True only for the specific path.
    - os.rename: Checks if the rename operation is called.
    """
    app.project_dir = os.path.dirname(os.path.abspath(__file__))
    app.default_file_name = "demo.mot"
    eep_base_name = "demo_appliance"

    mock_exists.side_effect = lambda path: path == os.path.join(
        app.project_dir, "demo.mot"
    )

    result = app.find_and_set_mot_file(eep_base_name)

    assert result is True
    mock_rename.assert_called_once_with(
        os.path.join(app.project_dir, "demo.mot"),
        os.path.join(app.project_dir, "demo_appliance.mot"),
    )


@patch("os.path.exists", return_value=False)
def test_find_and_set_mot_file_failure(mock_exists, app):
    """
    Checks if find_and_set_mot_file returns False when the file does not exist.

    Mocks:
    - os.path.exists: Returns False.
    """
    app.project_dir = "/test"
    app.default_file_name = "default.mot"
    eep_base_name = "test_file"
    result = app.find_and_set_mot_file(eep_base_name)
    assert result is False


def test_display_error(app):
    """
    Checks if display_error correctly displays the error message.

    Mocks:
    - app.display_box: Checks GUI method calls.
    """
    app.display_error("Test error message")
    app.display_box.delete.assert_called_once_with(DISPLAY_START, DISPLAY_END)
    app.display_box.insert.assert_called_once_with(
        DISPLAY_START, "Test error message"
    )
