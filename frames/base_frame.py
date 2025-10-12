import customtkinter as ctk

class BaseFrame(ctk.CTkFrame):

    """
    Base frame class that every window can inherit from
    Contains standard layout and header elements
    """

    def __init__(self, parent, controller, subtitle_text):
        super().__init__(parent)
        self.controller = controller

        # Main and header frames
        main_frame = ctk.CTkFrame(self, fg_color="#A9CEFF")
        main_frame.pack(fill="both", expand=True)

        header_frame = ctk.CTkFrame(main_frame, fg_color="#7CB5FF", corner_radius=0)
        header_frame.pack(ipady=5, fill="x", side="top")

        # Standard back button
        back_button = ctk.CTkButton(
            header_frame,
            text="← Back to Menu",
            text_color="black",
            font=ctk.CTkFont(size=14),
            fg_color="#689CE0",
            hover_color="#5480BA",
            height=45,
            width=150,
            command=lambda: controller.show_frame(MenuFrame)
        )
        back_button.pack(side="right", anchor="e", padx=10)

        # Title and changeable subtitle text
        title_label = ctk.CTkLabel(
            header_frame,
            text="THERMAL SOLVER",
            text_color="black",
            font=ctk.CTkFont(size=32)
        )
        title_label.pack(padx=10, pady=8, anchor="w")

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text=subtitle_text,
            text_color="black",
            font=ctk.CTkFont(size=16)
        )
        subtitle_label.pack(padx=10, anchor="w")

        # Container for child classes to add to
        self.content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.content_frame.pack(pady=15, padx=15, fill="both", expand=True)