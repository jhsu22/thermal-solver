import customtkinter as ctk
from frames import BaseFrame
from solvers.heatpipe_solver import calculate_heatpipe


class HeatPipeFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "HEAT PIPE")

        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        input_frame.pack(pady=10, padx=20, fill="both", expand=True)

        input_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Section Title: Heat Pipe Settings
        heatpipe_label = ctk.CTkLabel(
            input_frame,
            text="HEAT PIPE SETTINGS",
            text_color="black",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        heatpipe_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Wick Material
        wick_material_label = ctk.CTkLabel(input_frame, text="Wick Material", text_color="black",
                                           font=ctk.CTkFont(size=16))
        wick_material_label.grid(row=1, column=0, sticky="w", padx=5, pady=7)

        self.wick_material_selection = ctk.CTkOptionMenu(
            input_frame,
            values=["Copper", "Steel", "Sintered Nickel"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black",
            width=250
        )
        self.wick_material_selection.grid(row=1, column=1, sticky="w", padx=5, pady=7)

        # Working Fluid
        working_fluid_label = ctk.CTkLabel(input_frame, text="Working Fluid", text_color="black",
                                           font=ctk.CTkFont(size=16))
        working_fluid_label.grid(row=2, column=0, sticky="w", padx=5, pady=7)

        self.working_fluid_input = ctk.CTkOptionMenu(
            input_frame,
            values=["Water", "Ammonia", "Methanol"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black",
            width=250
        )
        self.working_fluid_input.grid(row=2, column=1, sticky="w", padx=10, pady=7)

        # Heat Pipe Dimensions
        dimensions_label = ctk.CTkLabel(input_frame, text="Dimensions (LxD)", text_color="black",
                                        font=ctk.CTkFont(size=16))
        dimensions_label.grid(row=3, column=0, sticky="w", padx=5, pady=7)

        self.dimensions_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="m x m",
            placeholder_text_color="#4F4F4F",
        )
        self.dimensions_input.grid(row=3, column=1, sticky="ew", padx=5, pady=7)

        # Operating Temperature
        op_temp_label = ctk.CTkLabel(input_frame, text="Operating Temperature", text_color="black",
                                     font=ctk.CTkFont(size=16))
        op_temp_label.grid(row=4, column=0, sticky="w", padx=10, pady=7)

        self.op_temp_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="deg C",
            placeholder_text_color="#4F4F4F",
        )
        self.op_temp_input.grid(row=4, column=1, sticky="ew", padx=10, pady=7)

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
            wick_material = self.wick_material_selection.get()
            working_fluid = self.working_fluid_input.get()
            dimensions = self.dimensions_input.get()
            op_temp = self.op_temp_input.get()

            # Pass inputs to calculator to get results
            calculation_results = calculate_heatpipe(
                wick_material=wick_material, working_fluid=working_fluid,
                dimensions=dimensions, op_temp=op_temp
            )

            self.results_label.configure(text=calculation_results)

        except ValueError:
            self.results_label.configure(text="Please enter valid inputs in all fields")

        except Exception as e:
            self.results_label.configure(text=f"An error occurred: {e}")