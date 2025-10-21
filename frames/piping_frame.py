import customtkinter as ctk
from frames import BaseFrame
from solvers.piping_solver import calculate_piping


class PipingFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "PIPING")

        self.materials = {
            "Copper": ["1/4", "3/8", "1/2", "5/8", "3/4", "1", "1 1/4", "1 1/2", "2", "2 1/2", "3", "3 1/2", "4", "5",
                       "6", "8", "10", "12"],
            "Steel": ["1/8", "1/4", "3/8", "1/2", "3/4", "1", "1 1/4", "1 1/2", "2", "2 1/2", "3", "3 1/2", "4", "5",
                      "6", "8", "10", "12"]
        }

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
            placeholder_text_color="#4F4F4F",
            text_color="black",
            width=150
        )
        self.length_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

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

        # Row 3: Nominal Diameter
        nominal_label = ctk.CTkLabel(input_frame, text="Nominal Diameter", text_color="black",
                                     font=ctk.CTkFont(size=16))
        nominal_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)

        self.nominal_input = ctk.CTkOptionMenu(
            input_frame,
            values=["1/4", "3/8", "1/2", "5/8", "3/4", "1", "1 1/4", "1 1/2", "2", "2 1/2", "3", "3 1/2", "4", "5", "6", "8", "10", "12"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black"
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
            values=["Water", "Hexane", "Kerosene", "Glycerine", "Mercury", "Ethylene Glycol", "Ethyl Alcohol"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black")
        self.fluid_input.grid(row=5, column=1, sticky="ew", padx=10, pady=7)

        # Fluid Volumetric Flow Rate
        fluid_fr_label = ctk.CTkLabel(
            input_frame,
            text="Volumetric Flow Rate",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        fluid_fr_label.grid(row=6, column=0, sticky="w", padx=10, pady=7)

        self.fluid_fr_input = ctk.CTkEntry(
            input_frame,
            placeholder_text_color="#4F4F4F",
        )
        self.fluid_fr_input.grid(row=6, column=1, sticky="ew", padx=10, pady=7)

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
        calculate_button.grid(row=7, column=0, columnspan=4, pady=50)

        # Results Label
        self.results_label = ctk.CTkLabel(
            input_frame,
            text="",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        self.results_label.grid(row=8, column=0, columnspan=4)
        self.update_placeholders()

        self.material_selected(self.material_selection.get())

    def material_selected(self, material):
        # Update the nominal diameter dropdown based on the selected material
        self.nominal_input.configure(values=self.materials[material])

        # Set the dropdown to the first available diameter to prevent errors
        self.nominal_input.set(self.materials[material][0])

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
            self.fluid_fr_input.configure(placeholder_text="m³/s")
        else: # Imperial
            self.length_entry.configure(placeholder_text="ft")
            self.fluid_fr_input.configure(placeholder_text="ft³/s")

    def calculate(self):
        try:
            # Take all input parameters from gui elements
            length = self.length_entry.get()
            material = self.material_selection.get()
            nominal_dia = self.nominal_input.get()
            fluid = self.fluid_input.get()
            fluid_flow = self.fluid_fr_input.get()

            schedule = None
            if material == "Steel":
                schedule = self.schedule_selection.get()

            ptype = None
            if material == "Copper":
                ptype = self.type_selection.get()

            # Pass inputs to calculator to get results
            calculation_results = calculate_piping(
                length=float(length), material=material, nominal_dia=nominal_dia,
                fluid=fluid, fluid_flow=float(fluid_flow), schedule=schedule, ptype=ptype, unit_system=self.controller.unit_system
            )

            self.controller.display_results_window("Calculation Results", f"=================\nPIPING RESULTS\n=================\n{calculation_results}")

        except ValueError:
            self.results_label.configure(text="Please enter valid inputs in all fields")

        except Exception as e:
            self.results_label.configure(text=f"An error occurred: {e}")