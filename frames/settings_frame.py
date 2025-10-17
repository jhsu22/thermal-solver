import customtkinter as ctk
import tkinter
from frames import BaseFrame

class SettingsFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "SETTINGS")

        credits_label = ctk.CTkLabel(
            self.content_frame,
            text="Trailblazed by The Nameless [ jowosie | sammychen1153 ]",
            text_color="black",
            font=ctk.CTkFont(size=14)
        )
        credits_label.pack(side="bottom", pady=(0, 10))

        version_label = ctk.CTkLabel(
            self.content_frame,
            text=f"Thermal Solver v{self.controller.version}",
            text_color="black",
            font=ctk.CTkFont(size=14)
        )
        version_label.pack(side="bottom")
        calculator_label = ctk.CTkLabel(
            self.content_frame,
            text="CALCULATION SETTINGS",
            text_color="black",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        calculator_label.pack(padx=20, pady=5, anchor="w")

        units_label = ctk.CTkLabel(
            self.content_frame,
            text="Calculator Units",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        units_label.pack(padx=25, pady=0, anchor="w")

        self.units_var = tkinter.StringVar(value=self.controller.unit_system)

        radio_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        radio_frame.pack(padx=20, pady=5, anchor="w")

        si_button = ctk.CTkRadioButton(
            radio_frame,
            corner_radius=0,
            text="SI Units",
            text_color="black",
            font=ctk.CTkFont(size=14),
            variable=self.units_var,
            value="SI",
            command=lambda: self.controller.set_units("SI")
        )
        si_button.pack(padx=25, side="left")

        imperial_button = ctk.CTkRadioButton(
            radio_frame,
            corner_radius=0,
            text="Imperial Units",
            text_color="black",
            font=ctk.CTkFont(size=14),
            variable=self.units_var,
            value="Imperial",
            command=lambda: self.controller.set_units("Imperial")
        )
        imperial_button.pack(padx=25, side="left")