import customtkinter as ctk
import tkinter as tk
import subprocess
import shlex


def run_powershell(cmd: str) -> subprocess.CompletedProcess:
    """
    Run a PowerShell command and return the completed process.

    Args:
        cmd (str): The PowerShell command to execute

    Returns:
        subprocess.CompletedProcess: The completed process object containing stdout, stderr, and return code
    """
    completed: subprocess.CompletedProcess = subprocess.run(
        ["powershell", "-Command", cmd], capture_output=True, shell=True)
    return completed


def run_command(command: str) -> None:
    """
    Execute a shell command.

    Args:
        command (str): The command string to execute
    """
    subprocess.call(shlex.split(command))


def add_line_to_file(file_name: str, new_line: str) -> bool:
    """
    Add a line to the specified file with error handling.

    Args:
        file_name (str): The name of the file to write to
        new_line (str): The line to add to the file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(file_name, 'a') as file:
            file.write(f"{new_line}\n")
        print(
            f"Process successfully ended. Added a new line to the file {file_name}")
        return True
    except IOError as e:
        print(f"Error writing to file {file_name}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error writing to file {file_name}: {e}")
        return False


def validate_and_get_input(entry: ctk.CTkEntry, entry_name: str, min_val: int = 0, max_val: int = 99) -> float | None:
    """
    Validate and return the input from a specific entry field.

    Args:
        entry (ctk.CTkEntry): The entry widget to validate
        entry_name (str): The name of the entry, for error messaging
        min_val (int, optional): Minimum allowed value. Defaults to 0
        max_val (int, optional): Maximum allowed value. Defaults to 99

    Returns:
        float | None: The validated value or None if invalid
    """
    try:
        value: float = float(entry.get())
        if min_val <= value <= max_val:
            return value
        else:
            print(
                f"Error: {entry_name.capitalize()} must be a number between {min_val} and {max_val}.")
    except ValueError:
        print(f"Error: {entry_name.capitalize()} must be a valid number.")
    return None
