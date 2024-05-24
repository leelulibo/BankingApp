import tkinter as tk
from tkinter import messagebox
import random
import string
import smtplib
import customtkinter as ctk
from customtkinter import CTk, CTkLabel, CTkImage
import random
import string
import re
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image, ImageTk
from tkinter import messagebox

class UserRegistrationApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("User Registration")

        # Bank Logo
        self.bank_logo_image = Image.open("2ILeFf-LogoMakr.png")  # Replace with your logo path
        self.bank_logo = ctk.CTkImage(self.bank_logo_image)
        self.logo_label = ctk.CTkLabel(self, image=self.bank_logo)
        self.logo_label.grid(row=0, column=0, columnspan=3, pady=20)

        # Choose an option label
        self.choice_label = ctk.CTkLabel(self, text="Choose an option:")
        self.choice_label.grid(row=1, column=0, columnspan=3, pady=5)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=2, column=0, columnspan=3, pady=5)
        
        self.register_btn = ctk.CTkButton(self.button_frame, text="Register", command=self.show_register_form)
        self.register_btn.grid(row=0, column=0, padx=2, pady=2)

        self.login_btn = ctk.CTkButton(self.button_frame, text="Login", command=self.show_login_form)
        self.login_btn.grid(row=0, column=1, padx=2, pady=2)

        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)

        # Registration Form
        self.register_frame = ctk.CTkFrame(self)
        self.register_frame.grid(row=3, column=0, columnspan=3)

        self.id_number_label = ctk.CTkLabel(self.register_frame, text="ID Number:")
        self.id_number_label.grid(row=0, column=0, sticky="e")
        self.id_number_entry = ctk.CTkEntry(self.register_frame)
        self.id_number_entry.grid(row=0, column=1)

        self.firstname_label = ctk.CTkLabel(self.register_frame, text="First Name:")
        self.firstname_label.grid(row=1, column=0, sticky="e")
        self.firstname_entry = ctk.CTkEntry(self.register_frame)
        self.firstname_entry.grid(row=1, column=1)

        self.lastname_label = ctk.CTkLabel(self.register_frame, text="Last Name:")
        self.lastname_label.grid(row=2, column=0, sticky="e")
        self.lastname_entry = ctk.CTkEntry(self.register_frame)
        self.lastname_entry.grid(row=2, column=1)

        self.phone_label = ctk.CTkLabel(self.register_frame, text="Phone Number:")
        self.phone_label.grid(row=3, column=0, sticky="e")
        self.phone_entry = ctk.CTkEntry(self.register_frame)
        self.phone_entry.grid(row=3, column=1)

        self.email_label = ctk.CTkLabel(self.register_frame, text="Email Address:")
        self.email_label.grid(row=4, column=0, sticky="e")
        self.email_entry = ctk.CTkEntry(self.register_frame)
        self.email_entry.grid(row=4, column=1)

        self.account_label = ctk.CTkLabel(self.register_frame, text="Account Number:")
        self.account_label.grid(row=5, column=0, sticky="e")
        self.account_entry = ctk.CTkEntry(self.register_frame, state="readonly")
        self.account_entry.grid(row=5, column=1)

        self.password_label = ctk.CTkLabel(self.register_frame, text="Password:")
        self.password_label.grid(row=6, column=0, sticky="e")
        self.password_entry = ctk.CTkEntry(self.register_frame, show="*")
        self.password_entry.grid(row=6, column=1)

        self.generate_password_btn = ctk.CTkButton(self.register_frame, text="Generate Password", command=self.generate_password)
        self.generate_password_btn.grid(row=6, column=2)

        self.register_submit_btn = ctk.CTkButton(self.register_frame, text="Register", command=self.register_user)
        self.register_submit_btn.grid(row=7, columnspan=2)

        # Login Form
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.grid()

        self.login_email_label = ctk.CTkLabel(self.login_frame, text="Email Address:")
        self.login_email_label.grid(row=0, column=0, sticky="e")
        self.login_email_entry = ctk.CTkEntry(self.login_frame)
        self.login_email_entry.grid(row=0, column=1)

        self.login_password_label = ctk.CTkLabel(self.login_frame, text="Password:")
        self.login_password_label.grid(row=1, column=0, sticky="e")
        self.login_password_entry = ctk.CTkEntry(self.login_frame, show="*")
        self.login_password_entry.grid(row=1, column=1)

        self.login_submit_btn = ctk.CTkButton(self.login_frame, text="Login", command=self.login_user)
        self.login_submit_btn.grid(row=2, columnspan=2)

        # Initially hide login form
        self.login_frame.grid_forget()

    def generate_password(self):
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
    
    def generate_account_number(self):
        return ''.join(random.choices(string.digits, k=8))

    def register_user(self):
        id_number = self.id_number_entry.get()
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Check if ID number contains only digits and has a length of 13
        if not id_number.isdigit() or len(id_number) != 13:
            messagebox.showerror("Error", "Invalid ID number.")
            return

        # Check if ID number already exists
        with open("user_data.txt", "r") as file:
            for line in file:
                # Split the line into fields
                fields = line.strip().split(",")

                # Check if the line has the expected number of fields
                if len(fields) != expected_field_count:
                    # Handle the malformed line (e.g., log it, skip it, etc.)
                    print(f"Malformed line: {line}")
                    continue

        # Check if first name contains only letters
        if not firstname.isalpha():
            messagebox.showerror("Error", "First name can only contain letters.")
            return

        # Check if last name contains only letters
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
        self.account_entry.configure(state="normal")
        self.account_entry.delete(0, tk.END)
        self.account_entry.insert(0, account_number)
        self.account_entry.configure(state="readonly")

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
        sender_email = "your_email@gmail.com"  # Your email
        receiver_email = email
        password = "your_email_password"  # Your email password

        message = MIMEMultipart("alternative")
        message["Subject"] = "Welcome to Virtual Vault!"
        message["From"] = sender_email
        message["To"] = receiver_email

        text = f"""\
        Dear {firstname} {lastname},

        Thank you for registering with Virtual Vault. Your account has been successfully created with the following details:

        First Name: {firstname}
        Last Name: {lastname}
        Email: {email}
        Account Number: {account_number}
        Password: {user_password}

        Please let us know if you have any questions.

        Best regards,
        Virtual Vault"""

        part = MIMEText(text, "plain")
        message.attach(part)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

    def show_register_form(self):
        self.register_frame.grid()
        self.login_frame.grid_forget()

    def show_login_form(self):
        self.login_frame.grid()
        self.register_frame.grid_forget()

    def login_user(self):
        email = self.login_email_entry.get()
        password = self.login_password_entry.get()

        # Email validation using regular expression
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid email address.")
            return

        with open("user_data.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if data[4] == email and data[6] == password:  # Adjusted index for email and password
                    messagebox.showinfo("Success", "Login successful!")

                    if os.path.exists(f"{data[0]}_TransactionLog.txt") and os.path.exists(f"{data[0]}_BankData.txt"):
                        # Open existing files
                        with open(f"{data[0]}_TransactionLog.txt", "r") as trans_file, open(f"{data[0]}_BankData.txt", "r") as bank_file:
                            # You can do something with these files here
                            pass
                    else:
                        # Create new files for the user
                        with open(f"{data[0]}_TransactionLog.txt", "w") as trans_file, open(f"{data[0]}_BankData.txt", "w") as bank_file:
                            # You can initialize these files if needed
                            pass

                    # Close the login window
                    self.destroy()

                    # Open bank_app.py window here
                    import bank_app  # Importing bank_app.py
                    bank_app.main()  # Call the main function of bank_app.py to open its window
                    return
        messagebox.showerror("Error", "Invalid email or password.")

def main():
    app = UserRegistrationApp()
    app.mainloop()

if __name__ == "__main__":
    main()
