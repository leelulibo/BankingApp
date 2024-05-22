import tkinter as tk
from bank_gui import BankApp
from gui import UserRegistrationApp
from backend import login_user  # Assume this function returns user_id on success
import customtkinter as ctk

def main():
    root = ctk.CTk()
    user_app = UserRegistrationApp(root)

    def on_login_success(user_id):
        root.withdraw()
        bank_root = ctk.CTk()
        bank_app = BankApp(bank_root, user_id)
        bank_root.mainloop()

    user_app.on_login_success = on_login_success
    root.mainloop()

if __name__ == "__main__":
    main()
