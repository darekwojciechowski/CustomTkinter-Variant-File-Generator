import customtkinter as ctk
import tkinter as tk
import subprocess
import shlex


def run_powershell(cmd):
    """
    function to run powershell command
    """
    completed = subprocess.run(
        ["powershell", "-Command", cmd], capture_output=True, shell=True)
    return completed


def run_command(command):
    subprocess.call(shlex.split(command))


def add_line_to_file(file_name, new_line):
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


def validate_and_get_input(entry, entry_name, min_val=0, max_val=99):
    """
    Validate and return the input from a specific entry field.

    :param entry: The entry widget to validate.
    :param entry_name: The name of the entry, for error messaging.
    :param min_val: Minimum allowed value.
    :param max_val: Maximum allowed value.
    :return: The validated value or None if invalid.
    """
    try:
        value = float(entry.get())
        if min_val <= value <= max_val:
            return value
        else:
            print(
                f"Error: {entry_name.capitalize()} must be a number between {min_val} and {max_val}.")
    except ValueError:
        print(f"Error: {entry_name.capitalize()} must be a valid number.")
    return None
