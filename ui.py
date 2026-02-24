import customtkinter as ctk

class BasicUI(ctk.CTkFrame):

    def __init__(self, parent, button_callback, history_callback):

        super().__init__(parent, fg_color='#1F1F1F')

        self.width = 360
        self.height = 615

        self.button_callback = button_callback
        self.history_callback = history_callback

        self.grid_rowconfigure(0, weight=5)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.history_frame = ctk.CTkFrame(self, fg_color='#3C3C3C')
        self.history_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=(8, 4))
        self.history_frame.grid_rowconfigure(0, weight=1)
        self.history_frame.grid_columnconfigure(0, weight=1)

        self.history_scroll = ctk.CTkScrollableFrame(self.history_frame, fg_color='#3C3C3C')
        self.history_scroll.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        self.typing_frame = ctk.CTkFrame(self, fg_color='#2E2E2E')
        self.typing_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=4)
        self.typing_entry = ctk.CTkEntry(self.typing_frame, font=('Jetbrains Mono', 34), fg_color='#2E2E2E', height=40, state='readonly', justify='left', border_width=0)
        self.typing_entry.pack(fill='both', padx=10, ipady=10)

        self.buttons_frame = ctk.CTkFrame(self, fg_color='#1F1F1F')
        self.buttons_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=(4,8))
        
        buttons = (
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
                                                
        for i, (symbol, type) in enumerate(buttons):
            row = i // 4
            column = i % 4

            if type == 'number':
                button = ctk.CTkButton(
                    self.buttons_frame,
                    text=symbol,
                    font=('Jetbrains Mono', 20),
                    fg_color='#3C3C3C',
                    hover_color='#4A4A4A',
                    command=lambda s=symbol: self.button_callback(s))
            elif type == 'operator' or type == 'decimal':
                button = ctk.CTkButton(
                    self.buttons_frame,
                    text=symbol, 
                    font=('Jetbrains Mono', 20), 
                    fg_color='#262626', 
                    hover_color='#323232', 
                    command=lambda s=symbol: self.button_callback(s))
            elif type == 'backspace':
                button = ctk.CTkButton(
                    self.buttons_frame, 
                    text=symbol, 
                    font=('Jetbrains Mono', 20), 
                    fg_color='#262626', 
                    hover_color="#C42B2B", 
                    command=lambda s=symbol: self.button_callback(s))
            else:
                button = ctk.CTkButton(
                    self.buttons_frame, 
                    text=symbol, 
                    font=('Jetbrains Mono', 20), 
                    fg_color='#E07B1A', 
                    hover_color='#FF944D', 
                    command=lambda s=symbol: self.button_callback(s))

            button.configure(cursor='hand2')
            button.grid(row=row, column=column, sticky='nsew', padx=5, pady=5)

        for i in range(5): 
            self.buttons_frame.grid_rowconfigure(i, weight=1) 
        for j in range(4): 
            self.buttons_frame.grid_columnconfigure(j, weight=1)


    def update_typing_display(self, text, calculated):

        self.typing_entry.configure(state='normal')
        self.typing_entry.delete(0, 'end')
        self.typing_entry.insert(0, text)

        if calculated:
            self.typing_entry.configure(font=ctk.CTkFont(size=24, weight='bold'))
        else:
            self.typing_entry.configure(font=ctk.CTkFont(size=24))

        self.typing_entry.configure(state='readonly')


    def add_history_item(self, expression, result):
        
        line = f'{expression} = {result}'

        item_label = ctk.CTkLabel(
                self.history_scroll,
                text=line,
                anchor='w',
                fg_color='#444444',
                text_color='#BFBFBF',
                font=ctk.CTkFont(size=20)
            )
        item_label.pack(fill='x', pady=(4, 2))

        item_label.configure(cursor='hand2')

        item_label.bind('<Enter>', lambda e: item_label.configure(text_color='#FFFFFF'))
        item_label.bind('<Leave>', lambda e: item_label.configure(text_color='#BBBBBB'))
        item_label.bind('<Button-1>', lambda e, exp=expression: self.history_callback(exp))

        separator = ctk.CTkFrame(self.history_scroll, height=1, fg_color='#555555')
        separator.pack(fill='x', pady=(0, 6))

        def scroll_to_bottom():
            canvas = self.history_scroll._parent_canvas
            canvas.update_idletasks()
            canvas.yview_moveto(1.0)

        self.history_scroll.after(0, scroll_to_bottom)

class ScientificUI(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent, fg_color='#2E2E2E')
        self.width = 720
        self.height = 615

        label = ctk.CTkLabel(self, text='Coming soon...', font=('Jetbrains Mono', 24))
        label.pack(expand=True)


class TemperatureUI(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent, fg_color='#2E2E2E')
        self.width = 460
        self.height = 715

        label = ctk.CTkLabel(self, text='Coming soon...', font=('Jetbrains Mono', 24))
        label.pack(expand=True)


class CurrencyUI(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent, fg_color='#2E2E2E')
        self.width = 460
        self.height = 715

        label = ctk.CTkLabel(self, text='Coming soon...', font=('Jetbrains Mono', 24))
        label.pack(expand=True)