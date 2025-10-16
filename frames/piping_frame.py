import customtkinter as ctk
from frames import BaseFrame
from solvers.piping_solver import calculate_piping


class PipingFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "PIPING")

        # --- Input Frame using .grid() for clean alignment ---
        # Create a dedicated frame for the input fields
        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        input_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Configure the grid columns.
        input_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="group1")

        # Section Title: Piping Settings
        exchanger_label = ctk.CTkLabel(
            input_frame,
            text="PIPING SETTINGS",
            text_color="black",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        # Span across 4 columns and add padding below it
        exchanger_label.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        # Row 1: Length
        length_label = ctk.CTkLabel(input_frame, text="Length", text_color="black", font=ctk.CTkFont(size=16))
        length_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.length_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="m",
            placeholder_text_color="#4F4F4F",
            text_color="black"
        )
        self.length_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # Row 2: Material
        material_label = ctk.CTkLabel(input_frame, text="Material", text_color="black", font=ctk.CTkFont(size=16))
        material_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.material_selection = ctk.CTkOptionMenu(
            input_frame,
            values=["Copper (Type K)", "Copper (Type M)", "Copper (Type L)", "Steel"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black"
        )
        self.material_selection.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        # Row 3: Nominal Diameter
        nominal_label = ctk.CTkLabel(input_frame, text="Nominal Diameter", text_color="black",
                                     font=ctk.CTkFont(size=16))
        nominal_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.nominal_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter as decimal",
            placeholder_text_color="#4F4F4F",
        )
        self.nominal_input.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        # Section Title: Fluid Settings
        fluid_label = ctk.CTkLabel(
            input_frame,
            text="FLUID SETTINGS",
            text_color="black",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        fluid_label.grid(row=4, column=0, columnspan=4, sticky="w", pady=(20, 10))

        # Fluid
        fluid_label = ctk.CTkLabel(
            input_frame,
            text="FLUID",
            text_color="black",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        fluid_label.grid(row=5, column=0, sticky="w", padx=5, pady=7)

        self.fluid_input = ctk.CTkOptionMenu(
            input_frame,
            values=["Water", "Hexane", "Ethylene Glycol", "Benzene", "Oil"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black")
        self.fluid_input.grid(row=5, column=1, sticky="ew", padx=10, pady=7)

        # Fluid Inlet Temp
        fluid_inlet_label = ctk.CTkLabel(
            input_frame,
            text="Inlet Temp",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        fluid_inlet_label.grid(row=6, column=0, sticky="w", padx=10, pady=7)

        self.fluid_inlet_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="°C",
            placeholder_text_color="#4F4F4F",
        )
        self.fluid_inlet_input.grid(row=6, column=1, sticky="ew", padx=10, pady=7)

        # Fluid Mass Flow Rate
        fluid_mfr_label = ctk.CTkLabel(
            input_frame,
            text="Mass Flow Rate",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        fluid_mfr_label.grid(row=7, column=0, sticky="w", padx=10, pady=7)

        self.fluid_mfr_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="kg/s",
            placeholder_text_color="#4F4F4F",
        )
        self.fluid_mfr_input.grid(row=7, column=1, sticky="ew", padx=10, pady=7)

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
        calculate_button.grid(row=8, column=0, columnspan=4, pady=50)

        # Results Label
        self.results_label = ctk.CTkLabel(
            input_frame,
            text="",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        self.results_label.grid(row=9, column=0, columnspan=4)

    def calculate(self):
        try:
            # Take all input parameters from gui elements
            length = self.length_entry.get()
            material = self.material_selection.get()
            nominal_dia = self.nominal_input.get()
            fluid = self.fluid_input.get()
            fluid_inlet_temp = self.fluid_inlet_input.get()
            fluid_mass_flow = self.fluid_mfr_input.get()

            # Pass inputs to calculator to get results
            calculation_results = calculate_piping(
                length=length, material=material, nominal_dia=nominal_dia,
                fluid=fluid, fluid_inlet_temp=fluid_inlet_temp, fluid_mass_flow=fluid_mass_flow
            )

            self.results_label.configure(text=calculation_results)

        except ValueError:
            self.results_label.configure(text="Please enter valid inputs in all fields")

        except Exception as e:
            self.results_label.configure(text=f"An error occurred: {e}")