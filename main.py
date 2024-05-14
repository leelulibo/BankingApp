import tkinter as tk
from tkinter import messagebox
import random
import string
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


# Function to register a new user with encrypted credentials
def register_user(full_name, surname, account_number, cell_number, email):
    global key  # Access the key defined globally
    key = generate_key()
    username = full_name.lower().replace(" ", "") + "_" + account_number[-4:]  # Create a username from full name and account number
    password = generate_password()  # Generate a random password
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

    def register_user_wrapper():
        # Check if all fields are filled
        if (full_name_entry.get().strip() and surname_entry.get().strip() and
                account_number_entry.get().strip() and cell_number_entry.get().strip() and
                email_entry.get().strip()):
            # If all fields are filled, proceed with registration
            key, username, password = register_user(full_name_entry.get().strip(),
                                                    surname_entry.get().strip(),
                                                    account_number_entry.get().strip(),
                                                    cell_number_entry.get().strip(),
                                                    email_entry.get().strip())
            if key:
                # If registration is successful, show username and password
                messagebox.showinfo("Registration Successful", f"Your username is: {username}\nYour password is: {password}")
                # If registration is successful, close the register window
                register_window.destroy()
        else:
            # If any field is empty, show an error message
            messagebox.showerror("Error", "All fields are required.")

    register_button = tk.Button(register_frame, text="Register", command=register_user_wrapper)
    register_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    # Pack register frame
    register_frame.pack(padx=20, pady=20)


# Function to handle user login
def login():
    # Close the main window
    window.destroy()

    # Create a new Tkinter window for login
    login_window = tk.Tk()
    login_window.title("Login")

    # Create the login frame
    login_frame = tk.Frame(login_window)

    # Login widgets
    username_label = tk.Label(login_frame, text="Username:")
    username_label.grid(row=0, column=0, padx=10, pady=5)
    username_entry = tk.Entry(login_frame, width=30)
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    password_label = tk.Label(login_frame, text="Password:")
    password_label.grid(row=1, column=0, padx=10, pady=5)
    password_entry = tk.Entry(login_frame, width=30, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    def authenticate():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        # Check if username exists in user_credentials dictionary
        if username in user_credentials:
            # Retrieve encrypted password for the given username
            encrypted_password = user_credentials[username]["password"]
            decrypted_password = decrypt_data(encrypted_password, key)

            # Check if entered password matches decrypted password
            if password == decrypted_password:
                messagebox.showinfo("Login", "Login successful!")
            else:
                messagebox.showerror("Login Failed", "Invalid password.")
        else:
            messagebox.showerror("Login Failed", "User not found.")

    login_button = tk.Button(login_frame, text="Login", command=authenticate)
    login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    # Pack login frame
    login_frame.pack(padx=20, pady=20)

    # Run the Tkinter event loop for the login window
    login_window.mainloop()


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

# Buttons
register_button = tk.Button(main_frame, text="Register", width=15, command=register)
register_button.grid(row=1, column=0, pady=5)

login_button = tk.Button(main_frame, text="Login", width=15, command=login)
login_button.grid(row=2, column=0, pady=5)

# Pack main frame
main_frame.pack(pady=50)

# Run the Tkinter event loop
window.mainloop()
