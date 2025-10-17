import customtkinter as ctk
from frames import BaseFrame
from solvers.boilcond_solver import calculate_boilcond


class BoilCondFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "BOILING & CONDENSATION")

        self.input_widgets = {}
        self.current_problem = None

        # --- Main Input Frame ---
        self.input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.input_frame.pack(pady=10, padx=20, fill="both", expand=True)
        # Configure the main frame for 4 columns to center content
        self.input_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="group1")

        # --- Problem Type Selection ---
        problem_type_label = ctk.CTkLabel(self.input_frame, text="Problem Type", text_color="black",
                                          font=ctk.CTkFont(size=18, weight="bold"))
        problem_type_label.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        self.problem_type_selection = ctk.CTkOptionMenu(
            self.input_frame,
            values=[
                "Vertical Plate (L & W)",
                "Vertical Plate (H)",
                "Horizontal Tube (OD)",
                "Horizontal Tube (OD & ID)",
                "Circular Heating Element"
            ],
            command=self.show_inputs_for_problem
        )
        self.problem_type_selection.grid(row=1, column=0, columnspan=4, sticky="ew", padx=5, pady=7)

        # --- Dynamic Input Fields Frame ---
        self.dynamic_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.dynamic_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=(10, 0))
        # Configure the dynamic frame for 4 columns as well
        self.dynamic_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="group1")

        # --- Calculate Button and Results ---
        calculate_button = ctk.CTkButton(
            self.input_frame, text="Calculate!", text_color="black", font=ctk.CTkFont(size=16),
            fg_color="#689CE0", hover_color="#5480BA", height=45, width=150, command=self.calculate
        )
        calculate_button.grid(row=3, column=0, columnspan=4, pady=40)

        self.results_label = ctk.CTkLabel(self.input_frame, text="", text_color="black", font=ctk.CTkFont(size=16),
                                          justify="left")
        self.results_label.grid(row=4, column=0, columnspan=4)

        # Initialize with the first problem's inputs
        self.show_inputs_for_problem(self.problem_type_selection.get())

    def update_placeholders(self):
        # This will now just re-trigger the input creation
        self.show_inputs_for_problem(self.problem_type_selection.get(), force_update=True)

    def create_input_field(self, parent, label_text, placeholder, row, col):
        """Helper function to create a label and an entry widget."""
        # col determines if it's the left (0) or right (1) pair of columns
        label_col = col * 2
        entry_col = col * 2 + 1

        label = ctk.CTkLabel(parent, text=label_text, text_color="black", font=ctk.CTkFont(size=16))
        label.grid(row=row, column=label_col, sticky="w", padx=5, pady=7)
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, placeholder_text_color="#4F4F4F")
        entry.grid(row=row, column=entry_col, sticky="ew", padx=5, pady=7)
        return label, entry

    def show_inputs_for_problem(self, problem_name, force_update=False):
        """Clears and shows the correct input widgets for the selected problem."""
        if self.current_problem == problem_name and not force_update:
            return  # No change needed
        self.current_problem = problem_name

        # Clear previous widgets
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()
        self.input_widgets.clear()

        # Define inputs for each problem type: (label, {si_placeholder, imperial_placeholder}, row, column_pair)
        si_placeholders = {
            "Vertical Plate (L & W)": [
                ("Surface Temp", "°C", 0, 0), ("Saturated Temp", "°C", 1, 0),
                ("Length", "m", 0, 1), ("Width", "m", 1, 1),
                ("Latent Heat", "kJ/kg", 2, 0)
            ],
            "Vertical Plate (H)": [
                ("Surface Temp", "°C", 0, 0), ("Height", "m", 1, 0),
                ("Pressure", "Pa", 0, 1)
            ],
            "Horizontal Tube (OD)": [
                ("Surface Temp", "°C", 0, 0), ("Outer Diameter", "m", 1, 0),
                ("Pressure", "Pa", 0, 1)
            ],
            "Horizontal Tube (OD & ID)": [
                ("Mean Water Temp", "°C", 0, 0), ("Outer Diameter", "m", 1, 0),
                ("Inner Diameter", "m", 2, 0), ("Outside Convection Coeff", "W/m²K", 0, 1),
                ("Inside Convection Coeff", "W/m²K", 1, 1), ("Pressure", "Pa", 2, 1)
            ],
            "Circular Heating Element": [
                ("Surface Temp", "°C", 0, 0), ("Diameter", "m", 1, 0),
                ("Pressure", "atm", 0, 1)
            ]
        }
        imperial_placeholders = {
            "Vertical Plate (L & W)": [
                ("Surface Temp", "°F", 0, 0), ("Saturated Temp", "°F", 1, 0),
                ("Length", "ft", 0, 1), ("Width", "ft", 1, 1),
                ("Latent Heat", "Btu/lbm", 2, 0)
            ],
            "Vertical Plate (H)": [
                ("Surface Temp", "°F", 0, 0), ("Height", "ft", 1, 0),
                ("Pressure", "psi", 0, 1)
            ],
            "Horizontal Tube (OD)": [
                ("Surface Temp", "°F", 0, 0), ("Outer Diameter", "ft", 1, 0),
                ("Pressure", "psi", 0, 1)
            ],
            "Horizontal Tube (OD & ID)": [
                ("Mean Water Temp", "°F", 0, 0), ("Outer Diameter", "ft", 1, 0),
                ("Inner Diameter", "ft", 2, 0), ("Outside Convection Coeff", "Btu/hr·ft²·°F", 0, 1),
                ("Inside Convection Coeff", "Btu/hr·ft²·°F", 1, 1), ("Pressure", "psi", 2, 1)
            ],
            "Circular Heating Element": [
                ("Surface Temp", "°F", 0, 0), ("Diameter", "ft", 1, 0),
                ("Pressure", "atm", 0, 1)
            ]
        }


        # Create and store widgets for the selected problem
        problem_inputs = imperial_placeholders if self.controller.unit_system == "Imperial" else si_placeholders
        inputs = problem_inputs.get(problem_name, [])
        for label_text, placeholder, row, col_pair in inputs:
            label, entry = self.create_input_field(self.dynamic_frame, label_text, placeholder, row, col_pair)
            self.input_widgets[label_text.replace(" ", "_").lower()] = entry

    def calculate(self):
        try:
            problem_type = self.problem_type_selection.get()
            # Get values from the currently visible input widgets
            inputs = {key: widget.get() for key, widget in self.input_widgets.items()}

            # Pass to the solver
            results = calculate_boilcond(problem_type, inputs)

            # Format and display results
            results_text = "\n".join([f"{key.replace('_', ' ').title()}: {value}" for key, value in results.items()])
            self.results_label.configure(text=results_text)

        except ValueError:
            self.results_label.configure(text="Please enter valid numbers in all fields.")
        except Exception as e:
            self.results_label.configure(text=f"An error occurred: {e}")