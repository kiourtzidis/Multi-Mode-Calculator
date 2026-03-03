import customtkinter as ctk

class CalculatorUI(ctk.CTkFrame):
    
    def __init__(self, parent, logic, width, height):
        super().__init__(parent, fg_color='#1F1F1F')

        self.logic = logic
        self.width = width
        self.height = height
        self.max_history_chars = 15

        self.grid_rowconfigure(0, weight=5)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_history()
        self._build_display()

    
    def _build_history(self):

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
            font=('Jetbrains Mono', 14),
            command=self.history_clear
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

    def _build_display(self):

        self.typing_frame = ctk.CTkFrame(self, fg_color='#2E2E2E')
        self.typing_frame.grid(row=1, column=0, sticky='nsew',  padx=10, pady=4)
        self.typing_entry = ctk.CTkEntry(
            self.typing_frame, 
            font=('Jetbrains Mono', 24), 
            fg_color='#2E2E2E',
            height=40,
            state='readonly', 
            border_width=0)
        self.typing_entry.pack(fill='both', padx=10, ipady=10)
        self.typing_entry._entry.configure(cursor='arrow')

    
    def handle_symbol(self, symbol):

        if symbol == 'C':
            self.logic.clear()

        elif symbol == '⌫':
            self.logic.backspace()

        elif symbol == '=':
            expression, result = self.logic.calculate()
            if expression:
                self.add_history_item(expression, result)

        else:
            self.logic.append(symbol)

        self.update_typing_display()


    def update_typing_display(self):

        self.typing_entry.configure(state='normal')
        self.typing_entry.delete(0, 'end')
        self.typing_entry.insert(0, self.logic.expression)

        if self.logic.calculated:
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

        formatted_line = self.format_history_item(line)
        item_label.configure(text=formatted_line)

        copy_button = ctk.CTkButton(
            item_frame,
            text='⧉',
            width=24,
            height=24,
            fg_color='#444444',
            font=('Jetbrains Mono', 14),
            command=lambda l=line: self.history_copy(l)
        )
        copy_button.grid(row=0, column=1, sticky='e', padx=(5, 0))

        delete_button = ctk.CTkButton(
            item_frame,
            text='✕',
            width=24,
            height=24,
            fg_color='#444444',
            font=('Jetbrains Mono', 14),
            command=lambda l=line, f=outer: self.history_delete(l, f)
        )
        delete_button.grid(row=0, column=2, sticky='e', padx=(5, 0))

        item_label.configure(cursor='hand2')
        copy_button.configure(cursor='hand2')
        delete_button.configure(cursor='hand2')

        item_label.bind('<Enter>', lambda e: item_label.configure(text_color='#FFFFFF'))
        item_label.bind('<Leave>', lambda e: item_label.configure(text_color='#BBBBBB'))
        item_label.bind('<Button-1>', lambda e, exp=expression: self.history_click(exp))

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


    def format_history_item(self, line):
        if len(line) > self.max_history_chars:
            return line[:self.max_history_chars - 1] + '…'
        return line


    def history_clear(self):

        for frame in list(self.history_scroll.winfo_children()):
            frame.destroy()

        self.logic.clear_history()


    def history_click(self, expression):

        self.logic.expression = expression
        self.logic.calculated = False
        self.update_typing_display()


    def history_copy(self, line):
        self.clipboard_clear()
        self.clipboard_append(line)


    def history_delete(self, line, outer_frame):
        
        try:
            self.logic.history.remove(line)
        except ValueError:
            pass
        
        outer_frame.destroy()