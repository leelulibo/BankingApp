import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime

class Bank:
    def __init__(self):
        self.load_bank_data()
        self.load_transaction_log()

    def load_bank_data(self):
        try:
            with open('BankData.txt', 'r') as file:
                self.balance = float(file.readline())
        except FileNotFoundError:
            self.balance = 0

    def save_bank_data(self):
        with open('BankData.txt', 'w') as file:
            file.write(str(self.balance))

    def load_transaction_log(self):
        try:
            with open('TransactionLog.txt', 'r') as file:
                self.transaction_log = file.readlines()
        except FileNotFoundError:
            self.transaction_log = []

    def save_transaction_log(self, transaction):
        with open('TransactionLog.txt', 'a') as file:
            file.write(transaction)

    def deposit(self, amount):
        try:
            self.amount = float(amount)
            if self.amount <= 0:
                raise ValueError("Invalid input: Please enter a valid amount.")
            self.balance += self.amount
            self.transaction_type = "Deposit"
            self.save_bank_data()
            transaction = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {self.transaction_type}: ${self.amount}\n"
            self.save_transaction_log(transaction)
            return True
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return False

    def withdraw(self, amount):
        try:
            self.amount = float(amount)
            if self.amount <= 0:
                raise ValueError("Invalid input: Please enter a valid amount.")
            if self.amount > self.balance:
                self.balance -= 8  # Charge R8 for insufficient funds
                self.transaction_type = "Insufficient Funds Charge"
                self.save_bank_data()
                transaction = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {self.transaction_type}: $8.00\n"
                self.save_transaction_log(transaction)
                messagebox.showinfo("Transaction", "Insufficient funds. R8 charged.")
            else:
                self.balance -= self.amount
                self.transaction_type = "Withdrawal"
                self.save_bank_data()
                transaction = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {self.transaction_type}: ${self.amount}\n"
                self.save_transaction_log(transaction)
            return True
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return False

    def display_balance(self):
        return f"Current Balance: ${self.balance}"

    def display_transaction_log(self):
        self.load_transaction_log()
        return "Transaction Log:\n" + "\n".join(self.transaction_log)

def make_deposit():
    amount = simpledialog.askfloat("Deposit", "How much would you like to deposit?")
    if amount is not None:  # Check if user canceled the dialog
        if bank.deposit(amount):
            update_balance_display()

def make_withdrawal():
    amount = simpledialog.askfloat("Withdrawal", "How much would you like to withdraw?")
    if amount is not None:  # Check if user canceled the dialog
        if bank.withdraw(amount):
            update_balance_display()

def view_statement():
    statement_window = tk.Toplevel()
    statement_window.title("Statement")
    statement_label = tk.Label(statement_window, text=bank.display_transaction_log())
    statement_label.pack()

def update_balance_display():
    balance_label.config(text=bank.display_balance())

def main():
    global bank

    bank = Bank()

    root = tk.Tk()
    root.title("Banking Application")

    deposit_button = tk.Button(root, text="Deposit", command=make_deposit)
    deposit_button.pack()

    withdrawal_button = tk.Button(root, text="Withdrawal", command=make_withdrawal)
    withdrawal_button.pack()

    statement_button = tk.Button(root, text="View Statement", command=view_statement)
    statement_button.pack()

    global balance_label
    balance_label = tk.Label(root, text=bank.display_balance())
    balance_label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
