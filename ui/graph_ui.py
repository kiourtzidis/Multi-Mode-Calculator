import customtkinter as ctk

class GraphUI(ctk.CTkFrame):

    def __init__(self, parent):
        
        super().__init__(parent, fg_color='#1F1F1F')

        self.width = 500
        self.height = 620

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

    
    def _build_controls(self):
        self.controls_frame = ctk.CTkFrame(self, fg_color='#2E2E2E', height=70)
        self.controls_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=(8, 4))


    def _build_buttons(self):
        self.buttons_frame = ctk.CTkFrame(self, fg_color='#1F1F1F', height=165)
        self.buttons_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)