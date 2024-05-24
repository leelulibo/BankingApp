from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fpdf import FPDF
from email.mime.base import MIMEBase
from email import encoders
import os
from tkinter import messagebox
import PyPDF2
import customtkinter as ctk
import json


class Bank:
    def __init__(self, user_id, currency="R", account_holder_name="", account_number="", account_holder_address=""):
        self.user_id = user_id
        self.currency = currency
        self.account_holder_name = account_holder_name
        self.account_number = account_number
        self.account_holder_address = account_holder_address
        self.address_last_updated = None  # Store the date when the address was last updated
        self.bank_data_file = f"{user_id}_BankData.txt"
        self.transaction_log_file = f"{user_id}_TransactionLog.txt"
        self.load_bank_data()
        self.load_transaction_log()
        self.load_user_details()
        
    def load_user_details(self):
        # Load user details from JSON file
        with open("user_data.json", "r") as json_file:
            users = json.load(json_file)
            for user in users:
                if user["user_id"] == self.user_id:
                    self.account_holder_name = user["firstname"]
                    self.lastname = user["lastname"]
                    self.phone = user["phone"]
                    self.address = user["address"]
                    break
   
        
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

    def update_address(self, new_address):
        self.account_holder_address = new_address
        self.address_last_updated = datetime.now()

    def address_needs_update(self):
        if self.address_last_updated is None:
            return True
        # Check if it has been more than 14 days since the address was last updated
        return datetime.now() - self.address_last_updated > timedelta(days=14)    
        

    def get_user_file_path(self, filename):
        return f"{self.user_id}_{filename}"

    def load_bank_data(self):
        try:
            with open(self.bank_data_file, 'r') as file:
                self.balance = float(file.readline())
        except FileNotFoundError:
            self.balance = 0

    def save_bank_data(self):
        with open(self.bank_data_file, 'w') as file:
            file.write(str(self.balance))
            
            

    def load_transaction_log(self):
        try:
            with open(self.transaction_log_file, 'r') as file:
                self.transaction_log = file.readlines()
        except FileNotFoundError:
            self.transaction_log = []

    def save_transaction_log(self, transaction):
        with open(self.transaction_log_file, 'a') as file:
            file.write(transaction)
            
    def get_transactions(self):
        transactions = []
        for transaction in self.transaction_log:
            transaction_parts = transaction.strip().split(': ')
            transactions.append(transaction_parts)
        return transactions[::-1]      

    def deposit(self, amount):
        try:
            self.amount = float(amount)
            if self.amount <= 0 or self.amount % 10 != 0:
                raise ValueError("Invalid input: Please enter a valid amount in multiples of 10.")
            
            confirmation = messagebox.askyesno("Deposit Charge", "A charge of R10 will be applied for this transaction. Do you want to continue?")
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
                confirmation = messagebox.askyesno("Withdrawal Charge", "A charge of R8 will be applied for withdrawing above your balance. Do you want to continue?")
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
        return f"Current Balance: {self.currency}{self.balance:.2f}"
    

    def display_transaction_log(self):
        self.load_transaction_log()
        formatted_log = ""
        for transaction in self.transaction_log:
            formatted_log += f"{transaction.strip()} {self.currency}\n"
        return formatted_log
    
    def send_statement_email(self, email):
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
        body = self.display_transaction_log()
        pdf.multi_cell(0, 10, body)
        pdf_file_name = "bank_statement.pdf"
        pdf.output(pdf_file_name)

        with open(pdf_file_name, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {pdf_file_name}")

        msg.attach(part)

        text = msg.as_string()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        
def encrypt_pdf(pdf_file_name):
    output_pdf_file = "encrypted_bank_statement.pdf"
    pdf_writer = PyPDF2.PdfWriter()
    with open(pdf_file_name, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])
        pdf_writer.encrypt("12345")  
        with open(output_pdf_file, "wb") as encrypted_pdf_file:
            pdf_writer.write(encrypted_pdf_file)
    return output_pdf_file


def decrypt_pdf(encrypted_pdf_file):
    decrypted_pdf_file = "decrypted_bank_statement.pdf"
    with open(encrypted_pdf_file, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        if pdf_reader.is_encrypted:
            pdf_reader.decrypt("12345")  
        pdf_writer = PyPDF2.PdfWriter()
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])
        with open(decrypted_pdf_file, "wb") as decrypted_pdf:
            pdf_writer.write(decrypted_pdf)
    return decrypted_pdf_file  

def update_details(self):
    update_window = ctk.CTkToplevel()
    update_window.title("Update Personal Details")
    update_window.geometry("300x300")

    # Labels and entry fields for updating personal detailspip

    phone_label = ctk.CTkLabel(update_window, text="Phone Number:")
    phone_label.pack()

    phone_entry = ctk.CTkEntry(update_window)
    phone_entry.pack()

    address_label = ctk.CTkLabel(update_window, text="Address:")
    address_label.pack()

    address_entry = ctk.CTkEntry(update_window)
    address_entry.pack()

    # Function to handle updating details and sending email
    def update_and_send_email():
        
        phone = phone_entry.get()
        address = address_entry.get()

        # Update details in the backend
        # Assuming you have a method in the Bank class to update user details
        self.bank.update_user_details( phone, address)

        # Send updated details to user's email
        try:
            self.bank.send_update_details_email(  phone, address)
            messagebox.showinfo("Success", "Details updated and email sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {str(e)}")

        # Close the update window after updating
        update_window.destroy()

    # Button to submit updated details
    submit_button = ctk.CTkButton(update_window, text="Submit", command=update_and_send_email)
    submit_button.pack()
  
   