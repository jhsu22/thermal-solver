import customtkinter as ctk
from frames import BaseFrame

class DoublePipeFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "DOUBLE PIPE HEAT EXCHANGER")