import customtkinter as ctk
from frames import BaseFrame
from solvers.boilcond_solver import calculate_boilcond


class BoilCondFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "BOILING CONDENSATION")

        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        input_frame.pack(pady=10, padx=20, fill="both", expand=True)

        input_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Section Title: Boiling/Condensation Settings
        boilcond_label = ctk.CTkLabel(
            input_frame,
            text="BOILING/CONDENSATION SETTINGS",
            text_color="black",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        boilcond_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Type
        type_label = ctk.CTkLabel(input_frame, text="Type", text_color="black", font=ctk.CTkFont(size=16))
        type_label.grid(row=1, column=0, sticky="w", padx=5, pady=7)

        self.type_selection = ctk.CTkOptionMenu(
            input_frame,
            values=["Boiling", "Condensation"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black",
            width=250
        )
        self.type_selection.grid(row=1, column=1, sticky="w", padx=5, pady=7)

        # Fluid
        fluid_label = ctk.CTkLabel(input_frame, text="Fluid", text_color="black", font=ctk.CTkFont(size=16))
        fluid_label.grid(row=2, column=0, sticky="w", padx=5, pady=7)

        self.fluid_input = ctk.CTkOptionMenu(
            input_frame,
            values=["Water", "Hexane", "Ethylene Glycol", "Benzene", "Oil"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black",
            width=250
        )
        self.fluid_input.grid(row=2, column=1, sticky="w", padx=10, pady=7)

        # Saturation Temperature
        sat_temp_label = ctk.CTkLabel(input_frame, text="Saturation Temperature", text_color="black",
                                      font=ctk.CTkFont(size=16))
        sat_temp_label.grid(row=3, column=0, sticky="w", padx=10, pady=7)

        self.sat_temp_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="deg C",
            placeholder_text_color="#4F4F4F",
        )
        self.sat_temp_input.grid(row=3, column=1, sticky="ew", padx=10, pady=7)

        # Heat Flux
        heat_flux_label = ctk.CTkLabel(input_frame, text="Heat Flux", text_color="black", font=ctk.CTkFont(size=16))
        heat_flux_label.grid(row=4, column=0, sticky="w", padx=10, pady=7)

        self.heat_flux_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="W/m^2",
            placeholder_text_color="#4F4F4F",
        )
        self.heat_flux_input.grid(row=4, column=1, sticky="ew", padx=10, pady=7)

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

    def calculate(self):
        try:
            # Take all input parameters from gui elements
            type = self.type_selection.get()
            fluid = self.fluid_input.get()
            sat_temp = self.sat_temp_input.get()
            heat_flux = self.heat_flux_input.get()

            # Pass inputs to calculator to get results
            calculation_results = calculate_boilcond(
                type=type, fluid=fluid, sat_temp=sat_temp, heat_flux=heat_flux
            )

            self.results_label.configure(text=calculation_results)

        except ValueError:
            self.results_label.configure(text="Please enter valid inputs in all fields")

        except Exception as e:
            self.results_label.configure(text=f"An error occurred: {e}")