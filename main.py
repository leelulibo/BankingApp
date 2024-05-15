import tkinter as tk
from tkinter import messagebox
import random
import string
import re
from cryptography.fernet import Fernet

key = None  # Define key globally
user_credentials = {}  # Dictionary to store user credentials

# Function to generate a random encryption key
def generate_key():
    return Fernet.generate_key()

# Function to encrypt data using a given key
def encrypt_data(data, key):
    cipher = Fernet(key)
    return cipher.encrypt(data.encode())

# Function to decrypt data using a given key
def decrypt_data(encrypted_data, key):
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_data).decode()

# Function to generate a random password
def generate_password():
    # Define the pool of characters to choose from
    characters = string.ascii_letters + string.digits + string.punctuation
    # Generate a random password of length 12
    return ''.join(random.choices(characters, k=12))

# Function to check if a password meets the strength criteria
def check_password_strength(password):
    # Check if password length is 5
    if len(password) < 4:
        return False
    # Check if password contains at least one lowercase letter
    if not re.search("[a-z]", password):
        return False
    # Check if password contains at least one uppercase letter
    if not re.search("[A-Z]", password):
        return False
    # Check if password contains at least one digit
    if not re.search("[0-9]", password):
        return False
    # Check if password contains at least one symbol
    if not re.search("[!@#$%^&*()_+=-]", password):
        return False
    return True

# Function to register a new user with encrypted credentials
def register_user(full_name, surname, account_number, cell_number, email, password):
    global key  # Access the key defined globally
    
    # Check if account number already exists
    if check_account_existence(account_number):
        messagebox.showerror("Error", "Account number already exists. Please login instead.")
        return None, None, None
    
    key = generate_key()
    username = full_name.lower().replace(" ", "") + "_" + account_number[-4:]  # Create a username from full name and account number
    encrypted_full_name = encrypt_data(full_name, key)
    encrypted_surname = encrypt_data(surname, key)
    encrypted_username = encrypt_data(username, key)
    encrypted_password = encrypt_data(password, key)
    encrypted_cell_number = encrypt_data(cell_number, key)
    encrypted_email = encrypt_data(email, key)

    # Store encrypted credentials in dictionary
    user_credentials[username] = {
        "full_name": encrypted_full_name,
        "surname": encrypted_surname,
        "account_number": account_number,
        "cell_number": encrypted_cell_number,
        "email": encrypted_email,
        "username": encrypted_username,
        "password": encrypted_password
    }

    try:
        with open("user_credentials.txt", "ab") as file:
            file.write(encrypted_full_name + b":" + encrypted_surname + b":" +
                       account_number.encode() + b":" + encrypted_cell_number + b":" +
                       encrypted_email + b":" + encrypted_username + b":" + encrypted_password + b"\n")
        return key, username, password
    except Exception as e:
        messagebox.showerror("Error", f"Registration failed: {str(e)}")
        return None, None, None

# Function to check if the account number already exists
def check_account_existence(account_number):
    with open("user_credentials.txt", "rb") as file:
        for line in file:
            data = line.split(b":")
            if data[2].decode() == account_number:
                return True
    return False

