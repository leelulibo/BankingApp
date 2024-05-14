import tkinter as tk
from tkinter import messagebox
import random
import string
from cryptography.fernet import Fernet
import pyotp
import webbrowser

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
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

# Function to register a new user with encrypted credentials
def register_user(username, password):
    key = generate_key()
    encrypted_username = encrypt_data(username, key)
    encrypted_password = encrypt_data(password, key)
    with open("user_credentials.txt", "ab") as file:
        file.write(encrypted_username + b":" + encrypted_password + b"\n")
    return key

# Function to reset password for a user
def reset_password(username, new_password):
    with open("user_credentials.txt", "rb") as file:
        lines = file.readlines()
    with open("user_credentials.txt", "wb") as file:
        for line in lines:
            encrypted_username, encrypted_password = line.strip().split(b":")
            decrypted_username = decrypt_data(encrypted_username, key)
            if username == decrypted_username:
                encrypted_password = encrypt_data(new_password, key)
                file.write(encrypted_username + b":" + encrypted_password + b"\n")
            else:
                file.write(line)

# Function to login user with multi-factor authentication
def login_user(username, password, otp_code, key):
    with open("user_credentials.txt", "rb") as file:
        for line in file:
            encrypted_username, encrypted_password = line.strip().split(b":")
            decrypted_username = decrypt_data(encrypted_username, key)
            decrypted_password = decrypt_data(encrypted_password, key)
            if username == decrypted_username and password == decrypted_password:
                totp = pyotp.TOTP("base32secret3232")
                if totp.verify(otp_code):
                    return True
    return False

# Function to toggle password visibility
def toggle_password_visibility():
    if password_entry.cget("show") == "":
        password_entry.config(show="*")
    else:
        password_entry.config(show="")

# Function to handle user registration
def register():
    main_page_frame.pack_forget()  # Hide the main page frame
    register_form_frame.pack()     # Show the register form frame

# Function to handle user login
def login():
    main_page_frame.pack_forget()  # Hide the main page frame
    login_form_frame.pack()        # Show the login form frame

# Function to handle password reset
def forgot_password():
    login_form_frame.pack_forget()       # Hide the login form frame
    forgot_password_frame.pack()         # Show the forgot password frame

# Function to go back to the main page
def go_back():
    register_form_frame.pack_forget()    # Hide the register form frame
    login_form_frame.pack_forget()       # Hide the login form frame
    forgot_password_frame.pack_forget()  # Hide the forgot password frame
    main_page_frame.pack()               # Show the main page frame

# Function to reset the password after verification
def reset_after_verification():
    username = verification_username_entry.get()
    new_password = generate_password()
    if username:
        reset_password(username, new_password)
        messagebox.showinfo("Password Reset", f"Your new password is: {new_password}")
        go_back()
    else:
        messagebox.showerror("Error", "Please enter your username.")

# Create a Tkinter window
window = tk.Tk()
window.title("Secure Banking Application")

# Create the main page frame
main_page_frame = tk.Frame(window)

# Create buttons for registration and login on the main page
register_button = tk.Button(main_page_frame, text="Register", command=register)
register_button.pack(pady=5)

login_button = tk.Button(main_page_frame, text="Login", command=login)
login_button.pack(pady=5)

# Create the register form frame
register_form_frame = tk.Frame(window)

# Create entry fields for register form
register_username_label = tk.Label(register_form_frame, text="Username:")
register_username_label.pack(pady=5)
register_username_entry = tk.Entry(register_form_frame, width=30, font=("Arial", 12), bd=3)
register_username_entry.pack(pady=5)

register_password_label = tk.Label(register_form_frame, text="Password:")
register_password_label.pack(pady=5)
register_password_entry = tk.Entry(register_form_frame, width=30, font=("Arial", 12), bd=3, show="*")
register_password_entry.pack(pady=5)

# Create a button to submit the registration form
register_submit_button = tk.Button(register_form_frame, text="Register", command=register)
register_submit_button.pack(pady=5)

# Create a button to go back to the main page from the register form
register_back_button = tk.Button(register_form_frame, text="Back", command=go_back)
register_back_button.pack(pady=5)

# Create the login form frame
login_form_frame = tk.Frame(window)

# Create entry fields for login form
login_username_label = tk.Label(login_form_frame, text="Username:")
login_username_label.pack(pady=5)
login_username_entry = tk.Entry(login_form_frame, width=30, font=("Arial", 12), bd=3)
login_username_entry.pack(pady=5)

login_password_label = tk.Label(login_form_frame, text="Password:")
login_password_label.pack(pady=5)
login_password_entry = tk.Entry(login_form_frame, width=30, font=("Arial", 12), bd=3, show="*")
login_password_entry.pack(pady=5)

# Create a button to submit the login form
login_submit_button = tk.Button(login_form_frame, text="Login", command=login)
login_submit_button.pack(pady=5)

# Create a button to go back to the main page from the login form
login_back_button = tk.Button(login_form_frame, text="Back", command=go_back)
login_back_button.pack(pady=5)

# Create a button to reset password on the login form
forgot_password_button = tk.Button(login_form_frame, text="Forgot Password", command=forgot_password)
forgot_password_button.pack(pady=5)

# Create a Checkbutton to toggle password visibility in the login form
show_password_var = tk.BooleanVar()
show_password_checkbox = tk.Checkbutton(login_form_frame, text="Show Password", variable=show_password_var, command=toggle_password_visibility)
show_password_checkbox.pack(pady=5)

# Create the forgot password form frame
forgot_password_frame = tk.Frame(window)

# Create entry fields for the forgot password form
verification_username_label = tk.Label(forgot_password_frame, text="Username:")
verification_username_label.pack(pady=5)
verification_username_entry = tk.Entry(forgot_password_frame, width=30, font=("Arial", 12), bd=3)
verification_username_entry.pack(pady=5)

# Create a button to submit the forgot password form
verification_submit_button = tk.Button(forgot_password_frame, text="Verify and Reset Password", command=reset_after_verification)
verification_submit_button.pack(pady=5)

# Create a button to go back to the main page from the forgot password form
verification_back_button = tk.Button(forgot_password_frame, text="Back", command=go_back)
verification_back_button.pack(pady=5)

# Pack the main page frame to the window
main_page_frame.pack()

# Run the Tkinter event loop
window.mainloop()
