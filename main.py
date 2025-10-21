"""
Thermal Solver
The Nameless [ jowosie | sammychen1153 ]

A Python-based thermal systems solver!

Created as a project for Cal Poly Pomona's ME 4990 course
"""

# Import custom font (library not macOS compatible)
import sys
if sys.platform != "darwin":
    from tkextrafont import Font

from pathlib import Path
import customtkinter as ctk
from PIL import Image

# Import all frames
from frames.menu_frame import MenuFrame
from frames.settings_frame import SettingsFrame
from frames.piping_frame import PipingFrame
from frames.boilcond_frame import BoilCondFrame
from frames.doublepipe_frame import DoublePipeFrame
from frames.shelltube_frame import ShellTubeFrame
from frames.plateframe_frame import PlateFrameFrame
from frames.heatpipe_frame import HeatPipeFrame

class ThermalSolver(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Application version
        self.version = "0.1.8-alpha"

        # Asset management
        self.BASE_PATH = Path(__file__).parent
        self.FONT_PATH = self.BASE_PATH / "assets" / "fonts" / "PixelifySans.ttf"
        self.IMAGE_PATH = self.BASE_PATH / "assets" / "images"

        # Load custom font (NOT MACOS COMPATIBLE)
        if sys.platform != "darwin":
            Font(file=self.FONT_PATH, family="Pixelify Sans", size=12)

        # Load all images into dictionary
        self.images = {
            "piping": self.load_image("piping.png", (128,128)),
            "boiling": self.load_image("boiling.png", (128,128)),
            "dphx": self.load_image("dphx.png", (128,128)),
            "plate": self.load_image("plate.png", (128,128)),
            "shell": self.load_image("shell.png", (128,128)),
            "heatpipe": self.load_image("heatpipe.png", (128,128)),
            "settings": self.load_image("settings.png", (48,48))
        }

        # Window Configuration
        self.title("Thermal Solver")
        self.geometry("1000x650")
        self.resizable(False, False)

        # Set default unit system
        self.unit_system = "SI"

        # Container frame to hold pages
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to hold frames
        self.frames = {}

        # Create each page and add it to the dictionary
        for F in (MenuFrame, PipingFrame, BoilCondFrame, DoublePipeFrame, PlateFrameFrame, ShellTubeFrame,
                  HeatPipeFrame, SettingsFrame):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Start by showing the main menu
        self.show_frame("MenuFrame")

    # Function to load and process images
    def load_image(self, name, size):
        image_path = self.IMAGE_PATH / name
        image = Image.open(image_path).resize(size, resample=Image.Resampling.NEAREST)
        return ctk.CTkImage(light_image=image, size=size)

    # Function to bring a frame to the front
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    # Function to update the unit system
    def set_units(self, unit_system):
        self.unit_system = unit_system
        for frame in self.frames.values():
            if hasattr(frame, "update_placeholders"):
                frame.update_placeholders()

    # Function to display new results window
    def display_results_window(self, title, results_text):

        # Create a new window associated with the main app
        results_win = ctk.CTkToplevel(self)
        results_win.title(title)
        results_win.geometry("400x300")
        results_win.resizable(False, False)

        # Keep results window on top initially
        results_win.attributes("-topmost", True)

        # Display results in textbox
        results_textbox = ctk.CTkTextbox(results_win, wrap="word", font=ctk.CTkFont(size=14))
        results_textbox.pack(expand=True, fill="both", padx=10, pady=10)

        # Insert the results
        results_textbox.insert("1.0", results_text)

        # Make it read-only
        results_textbox.configure(state="disabled")

        close_button = ctk.CTkButton(results_win, text="Close", command=results_win.destroy)
        close_button.pack(pady=10)

        results_win.grab_set()

if __name__ == "__main__":
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("theme.json")
    app = ThermalSolver()
    app.mainloop()