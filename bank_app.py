import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF
import PyPDF2
import random
import string
import re
from email.mime.text import MIMEText


class Bank:
    def __init__(self, currency="R", account_holder_name="", account_number="", account_holder_address=""):  
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


class UserRegistrationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("User Registration")

        self.choice_label = tk.Label(master, text="Choose an option:")
        self.choice_label.grid(row=0, column=0, columnspan=2)

        self.register_btn = tk.Button(master, text="Register", command=self.show_register_form)
        self.register_btn.grid(row=1, column=0)

        self.login_btn = tk.Button(master, text="Login", command=self.show_login_form)
        self.login_btn.grid(row=1, column=1)

        self.register_frame = tk.Frame(master)
        self.register_frame.grid(row=2, column=0, columnspan=2)
        
        self.id_number_label = tk.Label(self.register_frame, text="ID Number:")
        self.id_number_label.grid(row=0, column=0, sticky="e")
        self.id_number_entry = tk.Entry(self.register_frame)
        self.id_number_entry.grid(row=0, column=1)

        self.firstname_label = tk.Label(self.register_frame, text="First Name:")
        self.firstname_label.grid(row=1, column=0, sticky="e")
        self.firstname_entry = tk.Entry(self.register_frame)
        self.firstname_entry.grid(row=1, column=1)

        self.lastname_label = tk.Label(self.register_frame, text="Last Name:")
        self.lastname_label.grid(row=2, column=0, sticky="e")
        self.lastname_entry = tk.Entry(self.register_frame)
        self.lastname_entry.grid(row=2, column=1)

        self.phone_label = tk.Label(self.register_frame, text="Phone Number:")
        self.phone_label.grid(row=3, column=0, sticky="e")
        self.phone_entry = tk.Entry(self.register_frame)
        self.phone_entry.grid(row=3, column=1)

        self.email_label = tk.Label(self.register_frame, text="Email Address:")
        self.email_label.grid(row=4, column=0, sticky="e")
        self.email_entry = tk.Entry(self.register_frame)
        self.email_entry.grid(row=4, column=1)

        self.account_label = tk.Label(self.register_frame, text="Account Number:")
        self.account_label.grid(row=5, column=0, sticky="e")
        self.account_entry = tk.Entry(self.register_frame, state="readonly")
        self.account_entry.grid(row=5, column=1)

        self.password_label = tk.Label(self.register_frame, text="Password:")
        self.password_label.grid(row=6, column=0, sticky="e")
        self.password_entry = tk.Entry(self.register_frame, show="*")
        self.password_entry.grid(row=6, column=1)

        self.generate_password_btn = tk.Button(self.register_frame, text="Generate Password", command=self.generate_password)
        self.generate_password_btn.grid(row=6, column=2)

        self.register_submit_btn = tk.Button(self.register_frame, text="Register", command=self.register_user)
        self.register_submit_btn.grid(row=7, columnspan=2)

        self.login_frame = tk.Frame(master)
        self.login_frame.grid(row=2, column=0, columnspan=2)

        self.login_email_label = tk.Label(self.login_frame, text="Email Address:")
        self.login_email_label.grid(row=0, column=0, sticky="e")
        self.login_email_entry = tk.Entry(self.login_frame)
        self.login_email_entry.grid(row=0, column=1)

        self.login_password_label = tk.Label(self.login_frame, text="Password:")
        self.login_password_label.grid(row=1, column=0, sticky="e")
        self.login_password_entry = tk.Entry(self.login_frame, show="*")
        self.login_password_entry.grid(row=1, column=1)

        self.login_submit_btn = tk.Button(self.login_frame, text="Login", command=self.login_user)
        self.login_submit_btn.grid(row=2, columnspan=2)

        self.login_frame.grid_remove()

    def generate_password(self):
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def register_user(self):
        id_number = self.id_number_entry.get()
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not id_number.isdigit() or len(id_number) != 13:
            messagebox.showerror("Error", "Invalid ID number.")
            return

        with open("user_data.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if data[0] == id_number:
                    messagebox.showinfo("Existing User", "User already exists. Please log in.")
                    self.show_login_form()  
                    return
            
        if not firstname.isalpha():
            messagebox.showerror("Error", "First name can only contain letters.")
            return

        if not lastname.isalpha():
            messagebox.showerror("Error", "Last name can only contain letters.")
            return
        
        if not phone.isdigit() or not phone.startswith('0') or len(phone) != 10:
            messagebox.showerror("Error", "Invalid phone number.")
            return
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid email address.")
            return

        if not firstname or not lastname or not phone or not email or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        account_number = self.generate_account_number()
        self.account_entry.config(state="normal")
        self.account_entry.delete(0, tk.END)
        self.account_entry.insert(0, account_number)
        self.account_entry.config(state="readonly")

        with open("user_data.txt", "a") as file:
            file.write(f"{id_number},{firstname},{lastname},{phone},{email},{account_number},{password}\n")

        messagebox.showinfo("Success", "User registered successfully.")
        self.send_registration_email(firstname, lastname, email, account_number, password)

    def clear_fields(self):
        self.firstname_entry.delete(0, tk.END)
        self.lastname_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def send_registration_email(self, firstname, lastname, email, account_number, user_password):
        sender_email = "mduduayanda01@gmail.com"  
        receiver_email = email
        password = "wghb wmhi fwgn qkmu"  

        message = MIMEMultipart("alternative")
        message["Subject"] = "Welcome to Virtual Vault!"
        message["From"] = sender_email
        message["To"] = receiver_email

        text = f"Dear {firstname} {lastname},\n\nThank you for registering with Virtual Vault. Your account has been successfully created with the following details:\n\nFirst Name: {firstname}\nLast Name: {lastname}\nEmail: {email}\nAccount Number: {account_number}\nPassword: {user_password}\n\nPlease let us know if you have any questions.\n\nBest regards,\nVirtual Vault"

        part = MIMEText(text, "plain")
        message.attach(part)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

    def show_register_form(self):
        self.register_frame.grid()
        self.login_frame.grid_remove()

    def show_login_form(self):
        self.login_frame.grid()
        self.register_frame.grid_remove()

    def login_user(self):
        email = self.login_email_entry.get()
        password = self.login_password_entry.get()

        with open("user_data.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if data[3] == email and data[5] == password:
                    messagebox.showinfo("Success", "Login successful!")
                    return
        messagebox.showerror("Error", "Invalid email or password.")

    def generate_account_number(self):
        return ''.join(random.choices(string.digits, k=8))


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


def view_statement():
    global root

    root.withdraw()  

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


def send_statement_email(email, window):
    if email.strip() == "":
        messagebox.showerror("Error", "Please enter a valid email address.")
        return

    sender_email = "mduduayanda01@gmail.com"  
    receiver_email = email
    password = "wghb wmhi fwgn qkmu"  

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

    encrypted_pdf_file = encrypt_pdf(pdf_file_name)

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
        window.destroy()  
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {str(e)}")


def back_to_main(root, statement_window):
    statement_window.destroy()  
    root.deiconify()  

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
    bank.load_account_info()  # Load account holder's info from file

    root = tk.Tk()
    root.title("Banking Application")


    # Load logo image
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
