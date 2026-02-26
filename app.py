import customtkinter as ctk
from ui.basic_ui import BasicUI
from ui.scientific_ui import ScientificUI
from ui.temperature_ui import TemperatureUI
from ui.currency_ui import CurrencyUI
from logic.calculator_logic import CalculatorLogic
from logic.temperature_logic import TemperatureLogic
from logic.currency_logic import CurrencyLogic

class App:

    def __init__(self, root):

        self.root = root

        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')
        self.root.configure(bg='#121212')

        self.expression = ''
        self.calculator_logic = CalculatorLogic()
        self.temperature_logic = TemperatureLogic()
        self.currency_logic = CurrencyLogic()

        self.top_frame = ctk.CTkFrame(root, fg_color='#1F1F1F')
        self.top_frame.pack(side='top', fill='x')

        self.selected_mode = ctk.StringVar(value='Basic')

        self.mode_frame = ctk.CTkFrame(root, fg_color='#2E2E2E')
        self.mode_frame.pack(side='top', fill='both', expand=True)

        self.windows = {
            'Basic': BasicUI(
                self.mode_frame,
                self.button_click,
                self.history_click,
                self.history_copy,
                self.history_delete,
                self.history_clear
            ),
            'Scientific': ScientificUI(self.mode_frame),
            'Temperature': TemperatureUI(self.mode_frame),
            'Currency': CurrencyUI(self.mode_frame)
        }

        self.mode_selector = ctk.CTkComboBox(
            self.top_frame,
            values=list(self.windows.keys()),
            variable=self.selected_mode,
            command=self.switch_mode,
            width=200,
            state='readonly',
            fg_color='#2A2A2A',
            button_color='#3A3A3A',
            button_hover_color='#444',
            dropdown_fg_color='#2A2A2A',
            dropdown_text_color='white',
            text_color='white'
        )
        self.mode_selector.pack(pady=10)

        self.mode_selector.bind('<Enter>', lambda e: e.widget.configure(cursor='arrow'))
        self.mode_selector.bind('<Leave>', lambda e: e.widget.configure(cursor='arrow'))

        self.current_window = self.windows['Basic']
        self.current_window.pack(fill='both')
        self.root.geometry(f'{self.current_window.width}x{self.current_window.height}')
        self.root.resizable(False, False)


    def switch_mode(self, window):

        self.current_window.pack_forget()
        self.current_window = self.windows[window]
        self.current_window.pack(fill='both')

        width = self.current_window.width
        height = self.current_window.height
        self.root.geometry(f'{width}x{height}') 

        self.root.resizable(width=False, height=False) 


    def button_click(self, symbol):

        ui = self.current_window
        logic = self.calculator_logic

        if symbol == 'C':
            logic.clear()
        elif symbol == '⌫':
            logic.backspace()
        elif symbol == '=':
            expression, result = logic.calculate()
            if expression:
                ui.add_history_item(expression, result)
        else:
            logic.append(symbol)

        ui.update_typing_display(logic.expression, logic.calculated)

    
    def history_click(self, expression):

        ui = self.current_window
        logic = self.calculator_logic

        logic.expression = expression
        logic.calculated = False

        ui.update_typing_display(expression, logic.calculated) 

    
    def history_copy(self, line):
        self.root.clipboard_clear()
        self.root.clipboard_append(line)


    def history_delete(self, line, outer_frame):

        logic = self.calculator_logic
        
        try:
            logic.history.remove(line)
        except ValueError:
            pass
        
        outer_frame.destroy() 


    def history_clear(self):

        ui = self.current_window
        logic = self.calculator_logic

        ui.clear_history_display()
        logic.clear_history()  