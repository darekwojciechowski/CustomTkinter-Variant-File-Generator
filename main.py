
import os
import subprocess
import traceback
from datetime import date
from tkinter import filedialog

import customtkinter as ctk
from function import add_line_to_file
from product_demo_data import id_map, product_names


class VariantGeneratorDemoApp(ctk.CTk):
    """
    A GUI application for generating variant files demo.

    Attributes:
        project_dir (str): Current working directory of the project.
        default_file_name (str): Default file name for generated .mot files.
    """

    # Application window dimensions
    APP_WIDTH = 550
    APP_HEIGHT = 620

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("green")

    LOG_FILE_NAME = 'ChangeLog.txt'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Variant Generator Demo")
        self.geometry(f"{self.APP_WIDTH}x{self.APP_HEIGHT}")

        self.project_dir = os.getcwd()
        self.default_file_name = "CPM_PU_PT.mot"
        self.eep_file_name = None
        self.generated_mot_path = None

        self.create_widgets()

    def create_widgets(self):
        """Initializes the GUI components of the application."""
        # Location Label and Button
        ctk.CTkLabel(self, text="Location EEP file").grid(
            row=0, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self, text="Open EEP file", command=self.generate_location).grid(
            row=0, column=1, padx=20, pady=20, sticky="ew")

        # Location Box
        self.location_box = ctk.CTkTextbox(self, width=200, height=60)
        self.location_box.grid(row=0, column=2, columnspan=4,
                               padx=20, pady=20, sticky="nsew")

        # Variant Selection
        ctk.CTkLabel(self, text="Variant").grid(
            row=1, column=0, padx=20, pady=20, sticky="ew")
        self.variant_option_menu = ctk.CTkOptionMenu(
            self, values=product_names)
        self.variant_option_menu.grid(
            row=1, column=1, padx=20, pady=20, columnspan=2, sticky="ew")

        # Major, Minor, Revision Input Fields
        for index, (label, placeholder) in enumerate([("Major", "0-99"), ("Minor", "0-99"), ("Revision", "0-99")], start=2):
            self.create_input_field(label, placeholder, index)

        # Generate Results Button
        ctk.CTkButton(self, text="Generate Results", command=self.generate_results).grid(
            row=5, column=1, columnspan=2, padx=20, pady=20, sticky="ew")

        # Result Display Box
        self.display_box = ctk.CTkTextbox(self, width=400, height=60)
        self.display_box.grid(row=6, column=0, columnspan=6,
                              padx=20, pady=20, sticky="nsew")

        # Open File Button (Initially Disabled)
        self.button_open_file = ctk.CTkButton(
            self, state="disabled", text="Open created file", command=self.open_folder_and_select_file, fg_color="gray")
        self.button_open_file.grid(
            row=7, column=1, columnspan=2, padx=20, pady=20, sticky="ew")

    def create_input_field(self, label, placeholder, row):
        """Creates labeled input fields for major, minor, and revision."""
        ctk.CTkLabel(self, text=label).grid(
            row=row, column=0, padx=20, pady=20, sticky="ew")
        entry = ctk.CTkEntry(self, placeholder_text=placeholder)
        entry.grid(row=row, column=1, columnspan=3,
                   padx=20, pady=20, sticky="ew")
        setattr(self, f"{label.lower()}_entry", entry)

    def generate_location(self):
        """Prompts the user to select an EEP file and updates the UI accordingly."""
        try:
            self.display_box.delete("0.0", "end")
            file_path = filedialog.askopenfilename(
                filetypes=[("EEP Files", "*.eep"), ("All Files", "*.*")])
            if not file_path:
                self.display_box.delete("0.0", "end")
                self.display_box.insert("0.0", "No file selected.")
                return
            if file_path.endswith(".eep"):
                self.eep_file_name = file_path
                self.location_box.delete("0.0", "end")
                self.location_box.insert("0.0", os.path.basename(file_path))
                self.display_box.delete("0.0", "end")
                self.display_box.insert("0.0", "File selected successfully.")
            else:
                self.eep_file_name = None
                self.display_error("Error: Please select a valid .eep file.")
        except Exception as e:
            self.display_error(f"Error selecting file: {e}")
            print(f"Exception in generate_location: {traceback.format_exc()}")

    def generate_results(self):
        """Processes the selected EEP file to generate a .MOT file based on user inputs."""
        try:
            self.display_box.delete("0.0", "end")

            if not self.eep_file_name or not self.eep_file_name.endswith(".eep"):
                self.display_error(
                    "Error: Please select a valid .eep file before proceeding.")
                return

            self.display_box.delete("0.0", "end")
            self.display_box.insert("0.0", "Process is running ...")
            self.display_box.update_idletasks()

            major, minor, revision = map(
                self.validate_and_get_input, ("major", "minor", "revision"))
            if None in [major, minor, revision]:
                return

            major, minor, revision = map(int, (major, minor, revision))

            eep_base_name = os.path.splitext(
                os.path.basename(self.eep_file_name))[0]
            product_id = id_map.get(self.variant_option_menu.get(), 0)

            batch_file = os.path.join(self.project_dir, "demo_writeheader.bat")
            if not os.path.exists(batch_file):
                self.display_error(
                    f"Error: Batch file not found at {batch_file}")
                return

            batch_file_name = os.path.basename(batch_file)
            command = f"cmd /c {batch_file_name} --content {eep_base_name} --id {product_id} --major {major} --minor {minor} --revision {revision}"
            print(f"Executing command: {command}")

            if os.name == 'nt':
                try:
                    result = subprocess.run(
                        command, shell=True, check=True, capture_output=True, text=True)
                    self.display_box.delete("0.0", "end")
                    self.display_box.insert(
                        "0.0", "Command executed successfully.")
                except subprocess.CalledProcessError as e:
                    self.display_error(f"Error executing command: {e.stderr}")
                    return

            log_entry = f"Created .mot file | {date.today()} | demo_writeheader --content {eep_base_name} --id {product_id} --major {major} --minor {minor} --revision {revision}"
            add_line_to_file(self.LOG_FILE_NAME, log_entry)

            expected_mot_file = os.path.join(self.project_dir, "demo.mot")
            if os.path.exists(expected_mot_file):
                self.generated_mot_path = expected_mot_file
                self.display_box.delete("0.0", "end")
                self.display_box.insert(
                    "0.0", "Operation completed successfully: .mot file has been created.")
                self.button_open_file.configure(
                    state="normal", fg_color="#1f538d")
            else:
                self.display_error("Error: MOT file was not generated.")
        except Exception as e:
            self.display_error(f"Unexpected error: {e}")
            print(f"Exception in generate_results: {traceback.format_exc()}")

    def validate_and_get_input(self, entry_name):
        """Validates and retrieves the value for the given entry name."""
        try:
            entry_value = getattr(self, f"{entry_name}_entry").get()
            value = float(entry_value)
            if 0 <= value <= 99:
                return value
            else:
                self.display_error(
                    f"Error: {entry_name.capitalize()} must be between 0 and 99.")
                return None
        except (ValueError, AttributeError):
            self.display_error(
                f"Error: {entry_name.capitalize()} must be a valid number.")
            return None

    def find_and_set_mot_file(self, eep_base_name):
        """Tries to locate the generated MOT file and renames it if necessary."""
        try:
            default_file_path = os.path.join(
                self.project_dir, self.default_file_name)
            if os.path.exists(default_file_path):
                new_file_path = os.path.join(
                    self.project_dir, f"{eep_base_name}.mot")
                os.rename(default_file_path, new_file_path)
                self.generated_mot_path = new_file_path
                return True
            return False
        except Exception as e:
            print(f"Error in find_and_set_mot_file: {e}")
            return False

    def open_folder_and_select_file(self):
        """Opens the folder containing the generated .mot file and highlights it."""
        try:
            if not self.generated_mot_path or not os.path.exists(self.generated_mot_path):
                self.display_error("Error: No valid MOT file found.")
                return
            if os.name == 'nt':
                subprocess.run(
                    ["explorer", "/select,", self.generated_mot_path])
        except Exception as e:
            self.display_error(f"Error opening file: {e}")

    def display_error(self, message):
        """Displays error messages in the display box."""
        self.display_box.delete("0.0", "end")
        self.display_box.insert("0.0", message)


if __name__ == "__main__":
    try:
        if not os.path.exists(VariantGeneratorDemoApp.LOG_FILE_NAME):
            with open(VariantGeneratorDemoApp.LOG_FILE_NAME, 'w') as f:
                f.write(
                    "# ChangeLog\n# Format: Created .mot file:: DATE || COMMAND\n")
        app = VariantGeneratorDemoApp()
        app.mainloop()
    except Exception as e:
        print(f"Critical application error: {e}")
        print(traceback.format_exc())
