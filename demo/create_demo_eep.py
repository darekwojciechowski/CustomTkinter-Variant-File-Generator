"""
Demo EEP File Generator
=======================

This script creates a demonstration .eep file for testing the Variant Generator application.
The .eep file contains random binary data to simulate a real device configuration file.

Purpose:
- Generate sample .eep files for demonstration and testing
- Provide realistic test data without using proprietary information
- Allow users to try the Variant Generator application without real device files

Usage:
    python create_demo_eep.py

Output:
    Creates a file named 'demo_appliance.eep' in the current directory
    containing 4KB of random binary data.

This tool is part of the Variant Generator demonstration package and is intended
for educational and testing purposes only.
"""

import os
import random


def create_demo_eep_file(filename: str = "demo_appliance.eep", size: int = 4096) -> str:
    """
    Creates a single demo .eep file with random binary data

    Args:
        filename: Name of the .eep file to create (default: demo_appliance.eep)
        size: Size of the file in bytes (default: 4KB)

    Returns:
        str: Absolute path to the created file
    """
    # Generate random binary data
    data: bytes = bytes([random.randint(0, 255) for _ in range(size)])

    # Write to file
    with open(filename, 'wb') as f:
        f.write(data)

    file_path: str = os.path.abspath(filename)
    print(f"Created demo .eep file: {file_path}")
    print(f"File size: {size} bytes")
    print(f"This file can be used with the Variant Generator application for testing purposes.")
    return file_path


if __name__ == "__main__":
    # Create just one demo file with the requested name
    create_demo_eep_file("demo_appliance.eep", 4096)
    print("\nNote: This is a simulated file containing random data.")
    print("In a real-world scenario, .eep files contain device configuration data.")