# Function to handle user registration
def register():
    register_window = tk.Toplevel(window)
    register_window.title("Register")

    # Create the register frame
    register_frame = tk.Frame(register_window)

    # Registration widgets
    full_name_label = tk.Label(register_frame, text="Full Name:")
    full_name_label.grid(row=0, column=0, padx=10, pady=5)
    full_name_entry = tk.Entry(register_frame, width=30)
    full_name_entry.grid(row=0, column=1, padx=10, pady=5)

    surname_label = tk.Label(register_frame, text="Surname:")
    surname_label.grid(row=1, column=0, padx=10, pady=5)
    surname_entry = tk.Entry(register_frame, width=30)
    surname_entry.grid(row=1, column=1, padx=10, pady=5)

    account_number_label = tk.Label(register_frame, text="Account Number:")
    account_number_label.grid(row=2, column=0, padx=10, pady=5)
    account_number_entry = tk.Entry(register_frame, width=30)
    account_number_entry.grid(row=2, column=1, padx=10, pady=5)

    cell_number_label = tk.Label(register_frame, text="Cell Number:")
    cell_number_label.grid(row=3, column=0, padx=10, pady=5)
    cell_number_entry = tk.Entry(register_frame, width=30)
    cell_number_entry.grid(row=3, column=1, padx=10, pady=5)

    email_label = tk.Label(register_frame, text="Email Address:")
    email_label.grid(row=4, column=0, padx=10, pady=5)
    email_entry = tk.Entry(register_frame, width=30)
    email_entry.grid(row=4, column=1, padx=10, pady=5)

    password_label = tk.Label(register_frame, text="Password:")
    password_label.grid(row=5, column=0, padx=10, pady=5)
    password_entry = tk.Entry(register_frame, width=30, show="*")
    password_entry.grid(row=5, column=1, padx=10, pady=5)

    generate_password_var = tk.BooleanVar(value=True)
    generate_password_check = tk.Checkbutton(register_frame, text="Generate Password", variable=generate_password_var)
    generate_password_check.grid(row=6, column=0, columnspan=2, pady=5)

    show_password_var = tk.BooleanVar(value=False)
    show_password_check = tk.Checkbutton(register_frame, text="Show Password", variable=show_password_var)
    show_password_check.grid(row=7, column=0, columnspan=2, pady=5)

    def show_password():
        if show_password_var.get():
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    show_password_check.config(command=show_password)

    def validate_input(event):
        # Validation for name and surname
        if event.widget == full_name_entry or event.widget == surname_entry:
            if not validate_name_surname(event.widget.get().strip()):
                event.widget.config(fg="red")
            else:
                event.widget.config(fg="black")  # Change text color back to black if validation succeeds
        # Validation for email address
        elif event.widget == email_entry:
            if not validate_email(event.widget.get().strip()):
                event.widget.config(fg="red")
            else:
                event.widget.config(fg="black")  # Change text color back to black if validation succeeds
        # Validation for cellphone number
        elif event.widget == cell_number_entry:
            if not validate_cellphone(event.widget.get().strip()):
                event.widget.config(fg="red")
            else:
                event.widget.config(fg="black")  # Change text color back to black if validation succeeds
        # Validation for account number
        elif event.widget == account_number_entry:
            if not validate_account_number(event.widget.get().strip()):
                event.widget.config(fg="red")
            elif check_account_existence(event.widget.get().strip()):
                event.widget.config(fg="red")
                messagebox.showerror("Error", "Account number already exists. Please login instead.")
            else:
                event.widget.config(fg="black")  # Change text color back to black if validation succeeds
        # Validation for password
        elif event.widget == password_entry:
            if not check_password_strength(event.widget.get().strip()):
                event.widget.config(fg="red")
            else:
                event.widget.config(fg="black")  # Change text color back to black if validation succeeds
        else:
            # Reset text color to black after validation
            event.widget.config(fg="black")

    full_name_entry.bind("<FocusOut>", validate_input)
    surname_entry.bind("<FocusOut>", validate_input)
    email_entry.bind("<FocusOut>", validate_input)
    cell_number_entry.bind("<FocusOut>", validate_input)
    account_number_entry.bind("<FocusOut>", validate_input)
    password_entry.bind("<FocusOut>", validate_input)

    def register_user_wrapper():
        # Check if all fields are filled
        if (full_name_entry.get().strip() and surname_entry.get().strip() and
                account_number_entry.get().strip() and cell_number_entry.get().strip() and
                email_entry.get().strip()):
            # Validate password strength
            password = password_entry.get().strip()
            if generate_password_var.get():
                password = generate_password()
            if not check_password_strength(password):
                messagebox.showerror("Error", "Password must have a mix of lowercase letters, uppercase letters, numbers, symbols, and a length of 5 characters.")
                return
            # If all fields are filled and password meets strength criteria, proceed with registration
            key, username, password = register_user(full_name_entry.get().strip(),
                                                    surname_entry.get().strip(),
                                                    account_number_entry.get().strip(),
                                                    cell_number_entry.get().strip(),
                                                    email_entry.get().strip(),
                                                    password)
            if key:
                # If registration is successful, show username and password
                messagebox.showinfo("Registration Successful", f"Your username is: {username}\nYour password is: {password}")
                # If registration is successful, close the register window
                register_window.destroy()
        else:
            # If any field is empty, show an error message
            messagebox.showerror("Error", "All fields are required.")

    register_button = tk.Button(register_frame, text="Register", command=register_user_wrapper)
    register_button.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

    # Pack register frame
    register_frame.pack(padx=20, pady=20)

