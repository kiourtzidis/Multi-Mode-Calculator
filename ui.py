import customtkinter as ctk

class BasicUI(ctk.CTkFrame):

    def __init__(self, parent, button_callback, history_callback, history_copy_callback, history_delete_callback, history_clear_callback):

        super().__init__(parent, fg_color='#1F1F1F')

        self.width = 360
        self.height = 615

        self.button_callback = button_callback
        self.history_callback = history_callback
        self.history_copy_callback = history_copy_callback 
        self.history_delete_callback = history_delete_callback
        self.history_clear_callback = history_clear_callback

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
            fg_color='#262626',
            hover_color='#323232',
            font=('Jetbrains Mono', 14),
            command=self.history_clear_callback
        )
        self.clear_history_button.grid(row=0, column=0, sticky='nsew', padx=4, pady=(4, 2))
        self.clear_history_button.configure(cursor='hand2')

        self.history_scroll = ctk.CTkScrollableFrame(self.history_frame, fg_color='#3C3C3C')
        self.history_scroll.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        self.typing_frame = ctk.CTkFrame(self, fg_color='#2E2E2E')
        self.typing_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=4)
        self.typing_entry = ctk.CTkEntry(
            self.typing_frame, 
            font=('Jetbrains Mono', 34), 
            fg_color='#2E2E2E', 
            height=40, 
            state='readonly', 
            border_width=0)
        self.typing_entry.pack(fill='both', padx=10, ipady=10)
        self.typing_entry._entry.configure(cursor='arrow')

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
                    hover_color='#C42B2B', 
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

        outer = ctk.CTkFrame(self.history_scroll, fg_color='#444444')
        outer.pack(fill='x', pady=(4, 2))

        item_frame = ctk.CTkFrame(outer, fg_color='#444444')
        item_frame.pack(fill='x', pady=1)
        item_frame.grid_rowconfigure(0, weight=1)
        item_frame.grid_columnconfigure(0, weight=1)
        item_frame.grid_columnconfigure(1, weight=0)
        item_frame.grid_columnconfigure(2, weight=0)

        item_label = ctk.CTkLabel(
                item_frame,
                text=line,
                anchor='w',
                justify='left',
                fg_color='#444444',
                text_color='#BFBFBF',
                font=ctk.CTkFont(size=24)
            )
        item_label.grid(row=0, column=0, sticky='nsew', padx=(5, 0), pady=(1, 0))

        copy_button = ctk.CTkButton(
            item_frame,
            text='⧉',
            width=24,
            height=24,
            fg_color='#444444',
            font=('Jetbrains Mono', 14),
            command=lambda l=line: self.history_copy_callback(l)
        )
        copy_button.grid(row=0, column=1, sticky='e', padx=(5, 0))

        delete_button = ctk.CTkButton(
            item_frame,
            text='✕',
            width=24,
            height=24,
            fg_color='#444444',
            font=('Jetbrains Mono', 14),
            command=lambda l=line, f=outer: self.history_delete_callback(l, f)
        )
        delete_button.grid(row=0, column=2, sticky='e', padx=(10, 5), pady=(1, 0))

        item_label.configure(cursor='hand2')
        copy_button.configure(cursor='hand2')
        delete_button.configure(cursor='hand2')

        item_label.bind('<Enter>', lambda e: item_label.configure(text_color='#FFFFFF'))
        item_label.bind('<Leave>', lambda e: item_label.configure(text_color='#BBBBBB'))
        item_label.bind('<Button-1>', lambda e, exp=expression: self.history_callback(exp))

        copy_button.bind('<Enter>', lambda e: copy_button.configure(text_color='#FFFFFF'))
        copy_button.bind('<Leave>', lambda e: copy_button.configure(text_color='#BBBBBB'))

        delete_button.bind('<Enter>', lambda e: delete_button.configure(text_color='#FFFFFF'))
        delete_button.bind('<Leave>', lambda e: delete_button.configure(text_color='#BBBBBB'))
        
        separator = ctk.CTkFrame(outer, height=1, fg_color='#555555')
        separator.pack(fill='x', pady=(0, 6))

        def scroll_to_bottom():
            canvas = self.history_scroll._parent_canvas
            canvas.update_idletasks()
            canvas.yview_moveto(1.0)

        self.history_scroll.after(0, scroll_to_bottom) 


    def clear_history_display(self):
        for frame in list(self.history_scroll.winfo_children()):
            frame.destroy()

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