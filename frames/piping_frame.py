import customtkinter as ctk
from frames import BaseFrame

class PipingFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller,"PIPING")

        # --- Input Frame using .grid() for clean alignment ---
        # Create a dedicated frame for the input fields
        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        input_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Configure the grid columns. Column 1 will expand to fill space.
        input_frame.grid_columnconfigure(1, weight=1)

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
        length_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="m",
            placeholder_text_color="#4F4F4F",
            text_color="black"
        )
        length_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5) # "ew" = expand east-west

        # Row 2: Material
        material_label = ctk.CTkLabel(input_frame, text="Material", text_color="black", font=ctk.CTkFont(size=16))
        material_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        material_selection = ctk.CTkOptionMenu(
            input_frame,
            values=["Copper Type K", "Copper Type M", "Copper Type L", "Steel"],
            text_color="black",
            font=ctk.CTkFont(size=14),
            dropdown_fg_color="#bfbdbd",
            dropdown_hover_color="#999999",
            dropdown_text_color="black"
        )
        material_selection.grid(row=2, column=1, sticky="w", padx=5, pady=5) # "w" = align west

        # Row 3: Nominal Diameter
        nominal_label = ctk.CTkLabel(input_frame, text="Nominal Diameter", text_color="black", font=ctk.CTkFont(size=16))
        nominal_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        nominal_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter as decimal",
            placeholder_text_color="#4F4F4F",
        )
        nominal_input.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        # Section Title: Fluid Settings
        fluid_label = ctk.CTkLabel(
            input_frame,
            text="FLUID SETTINGS",
            text_color="black",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        fluid_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=(20, 10))