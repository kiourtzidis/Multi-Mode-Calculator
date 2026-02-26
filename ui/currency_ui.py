import customtkinter as ctk

class CurrencyUI(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent, fg_color='#2E2E2E')
        self.width = 460
        self.height = 715

        label = ctk.CTkLabel(self, text='Coming soon...', font=('Jetbrains Mono', 24))
        label.pack(expand=True)