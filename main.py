import os
import subprocess
import sys
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
    APP_WIDTH: int = 550
    APP_HEIGHT: int = 620

    ctk.set_appearance_mode("Dark")

    # Custom violet/purple color theme
    # Using blue as base, will override with custom colors
    ctk.set_default_color_theme("blue")

    LOG_FILE_NAME: str = 'ChangeLog.txt'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Variant Generator Demo")
        self.geometry(f"{self.APP_WIDTH}x{self.APP_HEIGHT}")

        # Set custom violet theme colors
        self._set_violet_theme()

        # Get the directory where the script/executable is located
        # For PyInstaller, use sys._MEIPASS; otherwise use script directory
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            self.project_dir: str = os.path.dirname(sys.executable)
        else:
            # Running as script
            self.project_dir: str = os.path.dirname(os.path.abspath(__file__))
        self.default_file_name: str = "VariantGenerator_Output.mot"
        self.eep_file_name: str | None = None
        self.generated_mot_path: str | None = None

        self.location_box: ctk.CTkTextbox | None = None
        self.variant_option_menu: ctk.CTkOptionMenu | None = None
        self.major_entry: ctk.CTkEntry | None = None
        self.minor_entry: ctk.CTkEntry | None = None
        self.revision_entry: ctk.CTkEntry | None = None
        self.display_box: ctk.CTkTextbox | None = None
        self.button_open_file: ctk.CTkButton | None = None

        self.create_widgets()

    def _set_violet_theme(self) -> None:
        """Apply modern violet/purple color theme to the application."""
        # Modern AI-inspired violet color palette
        ctk.set_appearance_mode("Dark")

    def create_widgets(self) -> None:
        """Initializes the GUI components of the application."""
        # Location Label and Button
        ctk.CTkLabel(self, text="Location EEP file").grid(
            row=0, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self, text="Open EEP file", command=self.generate_location,
                      fg_color="#8B7FD8", hover_color="#7C6FCC").grid(
            row=0, column=1, padx=20, pady=20, sticky="ew")

        # Location Box
        self.location_box = ctk.CTkTextbox(self, width=200, height=60)
        self.location_box.grid(row=0, column=2, columnspan=4,
                               padx=20, pady=20, sticky="nsew")

        # Variant Selection
        ctk.CTkLabel(self, text="Variant").grid(
            row=1, column=0, padx=20, pady=20, sticky="ew")
        self.variant_option_menu = ctk.CTkOptionMenu(
            self, values=product_names, fg_color="#8B7FD8",
            button_color="#7C6FCC", button_hover_color="#6D5FBF")
        self.variant_option_menu.grid(
            row=1, column=1, padx=20, pady=20, columnspan=2, sticky="ew")

        # Major, Minor, Revision Input Fields
        for index, (label, placeholder) in enumerate([("Major", "0-99"), ("Minor", "0-99"), ("Revision", "0-99")], start=2):
            self.create_input_field(label, placeholder, index)

        # Generate Results Button
        ctk.CTkButton(self, text="Generate Results", command=self.generate_results,
                      fg_color="#9388DB", hover_color="#8B7FD8").grid(
            row=5, column=1, columnspan=2, padx=20, pady=20, sticky="ew")

        # Result Display Box
        self.display_box = ctk.CTkTextbox(self, width=400, height=60)
        self.display_box.grid(row=6, column=0, columnspan=6,
                              padx=20, pady=20, sticky="nsew")

        # Open File Button (Initially Disabled)
        self.button_open_file = ctk.CTkButton(
            self, state="disabled", text="Open created file",
            command=self.open_folder_and_select_file, fg_color="gray")
        self.button_open_file.grid(
            row=7, column=1, columnspan=2, padx=20, pady=20, sticky="ew")

    def create_input_field(self, label: str, placeholder: str, row: int) -> None:
        """Creates labeled input fields for major, minor, and revision."""
        ctk.CTkLabel(self, text=label).grid(
            row=row, column=0, padx=20, pady=20, sticky="ew")
        entry = ctk.CTkEntry(self, placeholder_text=placeholder)
        entry.grid(row=row, column=1, columnspan=3,
                   padx=20, pady=20, sticky="ew")
        setattr(self, f"{label.lower()}_entry", entry)

    def generate_location(self) -> None:
        """Prompts the user to select an EEP file and updates the UI accordingly."""
        try:
            self.display_box.delete("0.0", "end")
            file_path: str = filedialog.askopenfilename(
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

    def generate_results(self) -> None:
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

            major_int: int = int(major)
            minor_int: int = int(minor)
            revision_int: int = int(revision)

            eep_base_name: str = os.path.splitext(
                os.path.basename(self.eep_file_name))[0]
            product_id: int = id_map.get(self.variant_option_menu.get(), 0)

            # Look for batch file in multiple locations
            # First, check in the same directory as exe/script
            batch_file: str = os.path.join(
                self.project_dir, "demo_writeheader.bat")

            # If not found, check in demo subfolder (for development)
            if not os.path.exists(batch_file):
                batch_file = os.path.join(
                    self.project_dir, "demo", "demo_writeheader.bat")

            if not os.path.exists(batch_file):
                self.display_error(
                    f"Error: Batch file not found. Searched in:\n- {self.project_dir}\n- {os.path.join(self.project_dir, 'demo')}")
                return

            batch_file_name: str = os.path.basename(batch_file)
            command: str = f'cmd /c "{batch_file}" --content {eep_base_name} --id {product_id} --major {major_int} --minor {minor_int} --revision {revision_int}'
            print(f"Executing command: {command}")

            if os.name == 'nt':
                try:
                    result: subprocess.CompletedProcess = subprocess.run(
                        command, shell=True, check=True, capture_output=True, text=True)
                    self.display_box.delete("0.0", "end")
                    self.display_box.insert(
                        "0.0", "Command executed successfully.")
                except subprocess.CalledProcessError as e:
                    self.display_error(f"Error executing command: {e.stderr}")
                    return

            log_entry: str = f"Created .mot file | {date.today()} | demo_writeheader --content {eep_base_name} --id {product_id} --major {major_int} --minor {minor_int} --revision {revision_int}"
            add_line_to_file(self.LOG_FILE_NAME, log_entry)

            expected_mot_file: str = os.path.join(self.project_dir, "demo.mot")
            if os.path.exists(expected_mot_file):
                self.generated_mot_path = expected_mot_file
                self.display_box.delete("0.0", "end")
                self.display_box.insert(
                    "0.0", "✓ Operation completed successfully: .mot file has been created.\n\nClick the button below to open the file.")
                self.button_open_file.configure(
                    state="normal", fg_color="#10b981", hover_color="#059669",
                    text="✓ Open Created File", font=("", 13, "bold"))
            else:
                self.display_error("Error: MOT file was not generated.")
        except Exception as e:
            self.display_error(f"Unexpected error: {e}")
            print(f"Exception in generate_results: {traceback.format_exc()}")

    def validate_and_get_input(self, entry_name: str) -> float | None:
        """Validates and retrieves the value for the given entry name."""
        try:
            entry_value: str = getattr(self, f"{entry_name}_entry").get()
            value: float = float(entry_value)
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

    def find_and_set_mot_file(self, eep_base_name: str) -> bool:
        """Tries to locate the generated MOT file and renames it if necessary."""
        try:
            default_file_path: str = os.path.join(
                self.project_dir, self.default_file_name)
            if os.path.exists(default_file_path):
                new_file_path: str = os.path.join(
                    self.project_dir, f"{eep_base_name}.mot")
                os.rename(default_file_path, new_file_path)
                self.generated_mot_path = new_file_path
                return True
            return False
        except Exception as e:
            print(f"Error in find_and_set_mot_file: {e}")
            return False

    def open_folder_and_select_file(self) -> None:
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

    def display_error(self, message: str) -> None:
        """Displays error messages in the display box."""
        self.display_box.delete("0.0", "end")
        self.display_box.insert("0.0", message)


if __name__ == "__main__":
    try:
        if not os.path.exists(VariantGeneratorDemoApp.LOG_FILE_NAME):
            with open(VariantGeneratorDemoApp.LOG_FILE_NAME, 'w') as f:
                f.write(
                    "# ChangeLog\n# Format: Created .mot file:: DATE || COMMAND\n")
        app: VariantGeneratorDemoApp = VariantGeneratorDemoApp()
        app.mainloop()
    except Exception as e:
        print(f"Critical application error: {e}")
        print(traceback.format_exc())
