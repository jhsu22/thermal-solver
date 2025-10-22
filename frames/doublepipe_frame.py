import customtkinter as ctk
from frames import BaseFrame
from solvers.dphx_solver import calculate_dphx

class DoublePipeFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "DOUBLE PIPE HEAT EXCHANGER")

        self.materials = {
            "Copper": ["1/4", "3/8", "1/2", "5/8", "3/4", "1", "1 1/4", "1 1/2", "2", "2 1/2", "3", "3 1/2", "4", "5",
                       "6", "8", "10", "12"],
            "Steel": ["1/8", "1/4", "3/8", "1/2", "3/4", "1", "1 1/4", "1 1/2", "2", "2 1/2", "3", "3 1/2", "4", "5",
                      "6", "8", "10", "12"]
        }

        # Create a dedicated frame for the input fields
        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        input_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Configure the grid columns
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
        length_label = ctk.CTkLabel(
            input_frame,
            text="Length",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        length_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.length_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text_color="#4F4F4F",
            text_color="black"
        )
        self.length_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=7) # "ew" = expand east-west

        # Row 2: Material
        material_label = ctk.CTkLabel(input_frame, text="Material", text_color="black", font=ctk.CTkFont(size=16))
        material_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.material_selection = ctk.CTkOptionMenu(
            input_frame,
            values=["Copper", "Steel"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black",
            command=self.material_selected
        )
        self.material_selection.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        # Row 2 - Schedule Selector (Only for Steel)
        self.schedule_label = ctk.CTkLabel(input_frame, text="Schedule", text_color="black", font=ctk.CTkFont(size=16))
        self.schedule_selection = ctk.CTkOptionMenu(
            input_frame,
            values=["40 (std)", "80 (xs)", "160", "(xxs)"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black",
            width=250
        )

        # Row 2 - Type Selector (Only for Copper)
        self.type_label = ctk.CTkLabel(input_frame, text="Type", text_color="black", font=ctk.CTkFont(size=16))
        self.type_selection = ctk.CTkOptionMenu(
            input_frame,
            values=["Type K", "Type M", "Type L"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black"
        )

        # Row 3: Inner Nominal Diameter
        nominal_label_inner = ctk.CTkLabel(input_frame, text="Inner Nominal Dia", text_color="black",
                                     font=ctk.CTkFont(size=16))
        nominal_label_inner.grid(row=3, column=0, sticky="w", padx=5, pady=5)

        self.nominal_input_inner = ctk.CTkOptionMenu(
            input_frame,
            values=["1/4", "3/8", "1/2", "5/8", "3/4", "1", "1 1/4", "1 1/2", "2", "2 1/2", "3", "3 1/2", "4", "5", "6", "8", "10", "12"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black"
        )
        self.nominal_input_inner.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        # Outer Nominal Diameter
        nominal_label_outer = ctk.CTkLabel(input_frame, text="Outer Nominal Dia", text_color="black",
                                     font=ctk.CTkFont(size=16))
        nominal_label_outer.grid(row=3, column=2, sticky="ew", padx=0, pady=5)

        self.nominal_input_outer = ctk.CTkOptionMenu(
            input_frame,
            values=["1/4", "3/8", "1/2", "5/8", "3/4", "1", "1 1/4", "1 1/2", "2", "2 1/2", "3", "3 1/2", "4", "5", "6", "8", "10", "12"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black"
        )
        self.nominal_input_outer.grid(row=3, column=3, sticky="ew", padx=5, pady=5)

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
            values=["Water", "Hexane", "Ethanol", "Benzene", "R134a"],
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
            text="Inlet Temp",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        fluid1_inlet_label.grid(row=6, column=0, sticky="w", padx=10, pady=7)

        self.fluid1_inlet_input = ctk.CTkEntry(
            input_frame,
            placeholder_text_color="#4F4F4F",
        )
        self.fluid1_inlet_input.grid(row=6, column=1, sticky="ew", padx=10, pady=7)

        # Fluid 1 Mass Flow Rate
        fluid1_mfr_label = ctk.CTkLabel(
            input_frame,
            text="Mass Flow Rate",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        fluid1_mfr_label.grid(row=8, column=0, sticky="w", padx=10, pady=7)

        self.fluid1_mfr_input = ctk.CTkEntry(
            input_frame,
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
            values=["Water", "Hexane", "Ethanol", "Benzene", "R134a"],
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
            text="Inlet Temp",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        fluid2_inlet_label.grid(row=6, column=2, sticky="w", padx=10, pady=7)

        self.fluid2_inlet_input = ctk.CTkEntry(
            input_frame,
            placeholder_text_color="#4F4F4F",
        )
        self.fluid2_inlet_input.grid(row=6, column=3, sticky="ew", padx=10, pady=7)

        # Fluid 2 Mass Flow Rate
        fluid2_mfr_label = ctk.CTkLabel(
            input_frame,
            text="Mass Flow Rate",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        fluid2_mfr_label.grid(row=8, column=2, sticky="w", padx=10, pady=7)

        self.fluid2_mfr_input = ctk.CTkEntry(
            input_frame,
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

        # Results Label
        self.results_label = ctk.CTkLabel(
            input_frame,
            text="",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        self.results_label.grid(row=10, column=0, columnspan=4)

        self.update_placeholders()

        self.material_selected(self.material_selection.get())

    def material_selected(self, material):
        # Update the nominal diameter dropdown based on the selected material
        self.nominal_input_inner.configure(values=self.materials[material])
        self.nominal_input_outer.configure(values=self.materials[material])

        # Set the dropdown to the first available diameter to prevent errors
        self.nominal_input_inner.set(self.materials[material][0])
        self.nominal_input_outer.set(self.materials[material][0])

        if material == "Steel":
            self.schedule_label.grid(row=2, column=2, sticky="w", padx=15, pady=5)
            self.schedule_selection.grid(row=2, column=3, sticky="ew", padx=5, pady=5)
            self.type_selection.grid_forget()
            self.type_label.grid_forget()

        elif material == "Copper":
            self.type_label.grid(row=2, column=2, sticky="w", padx=15, pady=5)
            self.type_selection.grid(row=2, column=3, sticky="ew", padx=5, pady=5)
            self.schedule_label.grid_forget()
            self.schedule_selection.grid_forget()

    def update_placeholders(self):
        if self.controller.unit_system == "SI":
            self.length_entry.configure(placeholder_text="m")
            self.fluid1_inlet_input.configure(placeholder_text="°C")
            self.fluid1_mfr_input.configure(placeholder_text="kg/s")
            self.fluid2_inlet_input.configure(placeholder_text="°C")
            self.fluid2_mfr_input.configure(placeholder_text="kg/s")
        else: # Imperial
            self.length_entry.configure(placeholder_text="ft")
            self.fluid1_inlet_input.configure(placeholder_text="°F")
            self.fluid1_mfr_input.configure(placeholder_text="lb/s")
            self.fluid2_inlet_input.configure(placeholder_text="°F")
            self.fluid2_mfr_input.configure(placeholder_text="lb/s")

    def calculate(self):
        try:
            # Take all input parameters from gui elements
            length = self.length_entry.get()
            material = self.material_selection.get()
            nominal_dia_inner = self.nominal_input_inner.get()
            nominal_dia_outer = self.nominal_input_outer.get()
            fluid1 = self.fluid1_input.get()
            fluid1_inlet_temp = self.fluid1_inlet_input.get()
            fluid1_mass_flow = self.fluid1_mfr_input.get()
            fluid2 = self.fluid2_input.get()
            fluid2_inlet_temp = self.fluid2_inlet_input.get()
            fluid2_mass_flow = self.fluid2_mfr_input.get()

            schedule = None
            if material == "Steel":
                schedule = self.schedule_selection.get()

            ptype = None
            if material == "Copper":
                ptype = self.type_selection.get()

            # Pass inputs to calculator to get results
            calculation_results = calculate_dphx(
                length=length, material=material, nominal_dia_inner=nominal_dia_inner, nominal_dia_outer=nominal_dia_outer,
                fluid1=fluid1, fluid1_inlet_temp=fluid1_inlet_temp, fluid1_mass_flow=fluid1_mass_flow,
                fluid2=fluid2, fluid2_inlet_temp=fluid2_inlet_temp, fluid2_mass_flow=fluid2_mass_flow,
                schedule=schedule, ptype=ptype
            )
            results_text = "\n".join([f"{key.title()}: {value}" for key, value in calculation_results.items()])
            self.controller.display_results_window("Calculation Results",
                                                   f"==========================================\nDOUBLE PIPE HX RESULTS\n"
                                                   f"==========================================\n{results_text}")

        except ValueError as e:
            self.results_label.configure(text = f"An error occured: {e}")

        except Exception as e:
            self.results_label.configure(text = f"An error occurred: {e}")