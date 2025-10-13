import customtkinter as ctk

class MenuFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        # Import images
        self.piping_icon = self.controller.images["piping"]
        self.boiling_icon = self.controller.images["boiling"]
        self.dphx_icon = self.controller.images["dphx"]
        self.plate_icon = self.controller.images["plate"]
        self.shell_icon = self.controller.images["shell"]
        self.heatpipe_icon = self.controller.images["heatpipe"]
        self.settings_icon = self.controller.images["settings"]

        # Create main and header frames
        main_frame = ctk.CTkFrame(self, fg_color="#A9CEFF")
        main_frame.pack(padx=0, pady=0, fill="both", expand=True)

        header_frame = ctk.CTkFrame(main_frame, fg_color="#7CB5FF", corner_radius=0)
        header_frame.pack(ipady=5, padx=0, fill="x")


        # Create settings button and title labels in the header frame
        settings_button = self.create_button(header_frame, self.settings_icon, "", lambda: controller.show_frame("SettingsFrame"))
        settings_button.pack(side="right", padx=10,anchor="e")

        title_label = ctk.CTkLabel(
            header_frame,
            text="THERMAL SOLVER",
            text_color="black",
            font=ctk.CTkFont(size=32)
        )
        title_label.pack(padx=10, pady=8, anchor="w")

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="What are we solving today?",
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        subtitle_label.pack(padx=10, pady=0, anchor="w")

        # Create menu button grid
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20, padx=20, fill="both", expand=True)

        button_frame.grid_rowconfigure((0,1), weight=1)
        button_frame.grid_columnconfigure((0,1,2), weight=1)

        button_data = [
            (self.piping_icon, "Piping", lambda: controller.show_frame("PipingFrame")),
            (self.boiling_icon, "Boiling Condensation", lambda: controller.show_frame("BoilCondFrame")),
            (self.dphx_icon, "Double Pipe HX", lambda: controller.show_frame("DoublePipeFrame")),
            (self.plate_icon, "Plate & Frame HX", lambda: controller.show_frame("PlateFrameFrame")),
            (self.shell_icon, "Shell & Tube HX", lambda: controller.show_frame("ShellTubeFrame")),
            (self.heatpipe_icon, "Heat Pipe", lambda: controller.show_frame("HeatPipeFrame"))
        ]

        for i in range(len(button_data)):
            row = i // 3
            col = i % 3
            button = self.create_button(button_frame, button_data[i][0], button_data[i][1], button_data[i][2])
            button.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)

    def create_button(self, parent, image, text, command):
        button = ctk.CTkButton(
            parent,
            image=image,
            text=text,
            text_color="black",
            font=ctk.CTkFont(size=20),
            fg_color="transparent",
            hover_color="#689CE0",
            compound="top",
            command=command,
        )
        return button