# Function to validate name and surname
def validate_name_surname(text):
    return bool(re.match("^[a-zA-Z]+$", text))

# Function to validate email address
def validate_email(email):
    return bool(re.match("[^@]+@[^@]+\.[^@]+", email))

# Function to validate cellphone number
def validate_cellphone(cellphone):
    return bool(re.match("^0[0-9]{9}$", cellphone))

# Function to validate account number
def validate_account_number(account_number):
    return bool(re.match("^[0-9]{1,10}$", account_number))

# Function to check if entered password matches stored credentials
def check_password_match(account_number, password):
    with open("user_credentials.txt", "rb") as file:
        for line in file:
            data = line.split(b":")
            if data[2].decode() == account_number:
                stored_password = decrypt_data(data[6], key)
                if stored_password == password:
                    return True
                else:
                    return False
    return False

# Function to check if a user exists based on account number
def check_user_existence(account_number):
    with open("user_credentials.txt", "rb") as file:
        for line in file:
            data = line.split(b":")
            if data[2].decode() == account_number:
                return True
    return False

# Function to prompt user for password
def prompt_for_password():
    account_number = account_number_entry.get().strip()
    if check_user_existence(account_number):
        password = messagebox.askstring("Password Required", "Please enter your password:")
        if password:
            # Validate password against stored credentials
            if check_password_match(account_number, password):
                messagebox.showinfo("Login Successful", "You have successfully logged in!")
            else:
                messagebox.showerror("Login Failed", "Incorrect password. Please try again.")
        else:
            messagebox.showerror("Error", "Password cannot be empty.")
    else:
        messagebox.showerror("Error", "User with this account number does not exist.")

# Create a Tkinter window
window = tk.Tk()
window.title("Secure Banking Application")

# Set background color to light blue
window.configure(bg="#ADD8E6")  # Hex color code for light blue

# Create the main frame
main_frame = tk.Frame(window, bg="#ADD8E6")  # Set background color of the frame to match window color

# Money label
money_label = tk.Label(main_frame, text="Money", font=("Helvetica", 24, "italic"), bg="#ADD8E6")  # Set background color of label
money_label.grid(row=0, column=0, pady=20)

# Registration Button
register_button = tk.Button(main_frame, text="Register", width=15, command=register)
register_button.grid(row=1, column=0, pady=5)

# Account Number Label
account_number_label = tk.Label(main_frame, text="Account Number:", bg="#ADD8E6")
account_number_label.grid(row=2, column=0, pady=5)

# Account Number Entry
account_number_entry = tk.Entry(main_frame, width=30)
account_number_entry.grid(row=2, column=1, pady=5)

# Login Button
login_button = tk.Button(main_frame, text="Login", width=15, command=prompt_for_password)
login_button.grid(row=3, column=0, pady=5)

# Pack main frame
main_frame.pack(pady=50)

# Run the Tkinter event loop
window.mainloop()
