import customtkinter as ctk
from frames import BaseFrame
from solvers.shelltube_solver import calculate_shelltube


class ShellTubeFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "SHELL & TUBE HEAT EXCHANGER")

        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        input_frame.pack(pady=10, padx=20, fill="both", expand=True)

        input_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="group1")

        # Section Title: Exchanger Settings
        exchanger_label = ctk.CTkLabel(
            input_frame,
            text="EXCHANGER SETTINGS",
            text_color="black",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        exchanger_label.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        # --- Column 0 & 1 ---
        # Length
        length_label = ctk.CTkLabel(input_frame, text="Tube Length", text_color="black", font=ctk.CTkFont(size=16))
        length_label.grid(row=1, column=0, sticky="w", padx=5, pady=7)
        self.length_entry = ctk.CTkEntry(input_frame, placeholder_text_color="#4F4F4F")
        self.length_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=7)

        # Tube OD
        tube_od_label = ctk.CTkLabel(input_frame, text="Tube OD (in)", text_color="black", font=ctk.CTkFont(size=16))
        tube_od_label.grid(row=2, column=0, sticky="w", padx=5, pady=7)
        self.tube_od_entry = ctk.CTkOptionMenu(
            input_frame,
            values=["0.75", "1"],
            text_color="black", font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd", dropdown_hover_color="#999999",
            dropdown_text_color="black"
        )
        self.tube_od_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=7)

        # Tube BWG
        tube_bwg_label = ctk.CTkLabel(input_frame, text="Tube Gauge (BWG)", text_color="black",
                                      font=ctk.CTkFont(size=16))
        tube_bwg_label.grid(row=3, column=0, sticky="w", padx=5, pady=7)
        self.tube_bwg_selection = ctk.CTkOptionMenu(
            input_frame,
            values=["8","9","10","11","12","13","14","15","16","17","18"],
            text_color="black", font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd", dropdown_hover_color="#999999",
            dropdown_text_color="black"
        )
        self.tube_bwg_selection.grid(row=3, column=1, sticky="ew", padx=5, pady=7)

        # Number of Passes
        passes_label = ctk.CTkLabel(input_frame, text="Number of Tube Passes", text_color="black",
                                    font=ctk.CTkFont(size=16))
        passes_label.grid(row=4, column=0, sticky="w", padx=5, pady=7)
        self.passes_input = ctk.CTkOptionMenu(
            input_frame,
            values=["1", "2", "4", "6", "8"],
            text_color="black", font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd", dropdown_hover_color="#999999",
            dropdown_text_color="black"
        )
        self.passes_input.grid(row=4, column=1, sticky="ew", padx=5, pady=7)

        # --- Column 2 & 3 ---
        # Shell ID
        shell_id_label = ctk.CTkLabel(input_frame, text="Shell ID", text_color="black", font=ctk.CTkFont(size=16))
        shell_id_label.grid(row=1, column=2, sticky="w", padx=15, pady=7)
        self.shell_id_entry = ctk.CTkOptionMenu(
            input_frame,
            values=["8","10", "12", "13.25", "17.25", "19.25", "21.25", "23.25", "25", "27", "29", "31", "33", "35", "37", "39"],
            text_color="black", font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd", dropdown_hover_color="#999999",
            dropdown_text_color="black"
        )
        self.shell_id_entry.grid(row=1, column=3, sticky="ew", padx=5, pady=7)

        # Tube Arrangement
        arrangement_label = ctk.CTkLabel(input_frame, text="Tube Arrangement", text_color="black",
                                         font=ctk.CTkFont(size=16))
        arrangement_label.grid(row=2, column=2, sticky="w", padx=15, pady=7)
        self.arrangement_selection = ctk.CTkOptionMenu(
            input_frame,
            values=["Triangular", "Square"], text_color="black", font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd", dropdown_hover_color="#999999",
            dropdown_text_color="black"
        )
        self.arrangement_selection.grid(row=2, column=3, sticky="ew", padx=5, pady=7)

        # Tube Pitch
        tube_pitch_label = ctk.CTkLabel(input_frame, text="Tube Pitch (in)", text_color="black", font=ctk.CTkFont(size=16))
        tube_pitch_label.grid(row=3, column=2, sticky="w", padx=15, pady=7)
        self.tube_pitch_entry = ctk.CTkOptionMenu(
            input_frame,
            values=["0.9375", "1", "1.25"],
            text_color="black", font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd", dropdown_hover_color="#999999",
            dropdown_text_color="black"
        )
        self.tube_pitch_entry.grid(row=3, column=3, sticky="ew", padx=5, pady=7)

        # Number of Baffles
        baffles_label = ctk.CTkLabel(input_frame, text="Number of Baffles", text_color="black",
                                     font=ctk.CTkFont(size=16))
        baffles_label.grid(row=4, column=2, sticky="w", padx=15, pady=7)
        self.baffles_input = ctk.CTkEntry(input_frame, placeholder_text="e.g., 10", placeholder_text_color="#4F4F4F")
        self.baffles_input.grid(row=4, column=3, sticky="ew", padx=5, pady=7)

        # Section Title: Fluid Settings
        fluid_label = ctk.CTkLabel(
            input_frame, text="FLUID SETTINGS", text_color="black", font=ctk.CTkFont(size=18, weight="bold")
        )
        fluid_label.grid(row=5, column=0, columnspan=4, sticky="w", pady=(20, 10))

        # --- Fluid Inputs ---
        # Fluid Selection
        warm_fluid_label = ctk.CTkLabel(input_frame, text="WARM FLUID", text_color="black",
                                         font=ctk.CTkFont(size=16, weight="bold"))
        warm_fluid_label.grid(row=7, column=0, sticky="w", padx=5, pady=7)
        self.warm_fluid_input = ctk.CTkOptionMenu(input_frame,
                                                   values=["Water", "Hexane", "Ethanol", "Benzene", "R134a"],
                                                   text_color="black", font=ctk.CTkFont(size=14),
                                                   dropdown_fg_color="#bfbdbd", dropdown_hover_color="#999999",
                                                   dropdown_text_color="black")
        self.warm_fluid_input.grid(row=7, column=1, sticky="ew", padx=5, pady=7)

        cool_fluid_label = ctk.CTkLabel(input_frame, text="COOL FLUID", text_color="black",
                                        font=ctk.CTkFont(size=16, weight="bold"))
        cool_fluid_label.grid(row=7, column=2, sticky="w", padx=15, pady=7)
        self.cool_fluid_input = ctk.CTkOptionMenu(input_frame,
                                                  values=["Water", "Hexane", "Ethanol", "Benzene", "R134a"],
                                                  text_color="black", font=ctk.CTkFont(size=14),
                                                  dropdown_fg_color="#bfbdbd", dropdown_hover_color="#999999",
                                                  dropdown_text_color="black")
        self.cool_fluid_input.grid(row=7, column=3, sticky="ew", padx=5, pady=7)

        # Inlet Temp
        warm_inlet_label = ctk.CTkLabel(input_frame, text="Inlet Temp", text_color="black", font=ctk.CTkFont(size=16))
        warm_inlet_label.grid(row=8, column=0, sticky="w", padx=5, pady=7)
        self.warm_fluid_inlet_input = ctk.CTkEntry(input_frame, placeholder_text_color="#4F4F4F")
        self.warm_fluid_inlet_input.grid(row=8, column=1, sticky="ew", padx=5, pady=7)

        cool_inlet_label = ctk.CTkLabel(input_frame, text="Inlet Temp", text_color="black", font=ctk.CTkFont(size=16))
        cool_inlet_label.grid(row=8, column=2, sticky="w", padx=15, pady=7)
        self.cool_fluid_inlet_input = ctk.CTkEntry(input_frame, placeholder_text_color="#4F4F4F")
        self.cool_fluid_inlet_input.grid(row=8, column=3, sticky="ew", padx=5, pady=7)

        # Mass Flow Rate
        warm_mfr_label = ctk.CTkLabel(input_frame, text="Mass Flow Rate", text_color="black",
                                       font=ctk.CTkFont(size=16))
        warm_mfr_label.grid(row=9, column=0, sticky="w", padx=5, pady=7)
        self.warm_fluid_mfr_input = ctk.CTkEntry(input_frame, placeholder_text_color="#4F4F4F")
        self.warm_fluid_mfr_input.grid(row=9, column=1, sticky="ew", padx=5, pady=7)

        cool_mfr_label = ctk.CTkLabel(input_frame, text="Mass Flow Rate", text_color="black", font=ctk.CTkFont(size=16))
        cool_mfr_label.grid(row=9, column=2, sticky="w", padx=15, pady=7)
        self.cool_fluid_mfr_input = ctk.CTkEntry(input_frame, placeholder_text_color="#4F4F4F")
        self.cool_fluid_mfr_input.grid(row=9, column=3, sticky="ew", padx=5, pady=7)

        # Calculate button
        calculate_button = ctk.CTkButton(
            input_frame, text="Calculate!", text_color="black", font=ctk.CTkFont(size=16),
            fg_color="#689CE0", hover_color="#5480BA", height=45, width=150, command=self.calculate
        )
        calculate_button.grid(row=11, column=0, columnspan=4, pady=40)

        # Results Label
        self.results_label = ctk.CTkLabel(input_frame, text="", text_color="black", font=ctk.CTkFont(size=16))
        self.results_label.grid(row=12, column=0, columnspan=4)
        self.update_placeholders()

    def update_placeholders(self):
        if self.controller.unit_system == "SI":
            self.length_entry.configure(placeholder_text="m")
            self.warm_fluid_inlet_input.configure(placeholder_text="°C")
            self.cool_fluid_inlet_input.configure(placeholder_text="°C")
            self.warm_fluid_mfr_input.configure(placeholder_text="kg/s")
            self.cool_fluid_mfr_input.configure(placeholder_text="kg/s")
        else: # Imperial
            self.length_entry.configure(placeholder_text="ft")
            self.warm_fluid_inlet_input.configure(placeholder_text="°F")
            self.cool_fluid_inlet_input.configure(placeholder_text="°F")
            self.warm_fluid_mfr_input.configure(placeholder_text="lb/s")
            self.cool_fluid_mfr_input.configure(placeholder_text="lb/s")

    def calculate(self):
        try:
            # Take all input parameters from gui elements
            length = self.length_entry.get()
            shell_id = self.shell_id_entry.get()
            tube_od = self.tube_od_entry.get()
            tube_bwg = self.tube_bwg_selection.get()
            arrangement = self.arrangement_selection.get()
            tube_pitch = self.tube_pitch_entry.get()
            passes = self.passes_input.get()
            baffles = self.baffles_input.get()
            warm_fluid = self.warm_fluid_input.get()
            warm_fluid_inlet_temp = self.warm_fluid_inlet_input.get()
            warm_fluid_mass_flow = self.warm_fluid_mfr_input.get()
            cool_fluid = self.cool_fluid_input.get()
            cool_fluid_inlet_temp = self.cool_fluid_inlet_input.get()
            cool_fluid_mass_flow = self.cool_fluid_mfr_input.get()

            # Pass inputs to calculator to get results
            calculation_results = calculate_shelltube(
                length=length, shell_id=shell_id, tube_od=tube_od, tube_bwg=tube_bwg,
                arrangement=arrangement, tube_pitch=tube_pitch, passes=passes, baffles=baffles,
                warm_fluid=warm_fluid, warm_fluid_inlet_temp=warm_fluid_inlet_temp,
                warm_fluid_mass_flow=warm_fluid_mass_flow,
                cool_fluid=cool_fluid, cool_fluid_inlet_temp=cool_fluid_inlet_temp,
                cool_fluid_mass_flow=cool_fluid_mass_flow
            )
            results_text = "\n".join([f"{key.title()}: {value}" for key, value in calculation_results.items()])
            self.controller.display_results_window("Calculation Results",
                                                   f"==========================================\nSHELL TUBE HX RESULTS\n"
                                                   f"==========================================\n{results_text}")

        except ValueError as e:
            self.results_label.configure(text=f"An error occurred: {e}")

        except Exception as e:
            self.results_label.configure(text=f"An error occurred: {e}")