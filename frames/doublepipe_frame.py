import customtkinter as ctk
from frames import BaseFrame
from solvers.dphx_solver import calculate_dphx

class DoublePipeFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "DOUBLE PIPE HEAT EXCHANGER")

        # Create a dedicated frame for the input fields
        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        input_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Configure the grid columns. Column 1 will expand to fill space.
        input_frame.grid_columnconfigure((0,1,2,3), weight=1)

        # Section Title: Exchanger Settings
        exchanger_label = ctk.CTkLabel(
            input_frame,
            text="EXCHANGER SETTINGS",
            text_color="black",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        # Span across 2 columns and add padding below it
        exchanger_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Row 1: Length
        length_label = ctk.CTkLabel(input_frame, text="Length", text_color="black", font=ctk.CTkFont(size=16))
        length_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.length_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="m",
            placeholder_text_color="#4F4F4F",
            text_color="black"
        )
        self.length_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=7) # "ew" = expand east-west

        # Row 2: Material
        material_label = ctk.CTkLabel(input_frame, text="Material", text_color="black", font=ctk.CTkFont(size=16))
        material_label.grid(row=2, column=0, sticky="w", padx=5, pady=7)

        self.material_selection = ctk.CTkOptionMenu(
            input_frame,
            values=["Copper (Type K)", "Copper (Type M)", "Copper (Type L)", "Steel"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black",
            width=250
        )
        self.material_selection.grid(row=2, column=1, sticky="w", padx=5, pady=7) # "w" = align west

        # Row 3: Nominal Diameter
        nominal_label = ctk.CTkLabel(input_frame, text="Nominal Diameter", text_color="black", font=ctk.CTkFont(size=16))
        nominal_label.grid(row=3, column=0, sticky="w", padx=5, pady=7)

        self.nominal_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter as decimal",
            placeholder_text_color="#4F4F4F",
        )
        self.nominal_input.grid(row=3, column=1, sticky="ew", padx=5, pady=7)

        # Section Title: Fluid Settings
        fluid_label = ctk.CTkLabel(
            input_frame,
            text="FLUID SETTINGS",
            text_color="black",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        fluid_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=(15, 10))

        # Fluid 1
        fluid1_label = ctk.CTkLabel(
            input_frame,
            text="FLUID 1",
            text_color="black",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        fluid1_label.grid(row=5, column=0, sticky="w", padx=5, pady=7)

        self.fluid1_input = ctk.CTkOptionMenu(
            input_frame,
            values=["Water", "Hexane", "Ethylene Glycol", "Benzene", "Oil"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black",
            width=250
        )
        self.fluid1_input.grid(row=5, column=1, sticky="w", padx=10, pady=7)

        # Fluid 1 Inlet Temp
        fluid1_inlet_label = ctk.CTkLabel(
            input_frame,
            text="INLET TEMP",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        fluid1_inlet_label.grid(row=6, column=0, sticky="w", padx=10, pady=7)

        self.fluid1_inlet_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="deg C",
            placeholder_text_color="#4F4F4F",
        )
        self.fluid1_inlet_input.grid(row=6, column=1, sticky="ew", padx=10, pady=7)

        # Fluid 1 Outlet Temp
        fluid1_outlet_label = ctk.CTkLabel(
            input_frame,
            text="OUTLET TEMP",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        fluid1_outlet_label.grid(row=7, column=0, sticky="w", padx=10, pady=7)

        self.fluid1_outlet_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="deg C",
            placeholder_text_color="#4F4F4F",
        )
        self.fluid1_outlet_input.grid(row=7, column=1, sticky="ew", padx=10, pady=7)

        # Fluid 1 Mass Flow Rate
        fluid1_mfr_label = ctk.CTkLabel(
            input_frame,
            text="MASS FLOW RATE",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        fluid1_mfr_label.grid(row=8, column=0, sticky="w", padx=10, pady=7)

        self.fluid1_mfr_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="kg/s",
            placeholder_text_color="#4F4F4F",
        )
        self.fluid1_mfr_input.grid(row=8, column=1, sticky="ew", padx=10, pady=7)

        # Fluid 2
        fluid2_label = ctk.CTkLabel(
            input_frame,
            text="FLUID 2",
            text_color="black",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        fluid2_label.grid(row=5, column=2, sticky="w", padx=5, pady=7)

        self.fluid2_input = ctk.CTkOptionMenu(
            input_frame,
            values=["Water", "Hexane", "Ethylene Glycol", "Benzene", "Oil"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black",
            width=250
        )
        self.fluid2_input.grid(row=5, column=3, sticky="w", padx=10, pady=7)

        # Fluid 2 Inlet Temp
        fluid2_inlet_label = ctk.CTkLabel(
            input_frame,
            text="INLET TEMP",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        fluid2_inlet_label.grid(row=6, column=2, sticky="w", padx=10, pady=7)

        self.fluid2_inlet_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="deg C",
            placeholder_text_color="#4F4F4F",
        )
        self.fluid2_inlet_input.grid(row=6, column=3, sticky="ew", padx=10, pady=7)

        # Fluid 2 Outlet Temp
        fluid2_outlet_label = ctk.CTkLabel(
            input_frame,
            text="OUTLET TEMP",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        fluid2_outlet_label.grid(row=7, column=2, sticky="w", padx=10, pady=7)

        self.fluid2_outlet_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="deg C",
            placeholder_text_color="#4F4F4F",
        )
        self.fluid2_outlet_input.grid(row=7, column=3, sticky="ew", padx=10, pady=7)

        # Fluid 2 Mass Flow Rate
        fluid2_mfr_label = ctk.CTkLabel(
            input_frame,
            text="MASS FLOW RATE",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        fluid2_mfr_label.grid(row=8, column=2, sticky="w", padx=10, pady=7)

        self.fluid2_mfr_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="kg/s",
            placeholder_text_color="#4F4F4F",
        )
        self.fluid2_mfr_input.grid(row=8, column=3, sticky="ew", padx=10, pady=7)

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

    def calculate(self):
        try:
            # Take all input parameters from gui elements
            length = self.length_entry.get()
            material = self.material_selection.get()
            nominal_dia = self.nominal_input.get()
            fluid1 = self.fluid1_input.get()
            fluid1_inlet_temp = self.fluid1_inlet_input.get()
            fluid1_outlet_temp = self.fluid1_outlet_input.get()
            fluid1_mass_flow = self.fluid1_mfr_input.get()
            fluid2 = self.fluid2_input.get()
            fluid2_inlet_temp = self.fluid2_inlet_input.get()
            fluid2_outlet_temp = self.fluid2_outlet_input.get()
            fluid2_mass_flow = self.fluid2_mfr_input.get()

            # Pass inputs to calculator to get results
            calculation_results = calculate_dphx(
                length=length, material=material, nominal_dia=nominal_dia,
                fluid1=fluid1, fluid1_inlet_temp=fluid1_inlet_temp, fluid1_outlet_temp=fluid1_outlet_temp, fluid1_mass_flow=fluid1_mass_flow,
                fluid2=fluid2, fluid2_inlet_temp=fluid2_inlet_temp, fluid2_outlet_temp=fluid2_outlet_temp, fluid2_mass_flow=fluid2_mass_flow
            )

        except ValueError:
            self.results_label.configure(text = "Please enter valid inputs in all fields")

        except Exception as e:
            self.results_label.configure(text = f"An error occurred: {e}")