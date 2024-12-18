import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # For displaying images
import requests

def create_home_tab(notebook, set_global_token):
    """
    Creates the home tab with a login system, a welcome image, and a greeting for the logged-in user.
    :param notebook: The parent notebook to attach this tab.
    :param set_global_token: Function to store the authentication token globally.
    :return: The created home tab.
    """
    home_tab = tk.Frame(notebook)
    logged_in_user = tk.StringVar(value="")  # Holds the username after login

    # Load and display the welcome image
    def load_image():
        try:
            img = Image.open("res/home.png")  # Replace with the correct path to your image file
            img = img.resize((400, 400))
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    welcome_image = load_image()

    if welcome_image:
        image_label = tk.Label(home_tab, image=welcome_image)
        image_label.image = welcome_image  # Keep a reference to avoid garbage collection
        image_label.grid(row=0, column=0, columnspan=2, pady=10)

     # Title
    title_label = tk.Label(home_tab, text="Welcome to the Geometric Shape Calculator", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=20)

    # Display the greeting message at the top
    greeting_label = tk.Label(home_tab, text="", font=("Arial", 14, "bold"), fg="green")
    greeting_label.grid(row=1, column=0, columnspan=2, pady=10)

    
    # Login Form
    login_frame = tk.LabelFrame(home_tab, text="User Login", padx=20, pady=20, font=("Arial", 12, "bold"))
    login_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    username_label = tk.Label(login_frame, text="Username:")
    username_label.grid(row=0, column=0, sticky="e", pady=5)
    username_entry = tk.Entry(login_frame)
    username_entry.grid(row=0, column=1, pady=5)

    password_label = tk.Label(login_frame, text="Password:")
    password_label.grid(row=1, column=0, sticky="e", pady=5)
    password_entry = tk.Entry(login_frame, show="*")
    password_entry.grid(row=1, column=1, pady=5)

    # Notification Frame
    notification_label = tk.Label(home_tab, text="", fg="red", wraplength=400)
    notification_label.grid(row=3, column=0, columnspan=2, pady=10)

    # Function to handle login
    def login():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            notification_label.config(text="Error: Both username and password are required.", fg="red")
            return

        try:
            response = requests.post(
                "http://localhost:5000/login",  # Adjust the API endpoint as needed
                json={"username": username, "password": password},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()

            # Successful login
            token = data.get("access_token")
            if token:
                set_global_token(token)  # Set the global token
                logged_in_user.set(username)
                greeting_label.config(text=f"Welcome, {username}!")
                notification_label.config(text="Login successful!", fg="green")
            else:
                notification_label.config(text="Error: Login failed. No token received.", fg="red")

        except requests.exceptions.RequestException as e:
            notification_label.config(text=f"Error: {e}", fg="red")

    # Login Button
    login_button = tk.Button(login_frame, text="Login", command=login)
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Adjust window icon
    def set_window_icon(window):
        try:
            icon_image = "res/home.png"  # Path to the image file
            window.iconphoto(False, tk.PhotoImage(file=icon_image))
        except Exception as e:
            print(f"Error setting window icon: {e}")

    # Apply the window icon when this tab is opened
    parent_window = notebook.winfo_toplevel()
    set_window_icon(parent_window)

    return home_tab
