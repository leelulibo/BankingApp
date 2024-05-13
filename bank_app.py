import tkinter as tk
from tkinter import messagebox

class Bank:
    def __init__(self):
        self.balance = 0
        self.transaction_log = []

    def deposit(self, amount):
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
            self.balance += amount
            self.transaction_log.append(f"Deposit: +${amount}")
            return True
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid amount.")
            return False

    def withdraw(self, amount):
        try:
            amount = float(amount)
            if amount <= 0 or amount > self.balance:
                raise ValueError
            self.balance -= amount
            self.transaction_log.append(f"Withdrawal: -${amount}")
            return True
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid amount.")
            return False

    def display_balance(self):
        messagebox.showinfo("Balance", f"Current Balance: ${self.balance}")

    def display_transaction_log(self):
        log = "Transaction Log:\n" + "\n".join(self.transaction_log)
        messagebox.showinfo("Transaction Log", log)

def make_deposit(entry_amount):  # Receive entry_amount as argument
    amount = entry_amount.get()
    if bank.deposit(amount):
        bank.display_balance()

def make_withdrawal(entry_amount):  # Receive entry_amount as argument
    amount = entry_amount.get()
    if bank.withdraw(amount):
        bank.display_balance()

def show_transaction_log():
    bank.display_transaction_log()

def main():
    global bank  # Declare bank globally for access in functions

    bank = Bank()

    root = tk.Tk()
    root.title("Banking Application")

    label_amount = tk.Label(root, text="Amount:")
    label_amount.grid(row=0, column=0)

    entry_amount = tk.Entry(root)  # Create the entry widget within main
    entry_amount.grid(row=0, column=1)

    button_deposit = tk.Button(root, text="Deposit", command=lambda: make_deposit(entry_amount))
    button_deposit.grid(row=1, column=0)

    button_withdraw = tk.Button(root, text="Withdraw", command=lambda: make_withdrawal(entry_amount))
    button_withdraw.grid(row=1, column=1)

    button_log = tk.Button(root, text="Transaction Log", command=show_transaction_log)
    button_log.grid(row=2, column=0, columnspan=2)

    root.mainloop()


if __name__ == "__main__":
    main()

