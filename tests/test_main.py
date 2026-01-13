"""Unit tests for VariantGeneratorDemoApp main class."""
from unittest.mock import MagicMock, patch
import os
import pytest
from main import VariantGeneratorDemoApp


@pytest.mark.unit
class TestFileOperations:
    """Test suite for file-related operations."""

    @patch("os.path.exists", return_value=True)
    @patch("subprocess.run")
    def test_open_folder_highlights_existing_file(
        self, mock_subprocess: MagicMock, mock_exists: MagicMock, mock_app: VariantGeneratorDemoApp
    ) -> None:
        """Test that Windows Explorer highlights existing file."""
        mock_app.generated_mot_path = "test_file.mot"
        mock_app.open_folder_and_select_file()
        mock_subprocess.assert_called_once_with(
            ["explorer", "/select,", "test_file.mot"]
        )

    @patch("os.path.exists", return_value=False)
    def test_open_folder_shows_error_when_file_missing(
        self, mock_exists: MagicMock, mock_app: VariantGeneratorDemoApp
    ) -> None:
        """Test error message when MOT file doesn't exist."""
        mock_app.generated_mot_path = "test_file.mot"
        mock_app.open_folder_and_select_file()
        mock_app.display_box.delete.assert_called_once_with("0.0", "end")
        mock_app.display_box.insert.assert_called_once_with(
            "0.0", "Error: No valid MOT file found."
        )

    @patch("os.rename")
    @patch("os.path.exists")
    def test_find_and_set_mot_file_success(
        self, mock_exists: MagicMock, mock_rename: MagicMock, mock_app: VariantGeneratorDemoApp
    ) -> None:
        """Test successful MOT file rename."""
        mock_app.project_dir = os.path.dirname(os.path.abspath(__file__))
        mock_app.default_file_name = "demo.mot"
        eep_base_name: str = "demo_appliance"

        mock_exists.side_effect = lambda path: path == os.path.join(
            mock_app.project_dir, "demo.mot"
        )

        result: bool = mock_app.find_and_set_mot_file(eep_base_name)

        assert result is True
        mock_rename.assert_called_once_with(
            os.path.join(mock_app.project_dir, "demo.mot"),
            os.path.join(mock_app.project_dir, "demo_appliance.mot"),
        )

    @patch("os.path.exists", return_value=False)
    def test_find_and_set_mot_file_failure(
        self, mock_exists: MagicMock, mock_app: VariantGeneratorDemoApp
    ) -> None:
        """Test failure when MOT file not found."""
        mock_app.project_dir = "/test"
        mock_app.default_file_name = "default.mot"
        result: bool = mock_app.find_and_set_mot_file("test_file")
        assert result is False


@pytest.mark.unit
class TestInputValidation:
    """Test suite for input validation."""

    def test_validate_and_get_input_valid_number(self, mock_app: VariantGeneratorDemoApp) -> None:
        """Test valid numeric input."""
        mock_app.major_entry = MagicMock()
        mock_app.major_entry.get.return_value = "10"
        result: float | None = mock_app.validate_and_get_input("major")
        assert result == 10.0

    def test_validate_and_get_input_invalid_number(self, mock_app: VariantGeneratorDemoApp) -> None:
        """Test invalid non-numeric input."""
        mock_app.major_entry = MagicMock()
        mock_app.major_entry.get.return_value = "invalid"
        result: float | None = mock_app.validate_and_get_input("major")
        assert result is None
        mock_app.display_box.insert.assert_called_with(
            "0.0", "Error: Major must be a valid number."
        )

    def test_validate_and_get_input_invalid_extension(self, mock_app: VariantGeneratorDemoApp) -> None:
        """Test rejection of file extension strings."""
        mock_app.major_entry = MagicMock()
        mock_app.major_entry.get.return_value = "invalid_file.txt"
        result: float | None = mock_app.validate_and_get_input("major")
        assert result is None


@pytest.mark.unit
@pytest.mark.ui
class TestUIComponents:
    """Test suite for UI functionality."""

    def test_display_error(self, mock_app: VariantGeneratorDemoApp) -> None:
        """Test error message display."""
        mock_app.display_error("Test error message")
        mock_app.display_box.delete.assert_called_once_with("0.0", "end")
        mock_app.display_box.insert.assert_called_once_with(
            "0.0", "Test error message"
        )
