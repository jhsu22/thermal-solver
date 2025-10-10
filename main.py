import customtkinter as ctk
from PIL import Image

class ThermalSolver(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("Thermal Solver")
        self.geometry("900x550")
        self.resizable(False, False)

        # Import all UI icons
        self.piping_icon = ctk.CTkImage(Image.open("images/piping.png"), size=(64, 64))
        self.boiling_icon = ctk.CTkImage(Image.open("images/boiling.png"), size=(64, 64))
        self.dphx_icon = ctk.CTkImage(Image.open("images/dphx.png"), size=(64, 64))
        self.plate_icon = ctk.CTkImage(Image.open("images/plate.png"), size=(64, 64))
        self.shell_icon = ctk.CTkImage(Image.open("images/shell.png"), size=(64, 64))
        self.heatpipe_icon = ctk.CTkImage(Image.open("images/heatpipe.png"), size=(64, 64))
        self.settings_icon = ctk.CTkImage(Image.open("images/settings.png"), size=(64, 64))

        # Create main and header frames
        main_frame = ctk.CTkFrame(self, fg_color="#A9CEFF")
        main_frame.pack(padx=0, pady=0, fill="both", expand=True)

        header_frame = ctk.CTkFrame(main_frame, fg_color="#7CB5FF", corner_radius=0)
        header_frame.pack(pady=0, padx=0, fill="x")

        # Create settings button and title labels in the header frame
        settings_button = self.create_button(header_frame, self.settings_icon, "")
        settings_button.pack(side="right", anchor="e")

        title_label = ctk.CTkLabel(
            header_frame,
            text="THERMAL SOLVER",
            text_color="black",
            font=ctk.CTkFont(size=32)
        )
        title_label.pack(padx=10, anchor="w")

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="What are we solving today?",
            text_color="black",
            font=ctk.CTkFont(size=18)
        )
        subtitle_label.pack(padx=10, anchor="w")

        # Create menu button grid
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20, padx=20, fill="both", expand=True)

        button_frame.grid_rowconfigure((0,1), weight=1)
        button_frame.grid_columnconfigure((0,1,2), weight=1)

        button_data = [
            [self.piping_icon, "Piping"],
            [self.boiling_icon, "Boiling Condensation"],
            [self.dphx_icon, "Double Pipe HX"],
            [self.plate_icon, "Plate and Frame HX"],
            [self.shell_icon, "Shell and Tube HX"],
            [self.heatpipe_icon, "Heat Pipe"]
        ]

        for i in range(len(button_data)):
            row = i // 3
            col = i % 3
            button = self.create_button(button_frame, button_data[i][0], button_data[i][1])
            button.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)

    def create_button(self, parent, image, text):
        button = ctk.CTkButton(
            parent,
            image=image,
            text=text,
            text_color="black",
            font=ctk.CTkFont(size=20),
            fg_color="transparent",
            hover_color="#689CE0",
            compound="top",
        )
        return button


ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("theme.json")

app = ThermalSolver()
app.mainloop()