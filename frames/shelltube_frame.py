import customtkinter as ctk
from frames import BaseFrame
from solvers.shelltube_solver import calculate_shelltube


class ShellTubeFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "SHELL & TUBE HEAT EXCHANGER")

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

        # Number of Passes
        passes_label = ctk.CTkLabel(input_frame, text="Number of Passes", text_color="black", font=ctk.CTkFont(size=16))
        passes_label.grid(row=1, column=0, sticky="w", padx=5, pady=7)

        self.passes_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="e.g., 1, 2, 4",
            placeholder_text_color="#4F4F4F",
        )
        self.passes_input.grid(row=1, column=1, sticky="ew", padx=5, pady=7)

        # Tube Arrangement
        arrangement_label = ctk.CTkLabel(input_frame, text="Tube Arrangement", text_color="black",
                                         font=ctk.CTkFont(size=16))
        arrangement_label.grid(row=2, column=0, sticky="w", padx=5, pady=7)

        self.arrangement_selection = ctk.CTkOptionMenu(
            input_frame,
            values=["Triangular", "Square"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black",
            width=250
        )
        self.arrangement_selection.grid(row=2, column=1, sticky="w", padx=5, pady=7)

        # Section Title: Fluid Settings
        fluid_label = ctk.CTkLabel(
            input_frame,
            text="FLUID SETTINGS",
            text_color="black",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        fluid_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=(15, 10))

        # Shell-Side Fluid
        shell_fluid_label = ctk.CTkLabel(
            input_frame,
            text="SHELL-SIDE FLUID",
            text_color="black",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        shell_fluid_label.grid(row=5, column=0, sticky="w", padx=5, pady=7)

        self.shell_fluid_input = ctk.CTkOptionMenu(
            input_frame,
            values=["Water", "Hexane", "Ethylene Glycol", "Benzene", "Oil"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black",
            width=250
        )
        self.shell_fluid_input.grid(row=5, column=1, sticky="w", padx=10, pady=7)

        # Shell-Side Fluid Inlet Temp
        shell_fluid_inlet_label = ctk.CTkLabel(
            input_frame,
            text="INLET TEMP",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        shell_fluid_inlet_label.grid(row=6, column=0, sticky="w", padx=10, pady=7)

        self.shell_fluid_inlet_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="deg C",
            placeholder_text_color="#4F4F4F",
        )
        self.shell_fluid_inlet_input.grid(row=6, column=1, sticky="ew", padx=10, pady=7)

        # Shell-Side Fluid Mass Flow Rate
        shell_fluid_mfr_label = ctk.CTkLabel(
            input_frame,
            text="MASS FLOW RATE",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        shell_fluid_mfr_label.grid(row=8, column=0, sticky="w", padx=10, pady=7)

        self.shell_fluid_mfr_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="kg/s",
            placeholder_text_color="#4F4F4F",
        )
        self.shell_fluid_mfr_input.grid(row=8, column=1, sticky="ew", padx=10, pady=7)

        # Tube-Side Fluid
        tube_fluid_label = ctk.CTkLabel(
            input_frame,
            text="TUBE-SIDE FLUID",
            text_color="black",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        tube_fluid_label.grid(row=5, column=2, sticky="w", padx=5, pady=7)

        self.tube_fluid_input = ctk.CTkOptionMenu(
            input_frame,
            values=["Water", "Hexane", "Ethylene Glycol", "Benzene", "Oil"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black",
            width=250
        )
        self.tube_fluid_input.grid(row=5, column=3, sticky="w", padx=10, pady=7)

        # Tube-Side Fluid Inlet Temp
        tube_fluid_inlet_label = ctk.CTkLabel(
            input_frame,
            text="INLET TEMP",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        tube_fluid_inlet_label.grid(row=6, column=2, sticky="w", padx=10, pady=7)

        self.tube_fluid_inlet_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="deg C",
            placeholder_text_color="#4F4F4F",
        )
        self.tube_fluid_inlet_input.grid(row=6, column=3, sticky="ew", padx=10, pady=7)

        # Tube-Side Fluid Mass Flow Rate
        tube_fluid_mfr_label = ctk.CTkLabel(
            input_frame,
            text="MASS FLOW RATE",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        tube_fluid_mfr_label.grid(row=8, column=2, sticky="w", padx=10, pady=7)

        self.tube_fluid_mfr_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="kg/s",
            placeholder_text_color="#4F4F4F",
        )
        self.tube_fluid_mfr_input.grid(row=8, column=3, sticky="ew", padx=10, pady=7)

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
            passes = self.passes_input.get()
            arrangement = self.arrangement_selection.get()
            shell_fluid = self.shell_fluid_input.get()
            shell_fluid_inlet_temp = self.shell_fluid_inlet_input.get()
            shell_fluid_mass_flow = self.shell_fluid_mfr_input.get()
            tube_fluid = self.tube_fluid_input.get()
            tube_fluid_inlet_temp = self.tube_fluid_inlet_input.get()
            tube_fluid_mass_flow = self.tube_fluid_mfr_input.get()

            # Pass inputs to calculator to get results
            calculation_results = calculate_shelltube(
                passes=passes, arrangement=arrangement, shell_fluid=shell_fluid,
                shell_fluid_inlet_temp=shell_fluid_inlet_temp, shell_fluid_mass_flow=shell_fluid_mass_flow,
                tube_fluid=tube_fluid, tube_fluid_inlet_temp=tube_fluid_inlet_temp,
                tube_fluid_mass_flow=tube_fluid_mass_flow
            )

            self.results_label.configure(text=calculation_results)

        except ValueError:
            self.results_label.configure(text="Please enter valid inputs in all fields")

        except Exception as e:
            self.results_label.configure(text=f"An error occurred: {e}")