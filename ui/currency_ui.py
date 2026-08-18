import customtkinter as ctk

CURRENCY_FLAGS = {
    'USD': '🇺🇸', 'EUR': '🇪🇺', 'GBP': '🇬🇧', 'JPY': '🇯🇵', 'CAD': '🇨🇦',
    'AUD': '🇦🇺', 'CHF': '🇨🇭', 'CNY': '🇨🇳', 'INR': '🇮🇳', 'BRL': '🇧🇷',
    'MXN': '🇲🇽', 'KRW': '🇰🇷', 'SGD': '🇸🇬', 'NZD': '🇳🇿', 'SEK': '🇸🇪',
    'NOK': '🇳🇴', 'DKK': '🇩🇰', 'ZAR': '🇿🇦', 'HKD': '🇭🇰', 'TRY': '🇹🇷',
    'PLN': '🇵🇱', 'THB': '🇹🇭', 'IDR': '🇮🇩', 'AED': '🇦🇪', 'SAR': '🇸🇦',
}

REFERENCE_CURRENCIES = ('USD', 'EUR', 'GBP', 'JPY')

class CurrencyUI(ctk.CTkFrame):

    def __init__(self, parent, logic):

        super().__init__(parent, fg_color='#2E2E2E')
        self.width = 595
        self.height = 470
        self.logic = logic

        self.reference_labels = []
        self.shortcut_buttons = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_panel()


    def _build_panel(self):

        self.panel_frame = ctk.CTkFrame(
            self,
            fg_color='#292929',
            corner_radius=0
        )
        self.panel_frame.grid(row=0, column=0, sticky='nsew')

        self.panel_frame.grid_columnconfigure(0, weight=1)
        self.panel_frame.grid_rowconfigure(0, weight=0)
        self.panel_frame.grid_rowconfigure(1, weight=0)
        self.panel_frame.grid_rowconfigure(2, weight=0)
        self.panel_frame.grid_rowconfigure(3, weight=0)
        self.panel_frame.grid_rowconfigure(4, weight=0)
        self.panel_frame.grid_rowconfigure(5, weight=0)
        self.panel_frame.grid_rowconfigure(6, weight=1)

        self.entry_frame = ctk.CTkFrame(self.panel_frame, fg_color='#292929', corner_radius=0)
        self.entry_frame.grid(row=0, column=0, sticky='nsew')

        self.entry_frame.grid_columnconfigure(0, weight=1)
        self.entry_frame.grid_columnconfigure(1, weight=0)
        self.entry_frame.grid_columnconfigure(2, weight=1)

        self.from_label = ctk.CTkLabel(
            self.entry_frame, text='From:', font=('Jetbrains Mono', 12), text_color='#777777'
        )
        self.from_label.grid(row=0, column=0, sticky='w', padx=8, pady=(3, 0))

        self.from_entry = ctk.CTkEntry(
            self.entry_frame,
            font=('Jetbrains Mono', 20),
            fg_color='#242424',
            border_width=1,
            border_color='#4A4A4A',
            height=44
        )
        self.from_entry.grid(row=1, column=0, sticky='ew', padx=8, pady=(2, 6))
        #self.from_entry.bind('<KeyRelease>', self._convert)

        self.from_currency_menu = ctk.CTkOptionMenu(
            self.entry_frame,
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
            #command=self._convert
        )
        self.from_currency_menu.grid(row=2, column=0, sticky='ew', padx=8, pady=(0, 10))
        self.from_currency_menu.configure(cursor='hand2')

        self.swap_button = ctk.CTkButton(
            self.entry_frame,
            text='⇄',
            font=('Jetbrains Mono', 20),
            fg_color='#262626',
            hover_color='#3A3A3A',
            text_color='#AAAAAA',
            border_width=1,
            border_color='#333333',
            width=40,
            #command=self._swap_currencies
        )
        self.swap_button.grid(row=1, column=1, padx=8)
        self.swap_button.configure(cursor='hand2')

        self.to_label = ctk.CTkLabel(
            self.entry_frame, text='To:', font=('Jetbrains Mono', 12), text_color='#777777'
        )
        self.to_label.grid(row=0, column=2, sticky='w', padx=8, pady=(3, 0))

        self.to_entry = ctk.CTkEntry(
            self.entry_frame,
            font=('Jetbrains Mono', 20),
            fg_color='#242424',
            text_color='#999999',
            border_width=0,
            height=44
        )
        self.to_entry.grid(row=1, column=2, sticky='ew', padx=8, pady=(2, 6))
        self.to_entry.configure(state='readonly')

        self.to_currency_menu = ctk.CTkOptionMenu(
            self.entry_frame,
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
            #command=self._convert
        )
        self.to_currency_menu.grid(row=2, column=2, sticky='ew', padx=8, pady=(0, 10))
        self.to_currency_menu.configure(cursor='hand2')

        separator_1 = ctk.CTkFrame(self.panel_frame, height=1, fg_color='#333333')
        separator_1.grid(row=1, column=0, sticky='ew', pady=3)

        self.status_frame = ctk.CTkFrame(self.panel_frame, fg_color='#292929', corner_radius=0)
        self.status_frame.grid(row=2, column=0, sticky='nsew')

        self.status_frame.grid_columnconfigure(0, weight=1)
        self.status_frame.grid_columnconfigure(1, weight=0)

        self.refresh_button = ctk.CTkButton(
            self.status_frame,
            text='↻',
            font=('Jetbrains Mono', 14),
            fg_color='#242424',
            hover_color='#2E2E2E',
            text_color='#AAAAAA',
            border_width=1,
            border_color='#333333',
            width=28,
            height=28,
            #command=self._handle_refresh
        )
        self.refresh_button.grid(row=0, column=0, sticky='w', padx=8)
        self.refresh_button.configure(cursor='hand2')

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text='',
            font=('Jetbrains Mono', 11),
            text_color='#CCCCCC'
        )
        self.status_label.grid(row=0, column=1, sticky='w', padx=8)

        separator_2 = ctk.CTkFrame(self.panel_frame, height=1, fg_color='#333333')
        separator_2.grid(row=3, column=0, sticky='ew', pady=3)

        self.reference_frame = ctk.CTkFrame(self.panel_frame, fg_color='#292929', corner_radius=0)
        self.reference_frame.grid(row=4, column=0, sticky='nsew')

        self.reference_frame.grid_columnconfigure(0, weight=1)

        self.reference_header = ctk.CTkLabel(
            self.reference_frame, text='Reference Table', font=('Jetbrains Mono', 12), text_color='#777777'
        )
        self.reference_header.grid(row=0, column=0, pady=(0, 3))

        for i in range(len(REFERENCE_CURRENCIES)):
            label = ctk.CTkLabel(
                self.reference_frame, text='', font=('Jetbrains Mono', 14), text_color='#CCCCCC'
            )
            label.grid(row=1 + i, column=0)
            self.reference_labels.append(label)

        separator_3 = ctk.CTkFrame(self.panel_frame, height=1, fg_color='#333333')
        separator_3.grid(row=5, column=0, sticky='ew', pady=3)

        self.shortcuts_frame = ctk.CTkFrame(self.panel_frame, fg_color='#292929', corner_radius=0)
        self.shortcuts_frame.grid(row=6, column=0, sticky='nsew')

        self.shortcuts_frame.grid_columnconfigure(0, weight=1)
        self.shortcuts_frame.grid_rowconfigure(1, weight=1)

        self.shortcuts_header = ctk.CTkLabel(
            self.shortcuts_frame, text='Common Conversions', font=('Jetbrains Mono', 12), text_color='#777777'
        )
        self.shortcuts_header.grid(row=0, column=0, pady=3)

        self.shortcuts_grid = ctk.CTkFrame(self.shortcuts_frame, fg_color='#292929', corner_radius=0)
        self.shortcuts_grid.grid(row=1, column=0, sticky='nsew', padx=8, pady=2)

        for col in range(3):
            self.shortcuts_grid.grid_columnconfigure(col, weight=1)
        for row in range(2):
            self.shortcuts_grid.grid_rowconfigure(row, weight=1)

        for i in range(6):
            button = ctk.CTkButton(
                self.shortcuts_grid,
                text='',
                font=('Jetbrains Mono', 14),
                fg_color='#242424',
                hover_color='#2E2E2E',
                text_color='#CCCCCC',
                border_width=1,
                border_color='#333333',
                #command=lambda i=i: self._apply_shortcut(i)
            )
            button.grid(row=i // 3, column=i % 3, sticky='ew', padx=5, pady=3)
            button.configure(cursor='hand2')
            self.shortcut_buttons.append(button)