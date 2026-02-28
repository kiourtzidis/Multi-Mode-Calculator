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

        self.clear_history_button = ctk.CTkButton(
            self.history_frame,
            text='Clear History',
            height=28,
            fg_color='#2A2A2A',
            hover_color='#323232',
            font=('Jetbrains Mono', 14)
        )
        self.clear_history_button.grid(row=0, column=0, sticky='nsew', padx=4, pady=(4, 2))
        self.clear_history_button.configure(cursor='hand2')

        self.history_scroll = ctk.CTkScrollableFrame(
            self.history_frame, 
            fg_color='#3C3C3C',
            scrollbar_button_color='#777777',
            scrollbar_button_hover_color='#999999', 
            border_width=0)
        self.history_scroll.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)