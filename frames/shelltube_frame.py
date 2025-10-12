import customtkinter as ctk
from frames import BaseFrame

class ShellTubeFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "SHELL & TUBE HEAT EXCHANGER")