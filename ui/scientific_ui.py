import customtkinter as ctk
from ui.calculator_ui import CalculatorUI

class ScientificUI(CalculatorUI):

    def __init__(self, parent, logic):

        super().__init__(parent, logic, width=620, height=615, max_history_chars=60)

        self.toggle_state = False
        self.secondary_buttons = {}

        self._build_angle_switch()
        self._build_buttons()


    def _build_angle_switch(self):

        self.angle_switch = ctk.CTkButton(
            self.typing_frame,
            text='DEG',
            width=60,
            fg_color='#262626',
            hover_color='#3A3A3A',
            font=('Jetbrains Mono', 24),
            command=self.toggle_angle
        )
        self.angle_switch.pack(side='right', fill='x', padx=10, pady=10)
        self.angle_switch.configure(cursor='hand2')    


    def _build_buttons(self):
        
        self.buttons_frame = ctk.CTkFrame(self, fg_color='#1F1F1F')
        self.buttons_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=(4,8))

        self.buttons_frame.grid_rowconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(0, weight=1, uniform='group1')
        self.buttons_frame.grid_columnconfigure(1, weight=1, uniform='group1')

        self.basic_frame = ctk.CTkFrame(self.buttons_frame, fg_color='#1F1F1F')
        self.basic_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))

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
                    self.basic_frame,
                    text=symbol,
                    font=('Jetbrains Mono', 20),
                    fg_color='#3C3C3C',
                    hover_color='#4A4A4A',
                    command=lambda s=symbol: self.handle_symbol(s))
            elif type == 'operator' or type == 'decimal':
                button = ctk.CTkButton(
                    self.basic_frame,
                    text=symbol, 
                    font=('Jetbrains Mono', 20), 
                    fg_color='#262626', 
                    hover_color='#323232', 
                    command=lambda s=symbol: self.handle_symbol(s))
            elif type == 'backspace':
                button = ctk.CTkButton(
                    self.basic_frame, 
                    text=symbol, 
                    font=('Jetbrains Mono', 20), 
                    fg_color='#262626', 
                    hover_color='#C42B2B', 
                    command=lambda s=symbol: self.handle_symbol(s))
            else:
                button = ctk.CTkButton(
                    self.basic_frame, 
                    text=symbol, 
                    font=('Jetbrains Mono', 20), 
                    fg_color='#E07B1A', 
                    hover_color='#FF944D', 
                    command=lambda s=symbol: self.handle_symbol(s))

            button.configure(cursor='hand2')
            button.grid(row=i // 4, column=i % 4, sticky='nsew', padx=5, pady=5)

        for i in range(5): 
            self.basic_frame.grid_rowconfigure(i, weight=1) 
        for j in range(4): 
            self.basic_frame.grid_columnconfigure(j, weight=1)

        self.scientific_frame = ctk.CTkFrame(self.buttons_frame, fg_color='#1F1F1F')
        self.scientific_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 0))

        scientific_buttons = (
        (('(', 'parenthesis'),
         (')', 'parenthesis'),
         ('!', 'function')),

        ((('sin', 'arcsin'), 'function'),
         (('cos', 'arccos'), 'function'),
         (('tan', 'arctan'), 'function')),

        ((('log', 'log₂'), 'function'),
         (('ln', 'eˣ'), 'function'),
         (('|x|', '±'), 'function')),

        ((('x²', '√'), 'function'),
         (('x³', '∛'), 'function'),
         (('xʸ', 'ⁿ√'), 'function')),

        (('π', 'constant'),
         ('e', 'constant'),
         ('⇄', 'toggle'))
        )

        self.toggle_state = False
        self.secondary_buttons = {}

        for r, row in enumerate(scientific_buttons):
            for c, btn in enumerate(row):

                labels, type = btn

                if isinstance(labels, tuple):
                    text = labels[0]
                else:
                    text = labels
    
                button = ctk.CTkButton(
                    self.scientific_frame,
                    text=text,
                    font=('JetBrains Mono', 20),
                    fg_color='#262626' if text != '⇄' else '#3C3C3C',
                    hover_color='#323232' if text != '⇄' else '#4A4A4A',
                    command=lambda l=labels: self._scientific_click(l)
                )
                button.configure(cursor='hand2')
                button.grid(row=r, column=c, sticky='nsew', padx=5, pady=5)

                if isinstance(labels, tuple):
                    self.secondary_buttons[button] =  labels


        for r in range(len(scientific_buttons)):
            self.scientific_frame.grid_rowconfigure(r, weight=1)
        for c in range(4):
            self.scientific_frame.grid_columnconfigure(c, weight=1)


    def _scientific_click(self, labels):

        if labels == '⇄':
            self.toggle_functions()
            return

        if isinstance(labels, tuple):
            symbol = labels[1] if self.toggle_state else labels[0]
        else:
            symbol = labels

        self.handle_symbol(symbol)


    def toggle_angle(self):

        self.logic.toggle_angle_mode()

        if self.logic.angle_mode == 'DEG':
            self.angle_switch.configure(text='DEG')
        else:
            self.angle_switch.configure(text='RAD')


    def toggle_functions(self):

        self.toggle_state = not self.toggle_state
    
        for button, labels in self.secondary_buttons.items():
            new_text = labels[1] if self.toggle_state else labels[0]
            button.configure(text=new_text)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    