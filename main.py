import customtkinter as ctk
from app import App

def main():

    root = ctk.CTk()
    
    root.title("Multi-Mode Calculator")
    root.geometry("360x615")

    app = App(root)

    root.mainloop()


if __name__ == "__main__":
    main() 