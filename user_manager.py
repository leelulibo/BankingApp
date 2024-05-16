'''import tkinter as tk
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import messagebox
import smtplib
from bank_app import bank_main

class User:
    def __init__(self, firstname, lastname, phone, email, account_number, password):
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.email = email
        self.account_number = account_number
        self.password = password


    def register_user(self):
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not firstname or not lastname or not phone or not email or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        account_number = self.generate_account_number()
        self.account_entry.config(state="normal")
        self.account_entry.delete(0, tk.END)
        self.account_entry.insert(0, account_number)
        self.account_entry.config(state="readonly")

        with open("user_data.txt", "a") as file:
            file.write(f"{firstname},{lastname},{phone},{email},{account_number},{password}\n")

        messagebox.showinfo("Success", "User registered successfully.")
        self.send_registration_email(firstname, lastname, email, account_number, password)

    def clear_fields(self):
            self.firstname_entry.delete(0, tk.END)
            self.lastname_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

        

    def send_registration_email(self, firstname, lastname, email, account_number, user_password):
        sender_email = "mduduayanda01@gmail.com"  # Your email
        receiver_email = email
        password = "wghb wmhi fwgn qkmu"  # Your email password

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
            
    def login_user(self):
        email = self.login_email_entry.get()
        password = self.login_password_entry.get()

        with open("user_data.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if data[3] == email and data[5] == password:
                    messagebox.showinfo("Success", "Login successful!")
                    # Open bank_app.py page here
                    self.master.destroy()
                    bank_main()
                    return
        messagebox.showerror("Error", "Invalid email or password.")
              '''