import customtkinter as ctk
from frames import BaseFrame

class HeatPipeFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "HEAT PIPE")