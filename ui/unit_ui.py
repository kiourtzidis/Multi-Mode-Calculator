import customtkinter as ctk

class UnitUI(ctk.CTkFrame):

    def __init__(self, parent, logic):

        super().__init__(parent, fg_color='#292929')
        self.width = 750
        self.height = 390
        self.logic = logic

        self.categories = ('Length', 'Weight', 'Temperature', 'Time', 'Area', 'Speed', 'Volume', 'Energy', 'Data')
        self.current_category = self.categories[0]
        self.category_buttons = {}
        self.reference_labels = []

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_converter()

        self._select_category(self.current_category)


    def _build_sidebar(self):

        self.buttons_frame = ctk.CTkFrame(self, width=180, fg_color='#1F1F1F', corner_radius=0)
        self.buttons_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 2))

        for i, category in enumerate(self.categories):
            button = ctk.CTkButton(
                self.buttons_frame,
                text=category,
                font=('Jetbrains Mono', 16),
                fg_color='#242424',
                hover_color='#2E2E2E',
                border_width=1,
                border_color='#333333',
                command=lambda c=category: self._select_category(c)
            )
            button.grid(row=i, column=0, sticky='ew', padx=5, pady=5)
            button.configure(cursor='hand2')
            self.buttons_frame.grid_rowconfigure(i, weight=1)

            self.category_buttons[category] = button

        self.buttons_frame.grid_columnconfigure(0, weight=1)


    def _build_converter(self):

        self.converter_frame = ctk.CTkFrame(self, fg_color='#292929', corner_radius=0)
        self.converter_frame.grid(row=0, column=1, sticky='nsew')

        self.converter_frame.grid_columnconfigure(0, weight=1)
        self.converter_frame.grid_columnconfigure(1, weight=0)
        self.converter_frame.grid_columnconfigure(2, weight=1)

        self.from_label = ctk.CTkLabel(
            self.converter_frame,
            text='From:',
            font=('Jetbrains Mono', 12),
            text_color='#777777'
        )
        self.from_label.grid(row=0, column=0, sticky='w', padx=8, pady=(3, 0))

        self.from_entry = ctk.CTkEntry(
            self.converter_frame,
            font=('Jetbrains Mono', 20),
            fg_color='#242424',
            border_width=1,
            border_color='#4A4A4A',
            height=44
        )
        self.from_entry.grid(row=1, column=0, sticky='ew', padx=8, pady=(2, 6))
        self.from_entry.bind('<KeyRelease>', self._convert)

        self.from_unit_menu = ctk.CTkOptionMenu(
            self.converter_frame,
            values=[],
            font=('Jetbrains Mono', 14),
            fg_color='#242424',
            button_color='#2E2E2E',
            button_hover_color='#383838',
            text_color='#CCCCCC',
            dropdown_fg_color='#242424',
            dropdown_hover_color='#333333',
            dropdown_text_color='#CCCCCC',
            dynamic_resizing=False,
            command=self._convert
        )
        self.from_unit_menu.grid(row=2, column=0, sticky='ew', padx=8, pady=(0, 10))
        self.from_unit_menu.configure(cursor='hand2')

        self.swap_button = ctk.CTkButton(
            self.converter_frame,
            text='⇄',
            font=('Jetbrains Mono', 20),
            fg_color='#262626',
            hover_color='#3A3A3A',
            text_color='#AAAAAA',
            border_width=1,
            border_color='#3C3C3C',
            width=40,
            command=self._swap_units
        )
        self.swap_button.grid(row=1, column=1, padx=8)
        self.swap_button.configure(cursor='hand2')

        self.to_label = ctk.CTkLabel(
            self.converter_frame,
            text='To:',
            font=('Jetbrains Mono', 12),
            text_color='#777777'
        )
        self.to_label.grid(row=0, column=2, sticky='w', padx=8, pady=(3, 0))

        self.to_entry = ctk.CTkEntry(
            self.converter_frame,
            font=('Jetbrains Mono', 20),
            fg_color='#242424',
            text_color='#999999',
            border_width=0,
            height=44
        )
        self.to_entry.grid(row=1, column=2, sticky='ew', padx=8, pady=(2, 6))
        self.to_entry.configure(state='readonly')

        self.to_unit_menu = ctk.CTkOptionMenu(
            self.converter_frame,
            values=[],
            font=('Jetbrains Mono', 14),
            fg_color='#242424',
            button_color='#2E2E2E',
            button_hover_color='#383838',
            text_color='#CCCCCC',
            dropdown_fg_color='#242424',
            dropdown_hover_color='#333333',
            dropdown_text_color='#CCCCCC',
            dynamic_resizing=False,
            command=self._convert
        )
        self.to_unit_menu.grid(row=2, column=2, sticky='ew', padx=8, pady=(0, 10))
        self.to_unit_menu.configure(cursor='hand2')

        separator = ctk.CTkFrame(self.converter_frame, height=1, fg_color='#333333')
        separator.grid(row=3, column=0, columnspan=3, sticky='ew', pady=(0, 3))

        self.reference_header = ctk.CTkLabel(
                    self.converter_frame,
                    text='Reference Table',
                    font=('Jetbrains Mono', 12),
                    text_color='#777777'
                )
        self.reference_header.grid(row=4, column=0, columnspan=3)

        for i in range(3):
            label = ctk.CTkLabel(
                self.converter_frame,
                text='',
                font=('Jetbrains Mono', 15),
                text_color='#CCCCCC'
            )
            label.grid(row=5 + i, column=0, columnspan=3)
            self.reference_labels.append(label)

        self.converter_frame.grid_rowconfigure(8, weight=0)

        separator = ctk.CTkFrame(self.converter_frame, height=1, fg_color='#333333')
        separator.grid(row=8, column=0, columnspan=3, sticky='ew', pady=3)


    def _select_category(self, category):

        self.current_category = category

        for c, button in self.category_buttons.items():
            button.configure(fg_color='#3C3C3C' if c == category else '#2A2A2A')

        units = self.logic.get_units(category)

        self.from_unit_menu.configure(values=units)
        self.to_unit_menu.configure(values=units)
        self.from_unit_menu.set(units[0])
        self.to_unit_menu.set(units[1])

        self.from_entry.delete(0, 'end')
        self._set_result('')
        self._update_reference_table()


    def _swap_units(self):

        from_unit = self.from_unit_menu.get()
        to_unit = self.to_unit_menu.get()

        self.from_unit_menu.set(to_unit)
        self.to_unit_menu.set(from_unit)

        self.from_entry.delete(0, 'end')
        self.from_entry.insert(0, self.to_entry.get())

        self._convert()


    def _convert(self, _=None):

        text = self.from_entry.get()

        try:
            value = float(text)
        except ValueError:
            self._update_reference_table()
            self._set_result('')
            return

        from_unit = self.from_unit_menu.get()
        to_unit = self.to_unit_menu.get()

        result = self.logic.convert(self.current_category, value, from_unit, to_unit)

        self._set_result('' if result is None else f'{result:.10g}')
        self._update_reference_table()


    def _update_reference_table(self):

        from_unit = self.from_unit_menu.get()
        to_unit = self.to_unit_menu.get()

        for label, factor in zip(self.reference_labels, (1, 10, 100)):
            result = self.logic.convert(self.current_category, factor, from_unit, to_unit)
            if result is None:
                label.configure(text='')
            else:
                label.configure(text=f'{factor} {from_unit}  =  {result:.6g} {to_unit}')


    def _set_result(self, text):
        self.to_entry.configure(state='normal')
        self.to_entry.delete(0, 'end')
        self.to_entry.insert(0, text)
        self.to_entry.configure(state='readonly')