import tkinter as tk
from tkinter import messagebox
import random
import string
import smtplib
import re
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
<<<<<<< HEAD
from PIL import Image, ImageTk
=======
from bank_app import bank_main
>>>>>>> e27ec71b25e35ffea47d703bf91abf980aac0010

class UserRegistrationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("User Registration")

        # Bank Logo
        self.bank_logo = Image.open("2ILeFf-LogoMakr.png")  # Replace "bank_logo.png" with the path to your bank logo image
        self.bank_logo = ImageTk.PhotoImage(self.bank_logo)
        self.logo_label = tk.Label(master, image=self.bank_logo)
        self.logo_label.grid(row=0, column=0, columnspan=3, pady=20)

        # Choose an option label
        self.choice_label = tk.Label(master, text="Choose an option:")
        self.choice_label.grid(row=1, column=0, columnspan=3, pady=5)

        self.button_frame = tk.Frame(master)
        self.button_frame.grid(row=2, column=0, columnspan=3, pady=5)
        

        self.register_btn = tk.Button(self.button_frame, text="Register", command=self.show_register_form)
        self.register_btn.grid(row=0, column=0, padx=2, pady=2)

        self.login_btn = tk.Button(self.button_frame, text="Login", command=self.show_login_form)
        self.login_btn.grid(row=0, column=1, padx=2, pady=2)
        
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)

        # Registration Form
        self.register_frame = tk.Frame(master)
        self.register_frame.grid(row=3, column=0, columnspan=3)
        
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
        


        # Login Form
        self.login_frame = tk.Frame(master)
        self.login_frame.grid()

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
                data = line.strip().split(",")
                if data[0] == id_number:
                    messagebox.showinfo("Existing User", "User already exists. Please log in.")
                    self.show_login_form()  # Direct user to login form
                    return
            
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
<<<<<<< HEAD
                    
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
                    self.master.destroy()
                    
                    # Open bank_app.py window here
                    import bank_app  # Importing bank_app.py
                    bank_app.main()  # Call the main function of bank_app.py to open its window
=======
                    # Open bank_app.py page here
                    self.master.destroy()
                    bank_main()
>>>>>>> e27ec71b25e35ffea47d703bf91abf980aac0010
                    return
        messagebox.showerror("Error", "Invalid email or password.")

def main():
    root = tk.Tk()
    app = UserRegistrationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
