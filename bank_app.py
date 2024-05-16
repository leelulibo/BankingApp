import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fpdf import FPDF
from email.mime.base import MIMEBase
from email import encoders

class Bank:
    def __init__(self, currency="$", account_holder_name="", account_number="", account_holder_address=""):  
        self.currency = currency
        self.account_holder_name = account_holder_name
        self.account_number = account_number
        self.account_address = account_holder_address
        self.load_bank_data()
        self.load_transaction_log()

    def set_account_info(self, name, number, address):
        self.account_holder_name = name
        self.account_number = number
        self.account_holder_address = address

    def get_account_holder_name(self):
        return self.account_holder_name

    def get_account_number(self):
        return self.account_number
    
    def get_account_holder_address(self):
        return self.account_holder_address

    def load_bank_data(self):
        try:
            with open('BankData.txt', 'r') as file:
                self.balance = float(file.readline())
        except FileNotFoundError:
            self.balance = 0

    def load_account_info(self):
        try:
            with open('AccountInfo.txt', 'r') as file:
                data = file.readline().strip().split(',')
                self.account_holder_name = data[0]
                self.account_number = data[1]
        except FileNotFoundError:
            pass  # Handle missing file

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
            if self.amount <= 0 or self.amount % 10 != 0:
                raise ValueError("Invalid input: Please enter a valid amount in multiples of 10.")
            
            confirmation = messagebox.askyesno("Deposit Charge", 
                                               "A charge of R10 will be applied for this transaction. Do you want to continue?")
            if not confirmation:
                return False
            
            self.amount -= 10
            
            self.balance += self.amount
            self.transaction_type = "Deposit"
            self.save_bank_data()
            transaction = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {self.transaction_type}: ${self.amount}\n"
            self.save_transaction_log(transaction)
            
            charge_transaction = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Deposit Charge: $10.00\n"
            self.save_transaction_log(charge_transaction)
            
            return True
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return False

    def withdraw(self, amount):
        try:
            self.amount = float(amount)
            if self.amount <= 0 or self.amount % 10 != 0:
                raise ValueError("Invalid input: Please enter a valid amount in multiples of 10.")
            if self.amount > self.balance:
                confirmation = messagebox.askyesno("Withdrawal Charge", 
                                                   "A charge of R8 will be applied for withdrawing above your balance. Do you want to continue?")
                if not confirmation:
                    return False
                
                self.balance -= 8  
                
                self.transaction_type = "Insufficient Funds Charge"
                self.save_bank_data()
                transaction = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {self.transaction_type}: $8.00\n"
                self.save_transaction_log(transaction)
                messagebox.showinfo("Transaction", "Insufficient funds. R8 charged.")
                return False
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
        formatted_log = ""
        for transaction in self.transaction_log:
            formatted_log += f"{transaction.strip()} {self.currency}\n"
        return formatted_log

def make_deposit():
    amount = simpledialog.askfloat("Deposit", "How much would you like to deposit?")
    if amount is not None:  
        if bank.deposit(amount):
            update_balance_display()

def make_withdrawal():
    amount = simpledialog.askfloat("Withdrawal", "How much would you like to withdraw?")
    if amount is not None:  
        if bank.withdraw(amount):
            update_balance_display()

def send_statement_email(email, window, email_entry, send_button):
    if email.strip() == "":
        messagebox.showerror("Error", "Please enter a valid email address.")
        return
    
    sender_email = "mduduayanda01@gmail.com"  
    receiver_email = email
    password = "wghb wmhi fwgn qkmu"  

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Bank Statement"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    account_holder_name = bank.get_account_holder_name()
    account_number = bank.get_account_number()
    pdf.cell(200, 10, f"Account Holder: {account_holder_name}", ln=True)
    pdf.cell(200, 10, f"Account Number: {account_number}", ln=True)
    pdf.cell(200, 10, "", ln=True)  
    
    body = bank.display_transaction_log()
    pdf.multi_cell(0, 10, body)
    
    pdf_file_name = "bank_statement.pdf"
    pdf.output(pdf_file_name)

    with open(pdf_file_name, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {pdf_file_name}",
    )

    msg.attach(part)

    text = msg.as_string()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        messagebox.showinfo("Success", "Statement sent successfully!")
        email_entry.config(state=tk.DISABLED)
        send_button.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {str(e)}")

def update_balance_display():
    balance_label.config(text=bank.display_balance())

def view_statement():
    global root
    
    root.withdraw()  # Hide the main window
    
    statement_window = tk.Toplevel()
    statement_window.title("Statement")
    statement_window.geometry("400x450")
    
    statement_text = scrolledtext.ScrolledText(statement_window, width=40, height=10)
    statement_text.insert(tk.END, bank.display_transaction_log())
    statement_text.pack(fill=tk.BOTH, expand=True)
    
    email_label = tk.Label(statement_window, text="Enter your email address:")
    email_label.pack()
    
    email_entry = tk.Entry(statement_window)
    email_entry.pack()
    
    send_button = tk.Button(statement_window, text="Send Statement", command=lambda: send_statement_email(email_entry.get(), statement_window, email_entry, send_button))
    send_button.pack()
    
    back_button = tk.Button(statement_window, text="Back", command=lambda: back_to_main(root, statement_window))
    back_button.pack()

def back_to_main(root, statement_window):
    statement_window.destroy()  
    root.deiconify()  

def main():
    global bank, root

    bank = Bank(currency='R')
    bank.load_account_info()  # Load account holder's info from file

    root = tk.Tk()
    root.title("Banking Application")

    # Load logo image
    logo_image = tk.PhotoImage(file="2ILeFf-LogoMakr.png")
    logo_label = tk.Label(root, image=logo_image)
    logo_label.pack()

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
