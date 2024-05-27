import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import string
import random
from backend import register_user, login_user, send_registration_email
from bank_backend import Bank
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import face_recognition
import cv2
import numpy as np
import os



class UserRegistrationApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("450x520")
        self.master.title("User Registration")
        self.on_login_success = None  # Callback for successful login
        
        

        # Bank Logo
        try:
            bank_logo_img = Image.open("2ILeFf-LogoMakr.png")  # Replace with your path
            self.bank_logo = ImageTk.PhotoImage(bank_logo_img)
            self.logo_label = ctk.CTkLabel(master, image=self.bank_logo)
            self.logo_label.grid(row=0, column=0, columnspan=3, pady=20)
        except Exception as e:
            print("Error loading image:", e)
    
        # Choose an option label
        self.choice_label = ctk.CTkLabel(master, text="Choose an option:")
        self.choice_label.grid(row=1, column=0, columnspan=3, pady=5)

        self.button_frame = ctk.CTkFrame(master)
        self.button_frame.grid(row=2, column=0, columnspan=3, pady=5)

        self.register_btn = ctk.CTkButton(self.button_frame, text="Register", command=self.show_register_form)
        self.register_btn.grid(row=0, column=0, padx=2, pady=2)

        self.login_btn = ctk.CTkButton(self.button_frame, text="Login", command=self.show_login_form)
        self.login_btn.grid(row=0, column=1, padx=2, pady=2)

        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)

        # Registration Form
        self.register_frame = ctk.CTkFrame(master)
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
        
        self.address_label = ctk.CTkLabel(self.register_frame, text="Address:")
        self.address_label.grid(row=7, column=0, sticky="e")
        self.address_entry = ctk.CTkEntry(self.register_frame)
        self.address_entry.grid(row=7, column=1)

        self.register_submit_btn = ctk.CTkButton(self.register_frame, text="Register", command=self.register_user)
        self.register_submit_btn.grid(row=8, columnspan=2)

        # Login Form
        self.login_frame = ctk.CTkFrame(master)
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
        '''
        self.face_recognition_frame = ctk.CTkFrame(master)
        self.face_recognition_frame.grid(row=3, column=0, columnspan=3)
        self.face_recognition_frame.grid_forget()

        self.face_id_number_label = ctk.CTkLabel(self.face_recognition_frame, text="ID Number:")
        self.face_id_number_label.grid(row=0, column=0, sticky="e")
        self.face_id_number_entry = ctk.CTkEntry(self.face_recognition_frame)
        self.face_id_number_entry.grid(row=0, column=1)

        self.capture_face_btn = ctk.CTkButton(self.face_recognition_frame, text="Capture Face", command=self.capture_face)
        self.capture_face_btn.grid(row=1, columnspan=2)
        '''
        
        
        
        # Initially hide login form
        self.login_frame.grid_forget()
        '''
    def enable_face_recognition(self):
        self.face_recognition_frame.grid()
        self.register_frame.grid_forget()
        self.login_frame.grid_forget()
    # Add your face recognition setup code here
    # For example, you can start the camera and capture faces
        messagebox.showinfo("Face Recognition", "Face recognition enabled. Please look at the camera.")
        self.capture_face() 
        '''
    
        
    def generate_account_number(self):
      return ''.join(random.choices(string.digits, k=8))  
  
   
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
        address = self.address_entry.get()
        
        if not id_number.isdigit() or len(id_number) != 13:
            messagebox.showerror("Error", "Invalid ID number.")
            return

        with open("user_data.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if data[0] == id_number:
                    messagebox.showinfo("Existing User", "User with this ID number already exists. Please log in or use a different ID number.")
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

        if not id_number or not firstname or not lastname or not phone or not email or not password or not address:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        account_number = self.generate_account_number()
        self.account_entry.configure(state="normal")
        self.account_entry.delete(0, ctk.END)
        self.account_entry.insert(0, account_number)
        self.account_entry.configure(state="readonly")

        with open("user_data.txt", "a") as file:
            file.write(f"{id_number},{firstname},{lastname},{phone},{email},{account_number},{password},{address}\n")

        messagebox.showinfo("Success", "User registered successfully.")
        self.send_registration_email(firstname, lastname, email, account_number, password, address)
        
    def send_registration_email(self, firstname, lastname, email, account_number, user_password, address):
        sender_email = "mduduayanda01@gmail.com"  # Your email
        receiver_email = email
        password = "wghb wmhi fwgn qkmu"  # Your email password
 
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
    

    def show_register_form(self):
        self.register_frame.grid()
        self.login_frame.grid_forget()
        self.face_recognition_btn.grid_forget()
        self.face_recognition_login_btn.grid_forget()

    def show_login_form(self):
        self.login_frame.grid()
        self.register_frame.grid_forget()
        '''
        self.face_recognition_btn = ctk.CTkButton(self.button_frame, text="Enable Face Recognition", command=self.enable_face_recognition)
        self.face_recognition_btn.grid(row=0, column=2, padx=2, pady=2)
        '''
        

    def login_user(self):
        email = self.login_email_entry.get()
        password = self.login_password_entry.get()

        success,user_id, error_message = login_user(email, password)
        if success:
            messagebox.showinfo("Success", "Login successful!")
            if self.on_login_success:
                self.on_login_success(user_id)
        else:
            messagebox.showerror("Error", error_message)
        '''    
    def capture_face(self):
        id_number = self.face_id_number_entry.get()
        if not id_number:
            messagebox.showerror("Error", "Please enter ID number before capturing face.")
            return

        # Check if ID exists in user_data.txt
        user_exists = False
        with open("user_data.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if data[0] == id_number:
                    user_exists = True
                    break

        if not user_exists:
            messagebox.showerror("Error", "ID not found. Please register first.")
            return

            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()

            if ret:
          # Convert the image from BGR (OpenCV format) to RGB (face_recognition format)
            rgb_frame = frame[:, :, ::-1]

          # Display the frame
            cv2.imshow('Camera Feed', frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            # Detect faces in the frame
            face_locations = face_recognition.face_locations(rgb_frame)
            if face_locations:
                # Get the face encodings
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                if face_encodings:
                    # Save the face encoding
                    face_encoding = face_encodings[0]
                    face_data_file = f"{id_number}_face.npy"
                    with open(face_data_file, 'wb') as f:
                        np.save(f, face_encoding)
                    messagebox.showinfo("Success", "Face captured and saved successfully.")
                else:
                    messagebox.showerror("Error", "No face detected. Please try again.")
            else:
                messagebox.showerror("Error", "No face detected. Please try again.")
        else:
            messagebox.showerror("Error", "Failed to capture image. Please try again.")
            

    def capture_face(self):
        id_number = self.face_id_number_entry.get()
        if not id_number:
            messagebox.showerror("Error", "Please enter ID number before capturing face.")
            return

        # Check if ID exists in user_data.txt
        user_exists = False
        with open("user_data.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if data[0] == id_number:
                    user_exists = True
                    break

        if not user_exists:
            messagebox.showerror("Error", "ID not found. Please register first.")
            return

        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if ret:
            # Convert the image from BGR (OpenCV format) to RGB (face_recognition format)
            rgb_frame = frame[:, :, ::-1]

            # Display the frame
            cv2.imshow('Camera Feed', frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            # Detect face locations
            face_locations = face_recognition.face_locations(rgb_frame)

            # Ensure at least one face is detected
            if face_locations:
                # Get face encodings for the detected faces
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                if face_encodings:
                    face_encoding = face_encodings[0]  # Assuming only one face for simplicity
                    for file in os.listdir():
                        if file.endswith("_face.npy"):
                            saved_face_encoding = np.load(file)
                            matches = face_recognition.compare_faces([saved_face_encoding], face_encoding)
                            if True in matches:
                                matched_id_number = file.split('_')[0]
                                with open("user_data.txt", "r") as f:
                                    for line in f:
                                        data = line.strip().split(",")
                                        if data[0] == matched_id_number:
                                            messagebox.showinfo("Success", f"Login successful for {data[1]} {data[2]}!")
                                            if self.on_login_success:
                                                self.on_login_success(matched_id_number)
                                            return
                    messagebox.showerror("Error", "No matching face found.")
                else:
                    messagebox.showerror("Error", "No face encodings found. Please try again.")
            else:
                messagebox.showerror("Error", "No face detected. Please try again.")
        else:
            messagebox.showerror("Error", "Failed to capture image. Please try again.")
'''