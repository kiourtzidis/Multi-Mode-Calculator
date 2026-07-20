import customtkinter as ctk

class UnitUI(ctk.CTkFrame):

    def __init__(self, parent, logic):

        super().__init__(parent, fg_color='#2E2E2E')
        self.width = 460
        self.height = 350
        self.logic = logic

        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self._build_buttons()


    def _build_buttons(self):

        self.buttons_frame = ctk.CTkFrame(self, fg_color='#1F1F1F', width=180)
        self.buttons_frame.grid(row=0, column=0, sticky='nsew', padx=2, pady=(0, 2))

        unit_buttons = ('Length', 'Weight', 'Temperature', 'Time', 'Area', 'Speed', 'Volume', 'Data')

        for i, unit in enumerate(unit_buttons):
            button = ctk.CTkButton(
                self.buttons_frame,
                text=unit,
                font=('Jetbrains Mono', 16),
                fg_color='#2A2A2A',
                hover_color='#323232',
                border_width=1,
                border_color='#3C3C3C',
                #command=lambda u=unit: self.logic.switch_unit(u)
            )
            button.grid(row=i, column=0, sticky='ew', padx=5, pady=5)
            button.configure(cursor='hand2')
            self.buttons_frame.grid_rowconfigure(i, weight=1)

        self.buttons_frame.grid_columnconfigure(0, weight=1)