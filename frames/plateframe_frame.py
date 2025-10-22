import customtkinter as ctk
from frames import BaseFrame
from solvers.plateframe_solver import calculate_plateframe


class PlateFrameFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "PLATE & FRAME HEAT EXCHANGER")

        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        input_frame.pack(pady=10, padx=20, fill="both", expand=True)

        input_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Section Title: Exchanger Settings
        exchanger_label = ctk.CTkLabel(
            input_frame,
            text="EXCHANGER SETTINGS",
            text_color="black",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        exchanger_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Number of Plates
        plates_label = ctk.CTkLabel(input_frame, text="Number of Plates", text_color="black", font=ctk.CTkFont(size=16))
        plates_label.grid(row=1, column=0, sticky="w", padx=5, pady=7)

        self.plates_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="e.g., 10, 20, 50",
            placeholder_text_color="#4F4F4F",
        )
        self.plates_input.grid(row=1, column=1, sticky="ew", padx=5, pady=7)

        # Plate Length
        length_label = ctk.CTkLabel(input_frame, text="Plate Length", text_color="black",
                                        font=ctk.CTkFont(size=16))
        length_label.grid(row=2, column=0, sticky="w", padx=5, pady=7)

        self.length_input = ctk.CTkEntry(
            input_frame,
            placeholder_text_color="#4F4F4F",
        )
        self.length_input.grid(row=2, column=1, sticky="ew", padx=5, pady=7)

        # Plate Width
        width_label = ctk.CTkLabel(input_frame, text="Plate Width", text_color="black",
                                        font=ctk.CTkFont(size=16))
        width_label.grid(row=2, column=2, sticky="w", padx=5, pady=7)

        self.width_input = ctk.CTkEntry(
            input_frame,
            placeholder_text_color="#4F4F4F",
        )
        self.width_input.grid(row=2, column=3, sticky="ew", padx=5, pady=7)

        # Section Title: Fluid Settings
        fluid_label = ctk.CTkLabel(
            input_frame,
            text="FLUID SETTINGS",
            text_color="black",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        fluid_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=(15, 10))

        # Hot Fluid
        hot_fluid_label = ctk.CTkLabel(
            input_frame,
            text="HOT FLUID",
            text_color="black",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        hot_fluid_label.grid(row=5, column=0, sticky="w", padx=5, pady=7)

        self.hot_fluid_input = ctk.CTkOptionMenu(
            input_frame,
            values=["Water", "Hexane", "Ethylene Glycol", "Benzene", "Oil"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black",
            width=250
        )
        self.hot_fluid_input.grid(row=5, column=1, sticky="w", padx=10, pady=7)

        # Hot Fluid Inlet Temp
        hot_fluid_inlet_label = ctk.CTkLabel(
            input_frame,
            text="Inlet Temp",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        hot_fluid_inlet_label.grid(row=6, column=0, sticky="w", padx=10, pady=7)

        self.hot_fluid_inlet_input = ctk.CTkEntry(
            input_frame,
            placeholder_text_color="#4F4F4F",
        )
        self.hot_fluid_inlet_input.grid(row=6, column=1, sticky="ew", padx=10, pady=7)

        # Hot Fluid Mass Flow Rate
        hot_fluid_mfr_label = ctk.CTkLabel(
            input_frame,
            text="Mass Flow Rate",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        hot_fluid_mfr_label.grid(row=8, column=0, sticky="w", padx=10, pady=7)

        self.hot_fluid_mfr_input = ctk.CTkEntry(
            input_frame,
            placeholder_text_color="#4F4F4F",
        )
        self.hot_fluid_mfr_input.grid(row=8, column=1, sticky="ew", padx=10, pady=7)

        # Cold Fluid
        cold_fluid_label = ctk.CTkLabel(
            input_frame,
            text="COLD FLUID",
            text_color="black",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        cold_fluid_label.grid(row=5, column=2, sticky="w", padx=5, pady=7)

        self.cold_fluid_input = ctk.CTkOptionMenu(
            input_frame,
            values=["Water", "Hexane", "Ethylene Glycol", "Benzene", "Oil"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black",
            width=250
        )
        self.cold_fluid_input.grid(row=5, column=3, sticky="w", padx=10, pady=7)

        # Cold Fluid Inlet Temp
        cold_fluid_inlet_label = ctk.CTkLabel(
            input_frame,
            text="Inlet Temp",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        cold_fluid_inlet_label.grid(row=6, column=2, sticky="w", padx=10, pady=7)

        self.cold_fluid_inlet_input = ctk.CTkEntry(
            input_frame,
            placeholder_text_color="#4F4F4F",
        )
        self.cold_fluid_inlet_input.grid(row=6, column=3, sticky="ew", padx=10, pady=7)

        # Cold Fluid Mass Flow Rate
        cold_fluid_mfr_label = ctk.CTkLabel(
            input_frame,
            text="Mass Flow Rate",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        cold_fluid_mfr_label.grid(row=8, column=2, sticky="w", padx=10, pady=7)

        self.cold_fluid_mfr_input = ctk.CTkEntry(
            input_frame,
            placeholder_text_color="#4F4F4F",
        )
        self.cold_fluid_mfr_input.grid(row=8, column=3, sticky="ew", padx=10, pady=7)

        # Calculate button
        calculate_button = ctk.CTkButton(
            input_frame,
            text="Calculate!",
            text_color="black",
            font=ctk.CTkFont(size=16),
            fg_color="#689CE0",
            hover_color="#5480BA",
            height=45,
            width=150,
            command=self.calculate
        )
        calculate_button.grid(row=9, column=0, columnspan=4, pady=50)

        # Results Label
        self.results_label = ctk.CTkLabel(
            input_frame,
            text="",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        self.results_label.grid(row=10, column=0, columnspan=4)
        self.update_placeholders()

    def update_placeholders(self):
        if self.controller.unit_system == "SI":
            self.length_input.configure(placeholder_text="m")
            self.width_input.configure(placeholder_text="m")
            self.hot_fluid_inlet_input.configure(placeholder_text="°C")
            self.hot_fluid_mfr_input.configure(placeholder_text="kg/s")
            self.cold_fluid_inlet_input.configure(placeholder_text="°C")
            self.cold_fluid_mfr_input.configure(placeholder_text="kg/s")
        else: # Imperial
            self.length_input.configure(placeholder_text="ft")
            self.width_input.configure(placeholder_text="ft")
            self.hot_fluid_inlet_input.configure(placeholder_text="°F")
            self.hot_fluid_mfr_input.configure(placeholder_text="lb/s")
            self.cold_fluid_inlet_input.configure(placeholder_text="°F")
            self.cold_fluid_mfr_input.configure(placeholder_text="lb/s")

    def calculate(self):
        try:
            # Take all input parameters from gui elements
            plates = self.plates_input.get()
            length = self.length_input.get()
            width = self.width_input.get()
            hot_fluid = self.hot_fluid_input.get()
            hot_fluid_inlet_temp = self.hot_fluid_inlet_input.get()
            hot_fluid_mass_flow = self.hot_fluid_mfr_input.get()
            cold_fluid = self.cold_fluid_input.get()
            cold_fluid_inlet_temp = self.cold_fluid_inlet_input.get()
            cold_fluid_mass_flow = self.cold_fluid_mfr_input.get()

            # Pass inputs to calculator to get results
            calculation_results = calculate_plateframe(
                plates=plates, length=length, width=width, hot_fluid=hot_fluid,
                hot_fluid_inlet_temp=hot_fluid_inlet_temp, hot_fluid_mass_flow=hot_fluid_mass_flow,
                cold_fluid=cold_fluid, cold_fluid_inlet_temp=cold_fluid_inlet_temp,
                cold_fluid_mass_flow=cold_fluid_mass_flow
            )

            self.controller.display_results_window("Calculation Results", calculation_results)

        except ValueError:
            self.results_label.configure(text="Please enter valid inputs in all fields")

        except Exception as e:
            self.results_label.configure(text=f"An error occurred: {e}")