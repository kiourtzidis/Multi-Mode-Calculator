import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class GraphUI(ctk.CTkFrame):

    def __init__(self, parent):
        
        super().__init__(parent, fg_color='#1F1F1F')

        self.width = 500
        self.height = 620
        self.toggle_state = False
        self.secondary_buttons = {}

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self._build_canvas()
        self._build_controls()
        self._build_buttons()


    def _build_canvas(self):

        self.canvas_frame = ctk.CTkFrame(self, fg_color='#2E2E2E', width=self.width, height=300)
        self.canvas_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=(8, 4))

        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.ax.set_facecolor('#2E2E2E')
        self.fig.patch.set_facecolor('#2E2E2E')
        self.ax.grid(True, color='#444444')

        self.ax.tick_params(
            colors='#AAAAAA',
            labelsize=8
        )

        self.ax.locator_params(nbins=5)

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        self.ax.spines['bottom'].set_position('zero')
        self.ax.spines['left'].set_position('zero')

        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['bottom'].set_linewidth(1)
        self.ax.spines['left'].set_linewidth(1)

        self.ax.title.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.xaxis.label.set_color('white')

        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    
    def _build_controls(self):
        self.controls_frame = ctk.CTkFrame(self, fg_color='#1F1F1F', height=70)
        self.controls_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=(8, 4))

        self.controls_frame.grid_columnconfigure(0, weight=1)
        self.controls_frame.grid_columnconfigure(1, weight=1)

        self.function_entry = ctk.CTkEntry(
            self.controls_frame, 
            font=('Jetbrains Mono', 16),
            fg_color='#2E2E2E',
            height=40,
            placeholder_text='Enter function…'
        )
        self.function_entry.grid(row=0, column=0, columnspan=3, sticky='nsew', padx=2, pady=10)
        self.function_entry.configure(cursor='xterm')
        self.function_entry.bind('<Return>', lambda e: self.plot_function())

        self.plot_button = ctk.CTkButton(
            self.controls_frame,
            text='Plot',
            font=('Jetbrains Mono', 14),
            fg_color='#2A2A2A',
            hover_color='#323232',
            command=self.plot_function
        )
        self.plot_button.grid(row=1, column=0, sticky='nsew', padx=2, pady=(0, 2))
        self.plot_button.configure(cursor='hand2')

        self.clear_button = ctk.CTkButton(
            self.controls_frame,
            text='Clear',
            font=('Jetbrains Mono', 14),
            fg_color='#2A2A2A',
            hover_color='#323232',
            command=self.clear_functions
        )
        self.clear_button.grid(row=1, column=1, sticky='nsew', padx=2, pady=(0, 2))
        self.clear_button.configure(cursor='hand2')

    def _build_buttons(self):
        self.buttons_frame = ctk.CTkFrame(self, fg_color='#1F1F1F', height=170)
        self.buttons_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=(0, 8))

        graph_buttons = (
            (('C', 'clear'),
             ('.', 'decimal'),
             ('+', 'operator'),
             ('-', 'operator'),
             ('×', 'operator'),
             ('÷', 'operator')),

            ((('sin', 'sin⁻¹'), 'function'),
             (('cos', 'cos⁻¹'), 'function'),
             (('tan', 'tan⁻¹'), 'function'),
             (('sec', 'sec⁻¹'), 'function'),
             (('csc', 'csc⁻¹'), 'function'),
             (('cot', 'cot⁻¹'), 'function')),

            ((('x²', '√'), 'function'),
             (('x³', '∛'), 'function'),
             (('xʸ', '|x|'), 'function'),
             (('log', '10ˣ'), 'function'),
             (('log₂', '2ˣ'), 'function'),
             (('ln', 'eˣ'), 'function')),

            (('(', 'parenthesis'),
             (')', 'parenthesis'),
             ('x', 'variable'),
             ('π', 'constant'),
             ('e', 'constant'),
             ('⇄', 'toggle'))
        )

        self.toggle_state = False
        self.secondary_buttons = {}

        for r, row in enumerate(graph_buttons):
            for c, btn in enumerate(row):

                labels, type = btn

                if isinstance(labels, tuple):
                    text = labels[0]
                else:
                    text = labels

                if type == 'clear':
                        button = ctk.CTkButton(
                            self.buttons_frame,
                            text=text, 
                            font=('Jetbrains Mono', 20), 
                            fg_color='#E07B1A', 
                            hover_color='#FF944D'
                        )
                elif type == 'toggle':
                    button = ctk.CTkButton(
                        self.buttons_frame,
                        text=text, 
                        font=('Jetbrains Mono', 20), 
                        fg_color='#3C3C3C', 
                        hover_color='#4A4A4A', 
                        command=self.toggle_functions
                        )
                else:
                    button = ctk.CTkButton(
                        self.buttons_frame,
                        text=text, 
                        font=('Jetbrains Mono', 20), 
                        fg_color='#262626', 
                        hover_color='#323232'
                        )

                button.grid(row=r, column=c, sticky='nsew', padx=2, pady=2)
                button.configure(cursor='hand2')

                if isinstance(labels, tuple):
                    self.secondary_buttons[button] =  labels

        for r in range(len(graph_buttons)):
            self.buttons_frame.grid_rowconfigure(r, weight=1)
        for c in range(6):
            self.buttons_frame.grid_columnconfigure(c, weight=1)


    def plot_function(self):
        pass


    def clear_functions(self):
        pass


    def toggle_functions(self):

        self.toggle_state = not self.toggle_state
    
        for button, labels in self.secondary_buttons.items():
            new_button = labels[1] if self.toggle_state else labels[0]
            button.configure(text=new_button)