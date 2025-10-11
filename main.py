"""
Thermal Solver
The Nameless [ jowosie | sammychen1153 ]

A Python-based thermal systems solver!

Created as a project for Cal Poly Pomona's ME 4990 course
"""
import tkinter

import customtkinter as ctk
from PIL import Image

class ThermalSolver(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("Thermal Solver")
        self.geometry("1000x650")
        self.resizable(False, False)

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
            frame = F(container, self)  # Pass the container and this controller class
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Start by showing the main menu
        self.show_frame(MenuFrame)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

class MenuFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Define the sharp display size for the icons
        icon_size = (128, 128)

        # Import all UI icons
        piping_img_sharp = Image.open("images/piping.png").resize(icon_size, resample=Image.Resampling.NEAREST)
        self.piping_icon = ctk.CTkImage(light_image=piping_img_sharp, size=icon_size)

        boiling_img_sharp = Image.open("images/boiling.png").resize(icon_size, resample=Image.Resampling.NEAREST)
        self.boiling_icon = ctk.CTkImage(light_image=boiling_img_sharp, size=icon_size)

        dphx_img_sharp = Image.open("images/dphx.png").resize(icon_size, resample=Image.Resampling.NEAREST)
        self.dphx_icon = ctk.CTkImage(light_image=dphx_img_sharp, size=icon_size)

        plate_img_sharp = Image.open("images/plate.png").resize(icon_size, resample=Image.Resampling.NEAREST)
        self.plate_icon = ctk.CTkImage(light_image=plate_img_sharp, size=icon_size)

        shell_img_sharp = Image.open("images/shell.png").resize(icon_size, resample=Image.Resampling.NEAREST)
        self.shell_icon = ctk.CTkImage(light_image=shell_img_sharp, size=icon_size)

        heatpipe_img_sharp = Image.open("images/heatpipe.png").resize(icon_size, resample=Image.Resampling.NEAREST)
        self.heatpipe_icon = ctk.CTkImage(light_image=heatpipe_img_sharp, size=icon_size)

        settings_img_sharp = Image.open("images/settings.png").resize(icon_size, resample=Image.Resampling.NEAREST)
        self.settings_icon = ctk.CTkImage(light_image=settings_img_sharp, size=(48,48))

        # Create main and header frames
        main_frame = ctk.CTkFrame(self, fg_color="#A9CEFF")
        main_frame.pack(padx=0, pady=0, fill="both", expand=True)

        header_frame = ctk.CTkFrame(main_frame, fg_color="#7CB5FF", corner_radius=0)
        header_frame.pack(ipady=5, padx=0, fill="x")

        # Create settings button and title labels in the header frame
        settings_button = self.create_button(header_frame, self.settings_icon, "", lambda: controller.show_frame(SettingsFrame))
        settings_button.pack(side="right", padx=10,anchor="e")

        title_label = ctk.CTkLabel(
            header_frame,
            text="THERMAL SOLVER",
            text_color="black",
            font=ctk.CTkFont(size=32)
        )
        title_label.pack(padx=10, pady=8, anchor="w")

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="What are we solving today?",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        subtitle_label.pack(padx=10, pady=0, anchor="w")

        # Create menu button grid
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20, padx=20, fill="both", expand=True)

        button_frame.grid_rowconfigure((0,1), weight=1)
        button_frame.grid_columnconfigure((0,1,2), weight=1)

        button_data = [
            (self.piping_icon, "Piping", lambda: controller.show_frame(PipingFrame)),
            (self.boiling_icon, "Boiling Condensation", lambda: controller.show_frame(BoilCondFrame)),
            (self.dphx_icon, "Double Pipe HX", lambda: controller.show_frame(DoublePipeFrame)),
            (self.plate_icon, "Plate & Frame HX", lambda: controller.show_frame(PlateFrameFrame)),
            (self.shell_icon, "Shell & Tube HX", lambda: controller.show_frame(ShellTubeFrame)),
            (self.heatpipe_icon, "Heat Pipe", lambda: controller.show_frame(HeatPipeFrame))
        ]

        for i in range(len(button_data)):
            row = i // 3
            col = i % 3
            button = self.create_button(button_frame, button_data[i][0], button_data[i][1], button_data[i][2])
            button.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)

    def create_button(self, parent, image, text, command):
        button = ctk.CTkButton(
            parent,
            image=image,
            text=text,
            text_color="black",
            font=ctk.CTkFont(size=20),
            fg_color="transparent",
            hover_color="#689CE0",
            compound="top",
            command=command,
        )
        return button

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Create main and header frames
        main_frame = ctk.CTkFrame(self, fg_color="#A9CEFF")
        main_frame.pack(padx=0, pady=0, fill="both", expand=True)

        header_frame = ctk.CTkFrame(main_frame, fg_color="#7CB5FF", corner_radius=0)
        header_frame.pack(ipady=5, padx=0, fill="x")

        back_button = ctk.CTkButton(
            header_frame,
            text="← Back to Menu",
            text_color="black",
            font=ctk.CTkFont(size=14),
            fg_color="#689CE0",
            hover_color="#5480BA",
            height=45,
            width=150,
            command=lambda: controller.show_frame(MenuFrame)
        )
        back_button.pack(side="right", anchor="e", padx=10)

        title_label = ctk.CTkLabel(
            header_frame,
            text="THERMAL SOLVER",
            text_color="black",
            font=ctk.CTkFont(size=32)
        )
        title_label.pack(padx=10, pady=8, anchor="w")

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="SETTINGS",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        subtitle_label.pack(padx=10, anchor="w")

        credits_label = ctk.CTkLabel(
            main_frame,
            text="Trailblazed by The Nameless [ jowosie | sammychen1153 ]",
            text_color="black",
            font=ctk.CTkFont(size=14)
        )
        credits_label.pack(side="bottom", pady=(0, 10))

        version_label = ctk.CTkLabel(
            main_frame,
            text="Thermal Solver v0.1.0 beta",
            text_color="black",
            font=ctk.CTkFont(size=14)
        )
        version_label.pack(side="bottom")
        calculator_label = ctk.CTkLabel(
            main_frame,
            text="Calculation Settings",
            text_color="black",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        calculator_label.pack(padx=20, pady=10, anchor="w")

        units_label = ctk.CTkLabel(
            main_frame,
            text="Calculator Units",
            text_color="black",
            font=ctk.CTkFont(size=14)
        )
        units_label.pack(padx=25, pady=0, anchor="w")

        units=tkinter.IntVar(value=1)

        radio_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        radio_frame.pack(padx=20, pady=5, anchor="w")

        si_button = ctk.CTkRadioButton(
            radio_frame,
            corner_radius=0,
            text="SI Units",
            text_color="black",
            font=ctk.CTkFont(size=12),
            variable=units,
            value=1
        )
        si_button.pack(padx=25, side="left")

        imperial_button = ctk.CTkRadioButton(
            radio_frame,
            corner_radius=0,
            text="Imperial Units",
            text_color="black",
            font=ctk.CTkFont(size=12),
            variable=units,
            value=2
        )
        imperial_button.pack(padx=25, side="left")


class PipingFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Add a back button to return to the main menu
        back_button = ctk.CTkButton(self, text="← Back to Menu", command=lambda: controller.show_frame(MenuFrame))
        back_button.pack(pady=10, padx=10, anchor="nw")

        # Title for this page
        title_label = ctk.CTkLabel(self, text="Piping Solver", font=ctk.CTkFont(size=24))
        title_label.pack(pady=10, padx=20)

        # The rest of your content for this page goes here
        content_label = ctk.CTkLabel(self, text="All Piping solver widgets and logic will go here.")
        content_label.pack(pady=20, padx=20, expand=True)

class BoilCondFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        back_button = ctk.CTkButton(self, text="← Back to Menu", command=lambda: controller.show_frame(MenuFrame))
        back_button.pack(pady=10, padx=10, anchor="nw")
        label = ctk.CTkLabel(self, text="Boiling Condensation Page", font=ctk.CTkFont(size=24))
        label.pack(pady=20, padx=20, expand=True)

class DoublePipeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        back_button = ctk.CTkButton(self, text="← Back to Menu", command=lambda: controller.show_frame(MenuFrame))
        back_button.pack(pady=10, padx=10, anchor="nw")
        label = ctk.CTkLabel(self, text="Double Pipe HX Page", font=ctk.CTkFont(size=24))
        label.pack(pady=20, padx=20, expand=True)

class PlateFrameFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        back_button = ctk.CTkButton(self, text="← Back to Menu", command=lambda: controller.show_frame(MenuFrame))
        back_button.pack(pady=10, padx=10, anchor="nw")
        label = ctk.CTkLabel(self, text="Plate and Frame HX Page", font=ctk.CTkFont(size=24))
        label.pack(pady=20, padx=20, expand=True)

class ShellTubeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        back_button = ctk.CTkButton(self, text="← Back to Menu", command=lambda: controller.show_frame(MenuFrame))
        back_button.pack(pady=10, padx=10, anchor="nw")
        label = ctk.CTkLabel(self, text="Shell and Tube HX Page", font=ctk.CTkFont(size=24))
        label.pack(pady=20, padx=20, expand=True)

class HeatPipeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        back_button = ctk.CTkButton(self, text="← Back to Menu", command=lambda: controller.show_frame(MenuFrame))
        back_button.pack(pady=10, padx=10, anchor="nw")
        label = ctk.CTkLabel(self, text="Heat Pipe Page", font=ctk.CTkFont(size=24))
        label.pack(pady=20, padx=20, expand=True)

if __name__ == "__main__":
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("theme.json")
    app = ThermalSolver()
    app.mainloop()