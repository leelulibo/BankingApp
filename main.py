import tkinter as tk
from bank_gui import BankApp
from gui import UserRegistrationApp
from backend import login_user  # Assume this function returns user_id on success
import customtkinter as ctk

def show_login_window():
    root = ctk.CTk()
    user_app = UserRegistrationApp(root)

    def on_login_success(user_id):
        root.withdraw()
        show_bank_app(user_id)

    user_app.on_login_success = on_login_success
    root.mainloop()

def show_bank_app(user_id):
    bank_root = ctk.CTk()
    bank_app = BankApp(bank_root, user_id)

    def on_logout():
        bank_root.destroy()
        show_login_window()

    bank_app.on_logout = on_logout
    bank_root.mainloop()

def main():
    show_login_window()

if __name__ == "__main__":
    main()
