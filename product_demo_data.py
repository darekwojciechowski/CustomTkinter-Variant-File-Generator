# product_demo_data.py
"""
Demo product data for the Variant Generator application.
This file contains sample product information for demonstration purposes.
"""

# Mapping of product names to their corresponding IDs - Demo
id_map: dict[str, int] = {
    "Smart Thermostat": 1001,
    "Home Security Controller": 1002,
    "Smart Lighting Hub": 1003,
    "Energy Management System": 1004,
    "Water Leak Detector": 1005,
    "Air Quality Monitor": 1006,
    "Smart Door Lock": 1007,
    "Window Automation Controller": 1008
}

product_names: list[str] = list(id_map.keys())  # List of product names
