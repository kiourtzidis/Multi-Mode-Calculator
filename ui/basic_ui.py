import customtkinter as ctk
from ui.calculator_ui import CalculatorUI

class BasicUI(CalculatorUI):

    def __init__(self, parent, logic):

        super().__init__(parent, logic, width=360, height=615)
        self._build_buttons()

    
    def _build_buttons(self):

        self.buttons_frame = ctk.CTkFrame(self, fg_color='#1F1F1F')
        self.buttons_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=(4,8))
        
        basic_buttons = (
            ('C', 'clear'),
            ('⌫', 'backspace'),
            ('.', 'decimal'),
            ('+', 'operator'),

            ('1', 'number'),
            ('2', 'number'),
            ('3', 'number'),
            ('-', 'operator'),

            ('4', 'number'),
            ('5', 'number'),
            ('6', 'number'),
            ('×', 'operator'),

            ('7', 'number'),
            ('8', 'number'),
            ('9', 'number'),
            ('÷', 'operator'),

            ('0', 'number'),
            ('div', 'operator'),
            ('mod', 'operator'),
            ('=', 'equal')
        )
                                                
        for i, (symbol, type) in enumerate(basic_buttons):

            if type == 'number':
                button = ctk.CTkButton(
                    self.buttons_frame,
                    text=symbol,
                    font=('Jetbrains Mono', 20),
                    fg_color='#3C3C3C',
                    hover_color='#4A4A4A',
                    command=lambda s=symbol: self.handle_symbol(s))
            elif type == 'operator' or type == 'decimal':
                button = ctk.CTkButton(
                    self.buttons_frame,
                    text=symbol, 
                    font=('Jetbrains Mono', 20), 
                    fg_color='#262626', 
                    hover_color='#323232', 
                    command=lambda s=symbol: self.handle_symbol(s))
            elif type == 'backspace':
                button = ctk.CTkButton(
                    self.buttons_frame, 
                    text=symbol, 
                    font=('Jetbrains Mono', 20), 
                    fg_color='#262626', 
                    hover_color='#C42B2B', 
                    command=lambda s=symbol: self.handle_symbol(s))
            else:
                button = ctk.CTkButton(
                    self.buttons_frame, 
                    text=symbol, 
                    font=('Jetbrains Mono', 20), 
                    fg_color='#E07B1A', 
                    hover_color='#FF944D', 
                    command=lambda s=symbol: self.handle_symbol(s))

            button.configure(cursor='hand2')
            button.grid(row=i // 4, column=i % 4 , sticky='nsew', padx=5, pady=5)

        for i in range(5): 
            self.buttons_frame.grid_rowconfigure(i, weight=1) 
        for j in range(4): 
            self.buttons_frame.grid_columnconfigure(j, weight=1) 