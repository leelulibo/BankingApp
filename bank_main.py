import tkinter as tk
from bank_gui import BankApp
import customtkinter as ctk

def main():
    root = ctk.CTk()
    app = BankApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
