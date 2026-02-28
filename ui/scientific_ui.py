import customtkinter as ctk

class ScientificUI(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent, fg_color='#1F1F1F')

        self.max_history_chars = 15

        self.width = 720
        self.height = 615

        self.grid_rowconfigure(0, weight=5)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.history_frame = ctk.CTkFrame(self, fg_color='#3C3C3C')
        self.history_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=(8, 4))
        self.history_frame.grid_rowconfigure(0, weight=0)
        self.history_frame.grid_rowconfigure(1, weight=1)
        self.history_frame.grid_columnconfigure(0, weight=1)