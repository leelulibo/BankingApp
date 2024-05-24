import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from bank_backend import Bank
import customtkinter as ctk
from PIL import Image, ImageTk
from backend import register_user


class BankApp:
    def __init__(self, master, user_id):
        self.master = master
        self.master.geometry("450x520")
        self.master.title("Banking Application")
        self.bank = Bank(user_id, currency='R')
        
        self.deposit_button = ctk.CTkButton(master, text="Deposit", command=self.make_deposit)
        self.deposit_button.pack()

        self.withdrawal_button = ctk.CTkButton(master, text="Withdrawal", command=self.make_withdrawal)
        self.withdrawal_button.pack()

        self.statement_button = ctk.CTkButton(master, text="View Statement", command=self.view_statement)
        self.statement_button.pack()
        
        self.update_details_button = ctk.CTkButton(master, text="Update Details", command=self.update_details)
        self.update_details_button.pack()
        

        self.balance_label = ctk.CTkLabel(master, text=self.bank.display_balance())
        self.balance_label.pack()
        
        
        self.create_transaction_table()
        
    def create_transaction_table(self):
        self.table_frame = ctk.CTkFrame(self.master)
        self.table_frame.pack(pady=20, padx=20)

        headers = ["Date", "Time", "Type", "Balance"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.table_frame, text=header, width=120, height=25, anchor="w")
            label.grid(row=0, column=col, padx=5, pady=5)

        self.populate_transaction_table()

    def populate_transaction_table(self):
        transactions = self.bank.get_transactions()  # Replace with your method to get transactions
        for row, transaction in enumerate(transactions, start=1):
            for col, value in enumerate(transaction):
                label = ctk.CTkLabel(self.table_frame, text=value, width=120, height=25, anchor="w")
                label.grid(row=row, column=col, padx=5, pady=5)

    def make_deposit(self):
        amount = simpledialog.askfloat("Deposit", "How much would you like to deposit?")
        if amount is not None:
            if self.bank.deposit(amount):
                self.update_balance_display()

    def make_withdrawal(self):
        amount = simpledialog.askfloat("Withdrawal", "How much would you like to withdraw?")
        if amount is not None:
            if self.bank.withdraw(amount):
                self.update_balance_display()

    def view_statement(self):
        self.master.withdraw()
        
        statement_window = ctk.CTkToplevel()
        statement_window.title("Statement")
        statement_window.geometry("400x450")
        
        statement_text = scrolledtext.ScrolledText(statement_window, width=40, height=10)
        statement_text.insert(ctk.END, self.bank.display_transaction_log())
        statement_text.pack(fill=ctk.BOTH, expand=True)
        
        email_label = ctk.CTkLabel(statement_window, text="Enter your email address:")
        email_label.pack()
        
        email_entry = ctk.CTkEntry(statement_window)
        email_entry.pack()
        
        send_button = ctk.CTkButton(statement_window, text="Send Statement", command=lambda: self.send_statement_email(email_entry.get(), statement_window))
        send_button.pack()
        
        back_button = ctk.CTkButton(statement_window, text="Back", command=lambda: self.back_to_main(statement_window))
        back_button.pack()

    def send_statement_email(self, email, window):
        if email.strip() == "":
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        try:
            self.bank.send_statement_email(email)
            messagebox.showinfo("Success", "Statement sent successfully!")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {str(e)}")

    def back_to_main(self, statement_window):
        statement_window.destroy()
        self.master.deiconify()

    def update_balance_display(self):
        self.balance_label.configure(text=self.bank.display_balance())
        
    def update_transaction_table(self):
        # Clear the existing table
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        # Re-create the headers
        headers = ["Date", "Time", "Type", "Amount", "Balance"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.table_frame, text=header, width=120, height=25, anchor="w")
            label.grid(row=0, column=col, padx=5, pady=5)
        # Repopulate the table with updated transactions
        self.populate_transaction_table()
        
    def update_details(self):
        update_window = ctk.CTkToplevel()
        update_window.title("Update Personal Details")
        update_window.geometry("300x300")

        # Labels and entry fields for updating personal details
        firstname_label = ctk.CTkLabel(update_window, text="First Name:")
        firstname_label.pack()

        firstname_entry = ctk.CTkEntry(update_window)
        firstname_entry.pack()

        lastname_label = ctk.CTkLabel(update_window, text="Last Name:")
        lastname_label.pack()

        lastname_entry = ctk.CTkEntry(update_window)
        lastname_entry.pack()

        phone_label = ctk.CTkLabel(update_window, text="Phone Number:")
        phone_label.pack()

        phone_entry = ctk.CTkEntry(update_window)
        phone_entry.pack()

        address_label = ctk.CTkLabel(update_window, text="Address:")
        address_label.pack()

        address_entry = ctk.CTkEntry(update_window)
        address_entry.pack()
        
        # Load user details from the backend and pre-fill the entry fields
        firstname_entry.insert(0, self.bank.account_holder_name)
        lastname_entry.insert(0, self.bank.lastname)
        phone_entry.insert(0, self.bank.phone)
        address_entry.insert(0, self.bank.address)

        def update_and_send_email():
            firstname = firstname_entry.get()
            lastname = lastname_entry.get()
            phone = phone_entry.get()
            address = address_entry.get()

            # Update details in the backend
            self.bank.update_user_details(firstname, lastname, phone, address)

            # Send updated details to user's email
            try:
                self.bank.send_update_details_email(firstname, lastname, phone, address)
                messagebox.showinfo("Success", "Details updated and email sent successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send email: {str(e)}")

            # Close the update window after updating
            update_window.destroy()

        submit_button = ctk.CTkButton(update_window, text="Submit", command=update_and_send_email)
        submit_button.pack()    
     
        
