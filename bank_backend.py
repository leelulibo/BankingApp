from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF
import os
import PyPDF2

class Bank:
    def __init__(self, user_id, currency="R", account_holder_name="", account_number="", account_holder_address=""):
        self.user_id = user_id
        self.currency = currency
        self.account_holder_name = account_holder_name
        self.account_number = account_number
        self.account_holder_address = account_holder_address
        self.address_last_updated = None
        self.bank_data_file = f"{user_id}_BankData.txt"
        self.transaction_log_file = f"{user_id}_TransactionLog.txt"
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

    def update_address(self, new_address):
        self.account_holder_address = new_address
        self.address_last_updated = datetime.now()

    def address_needs_update(self):
        if self.address_last_updated is None:
            return True
        return datetime.now() - self.address_last_updated > timedelta(days=14)    

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
            
            confirmation = True # Use a variable to check the confirmation
            if confirmation:
                self.amount -= 10
                self.balance += self.amount
                self.transaction_type = "Deposit"
                self.save_bank_data()
                transaction = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {self.transaction_type}: ${self.amount}\n"
                self.save_transaction_log(transaction)
                
                charge_transaction = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Deposit Charge: $10.00\n"
                self.save_transaction_log(charge_transaction)
                
                return True
            else:
                return False
        except ValueError as e:
            return False

    def withdraw(self, amount):
        try:
            self.amount = float(amount)
            if self.amount <= 0 or self.amount % 10 != 0:
                raise ValueError("Invalid input: Please enter a valid amount in multiples of 10.")
            if self.amount > self.balance:
                confirmation = True # Use a variable to check the confirmation
                if confirmation:
                    self.balance -= 8
                    self.transaction_type = "Insufficient Funds Charge"
                    self.save_bank_data()
                    transaction = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {self.transaction_type}: $8.00\n"
                    self.save_transaction_log(transaction)
                    return False
                else:
                    return False
            else:
                self.balance -= self.amount
                self.transaction_type = "Withdrawal"
                self.save_bank_data()
                transaction = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {self.transaction_type}: ${self.amount}\n"
                self.save_transaction_log(transaction)
                return True
        except ValueError as e:
            return False

    def display_balance(self):
        return f"Current Balance: {self.currency}{self.balance:.2f}"

    def display_transaction_log(self):
        self.load_transaction_log()
        formatted_log = ""
        for transaction in self.transaction_log:
            formatted_log += f"{transaction.strip()} {self.currency}\n"
        return formatted_log
    
    def create_statement_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add logo to the PDF
        pdf.image("2ILeFf-LogoMakr.png", x=120, y=10, w=80)

        pdf.cell(200, 10, txt=f"Account Holder Name: {self.account_holder_name}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Account Number: {self.account_number}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Account Holder Address: {self.account_holder_address}", ln=True, align="L")
        pdf.cell(200, 10, txt="", ln=True)

        body = self.display_transaction_log()
        pdf.multi_cell(0, 10, body)

        pdf_file_name = f"{self.user_id}_bank_statement.pdf"
        pdf.output(pdf_file_name)
        return pdf_file_name

    def send_statement_email(self, email):
        sender_email = "mduduayanda01@gmail.com"
        receiver_email = email
        password = "wghb wmhi fwgn qkmu"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Bank Statement"

        pdf_file_name = self.create_statement_pdf()  # Create PDF statement

        # Attach PDF to the email
        with open(pdf_file_name, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {pdf_file_name}")
        msg.attach(part)

        text = msg.as_string()

        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
        server.quit()

        os.remove(pdf_file_name)  # Remove the temporary PDF file

# Example usage:
bank = Bank(user_id="123456", account_holder_name="John Doe", account_number="1234567890", account_holder_address="123 Main St")
