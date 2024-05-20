import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF
import PyPDF2
import random
import string
import re
from email.mime.text import MIMEText


class Bank:
    def __init__(self, currency="$"):  # Add a currency parameter with a default value
        self.currency = currency
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
            if self.amount <= 0 or self.amount % 10 != 0:
                raise ValueError("Invalid input: Please enter a valid amount in multiples of 10.")
            
            # Inform the user about the charge
            confirmation = messagebox.askyesno("Deposit Charge", 
                                               "A charge of R10 will be applied for this transaction. Do you want to continue?")
            if not confirmation:
                return False
            
            # Deduct the charge from the deposit
            self.amount -= 10
            
            self.balance += self.amount
            self.transaction_type = "Deposit"
            self.save_bank_data()
            transaction = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {self.transaction_type}: ${self.amount}\n"
            self.save_transaction_log(transaction)
            
            # Save the deposit charge as a separate entry
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
                # Inform the user about the charge for withdrawing above their balance
                confirmation = messagebox.askyesno("Withdrawal Charge", 
                                                   "A charge of R8 will be applied for withdrawing above your balance. Do you want to continue?")
                if not confirmation:
                    return False
                
                self.balance -= 8  # Charge R8 for insufficient funds
                
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
            # Append each transaction with the specified currency symbol
            formatted_log += f"{transaction.strip()} {self.currency}\n"
        return formatted_log


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

    send_button = tk.Button(statement_window, text="Send Statement", command=lambda: send_statement_email(email_entry.get(), statement_window))
    send_button.pack()

    back_button = tk.Button(statement_window, text="Back", command=lambda: back_to_main(root, statement_window))
    back_button.pack()


def encrypt_pdf(pdf_file_name):
    output_pdf_file = "encrypted_bank_statement.pdf"
    pdf_writer = PyPDF2.PdfWriter()
    with open(pdf_file_name, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])
        pdf_writer.encrypt("12345")  # Encrypt with password '12345'
        with open(output_pdf_file, "wb") as encrypted_pdf_file:
            pdf_writer.write(encrypted_pdf_file)
    return output_pdf_file


def decrypt_pdf(encrypted_pdf_file):
    decrypted_pdf_file = "decrypted_bank_statement.pdf"
    with open(encrypted_pdf_file, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        if pdf_reader.is_encrypted:
            pdf_reader.decrypt("12345")  # Decrypt with password '12345'
        pdf_writer = PyPDF2.PdfWriter()
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])
        with open(decrypted_pdf_file, "wb") as decrypted_pdf:
            pdf_writer.write(decrypted_pdf)
    return decrypted_pdf_file


def send_statement_email(email, window):
    if email.strip() == "":
        messagebox.showerror("Error", "Please enter a valid email address.")
        return

    sender_email = "mduduayanda01@gmail.com"  # Your email
    receiver_email = email
    password = "wghb wmhi fwgn qkmu"  # Your email password

    # Convert the transaction log text to a PDF file
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    body = bank.display_transaction_log()
    pdf.multi_cell(0, 10, body)
    pdf_file_name = "bank_statement.pdf"
    pdf.output(pdf_file_name)

    # Encrypt the PDF file
    encrypted_pdf_file = encrypt_pdf(pdf_file_name)

    # Attach the encrypted PDF file to the email
    with open(encrypted_pdf_file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {encrypted_pdf_file}",
    )

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Bank Statement"
    msg.attach(part)
    text = msg.as_string()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        messagebox.showinfo("Success", "Statement sent successfully!")
        window.destroy()  # Close the statement window
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {str(e)}")


def back_to_main(root, statement_window):
    statement_window.destroy()  # Close the statement window
    root.deiconify()  # Show the main window


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
    
    send_button = tk.Button(statement_window, text="Send Statement", command=lambda: send_statement_email(email_entry.get(), statement_window))
    send_button.pack()
    
    back_button = tk.Button(statement_window, text="Back", command=lambda: back_to_main(root, statement_window))
    back_button.pack()

def back_to_main(root, statement_window):
    statement_window.destroy()  
    root.deiconify()  

def main():
    global bank, root

    bank = Bank(currency='R')

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
