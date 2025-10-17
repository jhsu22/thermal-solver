import customtkinter as ctk
from frames import BaseFrame
from solvers.heatpipe_solver import calculate_heatpipe


class HeatPipeFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "HEAT PIPE")

        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        input_frame.pack(pady=10, padx=20, fill="both", expand=True)

        input_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="group1")

        # --- Section: Heat Pipe Geometry ---
        geometry_label = ctk.CTkLabel(
            input_frame, text="HEAT PIPE GEOMETRY", text_color="black", font=ctk.CTkFont(size=18, weight="bold")
        )
        geometry_label.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        evap_len_label = ctk.CTkLabel(input_frame, text="Evaporator Length", text_color="black",
                                      font=ctk.CTkFont(size=16))
        evap_len_label.grid(row=1, column=0, sticky="w", padx=5, pady=7)
        self.evap_len_entry = ctk.CTkEntry(input_frame, placeholder_text_color="#4F4F4F")
        self.evap_len_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=7)

        adia_len_label = ctk.CTkLabel(input_frame, text="Adiabatic Length", text_color="black",
                                      font=ctk.CTkFont(size=16))
        adia_len_label.grid(row=2, column=0, sticky="w", padx=5, pady=7)
        self.adia_len_entry = ctk.CTkEntry(input_frame, placeholder_text_color="#4F4F4F")
        self.adia_len_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=7)

        cond_len_label = ctk.CTkLabel(input_frame, text="Condenser Length", text_color="black",
                                      font=ctk.CTkFont(size=16))
        cond_len_label.grid(row=3, column=0, sticky="w", padx=5, pady=7)
        self.cond_len_entry = ctk.CTkEntry(input_frame, placeholder_text_color="#4F4F4F")
        self.cond_len_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=7)

        vapor_diam_label = ctk.CTkLabel(input_frame, text="Vapor Core Diameter", text_color="black",
                                        font=ctk.CTkFont(size=16))
        vapor_diam_label.grid(row=1, column=2, sticky="w", padx=15, pady=7)
        self.vapor_diam_entry = ctk.CTkEntry(input_frame, placeholder_text_color="#4F4F4F")
        self.vapor_diam_entry.grid(row=1, column=3, sticky="ew", padx=5, pady=7)

        orientation_label = ctk.CTkLabel(input_frame, text="Orientation", text_color="black", font=ctk.CTkFont(size=16))
        orientation_label.grid(row=2, column=2, sticky="w", padx=15, pady=7)
        self.orientation_selection = ctk.CTkOptionMenu(
            input_frame, values=["Horizontal", "Vertical"], text_color="black", font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd", dropdown_hover_color="#999999", dropdown_text_color="black"
        )
        self.orientation_selection.grid(row=2, column=3, sticky="ew", padx=5, pady=7)

        # --- Section: Wick Structure ---
        wick_label = ctk.CTkLabel(
            input_frame, text="WICK STRUCTURE", text_color="black", font=ctk.CTkFont(size=18, weight="bold")
        )
        wick_label.grid(row=4, column=0, columnspan=4, sticky="w", pady=(20, 10))

        wick_mat_label = ctk.CTkLabel(input_frame, text="Wick Material", text_color="black", font=ctk.CTkFont(size=16))
        wick_mat_label.grid(row=5, column=0, sticky="w", padx=5, pady=7)
        self.wick_material_selection = ctk.CTkOptionMenu(
            input_frame, values=["Stainless Steel Screen", "Copper Screen", "Sintered Nickel"], text_color="black",
            font=ctk.CTkFont(size=14), dropdown_fg_color="#bfbdbd", dropdown_hover_color="#999999",
            dropdown_text_color="black"
        )
        self.wick_material_selection.grid(row=5, column=1, sticky="ew", padx=5, pady=7)

        mesh_label = ctk.CTkLabel(input_frame, text="Mesh Number", text_color="black", font=ctk.CTkFont(size=16))
        mesh_label.grid(row=6, column=0, sticky="w", padx=5, pady=7)
        self.mesh_entry = ctk.CTkEntry(input_frame, placeholder_text="#400", placeholder_text_color="#4F4F4F")
        self.mesh_entry.grid(row=6, column=1, sticky="ew", padx=5, pady=7)

        wire_diam_label = ctk.CTkLabel(input_frame, text="Wire Diameter", text_color="black", font=ctk.CTkFont(size=16))
        wire_diam_label.grid(row=5, column=2, sticky="w", padx=15, pady=7)
        self.wire_diam_entry = ctk.CTkEntry(input_frame, placeholder_text_color="#4F4F4F")
        self.wire_diam_entry.grid(row=5, column=3, sticky="ew", padx=5, pady=7)

        layers_label = ctk.CTkLabel(input_frame, text="Number of Layers", text_color="black", font=ctk.CTkFont(size=16))
        layers_label.grid(row=6, column=2, sticky="w", padx=15, pady=7)
        self.layers_entry = ctk.CTkEntry(input_frame, placeholder_text="e.g., 3", placeholder_text_color="#4F4F4F")
        self.layers_entry.grid(row=6, column=3, sticky="ew", padx=5, pady=7)

        # --- Section: Operating Conditions ---
        op_label = ctk.CTkLabel(
            input_frame, text="OPERATING CONDITIONS", text_color="black", font=ctk.CTkFont(size=18, weight="bold")
        )
        op_label.grid(row=7, column=0, columnspan=4, sticky="w", pady=(20, 10))

        working_fluid_label = ctk.CTkLabel(input_frame, text="Working Fluid", text_color="black",
                                           font=ctk.CTkFont(size=16))
        working_fluid_label.grid(row=8, column=0, sticky="w", padx=5, pady=7)
        self.working_fluid_input = ctk.CTkOptionMenu(
            input_frame, values=["Water", "Ammonia", "Methanol"], text_color="black", font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd", dropdown_hover_color="#999999", dropdown_text_color="black"
        )
        self.working_fluid_input.grid(row=8, column=1, sticky="ew", padx=5, pady=7)

        op_temp_label = ctk.CTkLabel(input_frame, text="Operating Temperature", text_color="black",
                                     font=ctk.CTkFont(size=16))
        op_temp_label.grid(row=8, column=2, sticky="w", padx=15, pady=7)
        self.op_temp_input = ctk.CTkEntry(input_frame, placeholder_text_color="#4F4F4F")
        self.op_temp_input.grid(row=8, column=3, sticky="ew", padx=5, pady=7)

        # --- Calculate Button and Results ---
        calculate_button = ctk.CTkButton(
            input_frame, text="Calculate!", text_color="black", font=ctk.CTkFont(size=16),
            fg_color="#689CE0", hover_color="#5480BA", height=45, width=150, command=self.calculate
        )
        calculate_button.grid(row=9, column=0, columnspan=4, pady=40)

        self.results_label = ctk.CTkLabel(input_frame, text="", text_color="black", font=ctk.CTkFont(size=16),
                                          justify="left")
        self.results_label.grid(row=10, column=0, columnspan=4)
        self.update_placeholders()

    def update_placeholders(self):
        if self.controller.unit_system == "SI":
            self.evap_len_entry.configure(placeholder_text="cm")
            self.adia_len_entry.configure(placeholder_text="cm")
            self.cond_len_entry.configure(placeholder_text="cm")
            self.vapor_diam_entry.configure(placeholder_text="mm")
            self.wire_diam_entry.configure(placeholder_text="in")
            self.op_temp_input.configure(placeholder_text="°C")
        else: # Imperial
            self.evap_len_entry.configure(placeholder_text="in")
            self.adia_len_entry.configure(placeholder_text="in")
            self.cond_len_entry.configure(placeholder_text="in")
            self.vapor_diam_entry.configure(placeholder_text="in")
            self.wire_diam_entry.configure(placeholder_text="in")
            self.op_temp_input.configure(placeholder_text="°F")

    def calculate(self):
        try:
            # Gather all input values
            inputs = {
                "evap_len": self.evap_len_entry.get(),
                "adia_len": self.adia_len_entry.get(),
                "cond_len": self.cond_len_entry.get(),
                "vapor_diam": self.vapor_diam_entry.get(),
                "orientation": self.orientation_selection.get(),
                "wick_material": self.wick_material_selection.get(),
                "mesh": self.mesh_entry.get(),
                "wire_diam": self.wire_diam_entry.get(),
                "layers": self.layers_entry.get(),
                "working_fluid": self.working_fluid_input.get(),
                "op_temp": self.op_temp_input.get()
            }

            # Pass inputs to calculator
            calculation_results = calculate_heatpipe(**inputs)

            # Format and display results
            results_text = (
                f"Capillary Limit: {calculation_results['capillary']}\n"
                f"Sonic Limit: {calculation_results['sonic']}\n"
                f"Entrainment Limit: {calculation_results['entrainment']}\n"
                f"Boiling Limit: {calculation_results['boiling']}"
            )
            self.results_label.configure(text=results_text)

        except ValueError:
            self.results_label.configure(text="Please enter valid inputs in all fields.")
        except Exception as e:
            self.results_label.configure(text=f"An error occurred: {e}")