"""Unit tests for utility functions."""
from unittest.mock import MagicMock, patch, mock_open
import pytest
import subprocess
from function import run_powershell, run_command, add_line_to_file, validate_and_get_input
import customtkinter as ctk


@pytest.mark.unit
class TestRunPowershell:
    """Test suite for run_powershell function."""

    @patch("subprocess.run")
    def test_run_powershell_success(self, mock_run: MagicMock) -> None:
        """Test successful PowerShell command execution."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=["powershell", "-Command", "echo 'test'"],
            returncode=0, stdout="test", stderr=""
        )
        result = run_powershell("echo 'test'")
        assert result.returncode == 0

    @patch("subprocess.run")
    def test_run_powershell_with_error(self, mock_run: MagicMock) -> None:
        """Test PowerShell command error handling."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=["powershell", "-Command", "invalid_command"],
            returncode=1, stdout="", stderr="Command not found"
        )
        result = run_powershell("invalid_command")
        assert result.returncode == 1


@pytest.mark.unit
class TestRunCommand:
    """Test suite for run_command function."""

    @patch("subprocess.call")
    def test_run_command_simple(self, mock_call: MagicMock) -> None:
        """Test simple command execution."""
        run_command("ls -la")
        mock_call.assert_called_once()


@pytest.mark.unit
class TestAddLineToFile:
    """Test suite for add_line_to_file function."""

    @patch("builtins.open", new_callable=mock_open)
    def test_add_line_to_file_success(self, mock_file: MagicMock) -> None:
        """Test successful file write."""
        result = add_line_to_file("test.txt", "New line")
        assert result is True
        mock_file().write.assert_called_once_with("New line\n")

    @patch("builtins.open", side_effect=IOError("Permission denied"))
    def test_add_line_to_file_io_error(self, mock_file: MagicMock) -> None:
        """Test IO error handling."""
        result = add_line_to_file("test.txt", "New line")
        assert result is False


@pytest.mark.unit
class TestValidateAndGetInput:
    """Test suite for validate_and_get_input function."""

    def test_validate_valid_integer(self) -> None:
        """Test valid integer input."""
        mock_entry = MagicMock(spec=ctk.CTkEntry)
        mock_entry.get.return_value = "42"
        result = validate_and_get_input(mock_entry, "test", 0, 99)
        assert result == 42.0

    def test_validate_below_minimum(self) -> None:
        """Test value below minimum."""
        mock_entry = MagicMock(spec=ctk.CTkEntry)
        mock_entry.get.return_value = "-5"
        result = validate_and_get_input(mock_entry, "test", 0, 99)
        assert result is None

    def test_validate_non_numeric(self) -> None:
        """Test non-numeric input."""
        mock_entry = MagicMock(spec=ctk.CTkEntry)
        mock_entry.get.return_value = "invalid"
        result = validate_and_get_input(mock_entry, "test", 0, 99)
        assert result is None
