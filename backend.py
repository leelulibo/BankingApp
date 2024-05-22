import random
import string
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import tkinter as tk

def generate_account_number():
    return ''.join(random.choices(string.digits, k=8))

def register_user(id_number, firstname, lastname, phone, email, password, address):
    if not id_number.isdigit() or len(id_number) != 13:
        return None, "Invalid ID number."

    if not firstname.isalpha():
        return None, "First name can only contain letters."

    if not lastname.isalpha():
        return None, "Last name can only contain letters."

    if not phone.isdigit() or not phone.startswith('0') or len(phone) != 10:
        return None, "Invalid phone number."

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return None, "Invalid email address."

    if not firstname or not lastname or not phone or not email or not password or not address:
        return None, "Please fill in all fields."

    account_number = generate_account_number()
    user_id = email  # Use email as a unique identifier
    
    with open("user_data.txt", "a") as file:
        file.write(f"{id_number},{firstname},{lastname},{phone},{email},{account_number},{password},{address}\n")

    return account_number, None

def send_registration_email(firstname, lastname, email, account_number, user_password,address ):
    sender_email = "mduduayanda01@gmail.com"
    receiver_email = email
    password = "wghb wmhi fwgn qkmu"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Welcome to Virtual Vault!"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"Dear {firstname} {lastname},\n\nThank you for registering with Virtual Vault. Your account has been successfully created with the following details:\n\nFirst Name: {firstname}\nLast Name: {lastname}\nEmail: {email}\nAccount Number: {account_number}\nPassword: {user_password}\nAddress: {address}\n\nPlease let us know if you have any questions.\n\nBest regards,\nVirtual Vault"

    part = MIMEText(text, "plain")
    message.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def login_user(email, password):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False, None, "Invalid email address."

    with open("user_data.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if data[4] == email and data[6] == password:
                user_id = data[4]  # Use email as the user identifier
                if not os.path.exists(f"{user_id}_TransactionLog.txt"):
                    open(f"{user_id}_TransactionLog.txt", "w").close()
                if not os.path.exists(f"{user_id}_BankData.txt"):
                    open(f"{user_id}_BankData.txt", "w").close()
                return True, user_id, None

    return False, None, "Invalid email or password."


