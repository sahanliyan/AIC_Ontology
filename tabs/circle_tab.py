import tkinter as tk
import requests

def create_circle_tab(notebook, token_callback):
    """
    Creates a tab for circle area and perimeter calculations.
    :param notebook: The parent notebook to attach this tab.
    :param token_callback: A function to retrieve the JWT token.
    :return: The created tab.
    """
    circle_tab = tk.Frame(notebook)

    # Input fields for radius
    radius_label = tk.Label(circle_tab, text="Enter the radius of the circle:")
    radius_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    radius_entry = tk.Entry(circle_tab)
    radius_entry.grid(row=0, column=1, padx=10, pady=10)

    # Labels for results
    area_label = tk.Label(circle_tab, text="Area: ")
    area_label.grid(row=3, column=0, columnspan=2, pady=10)

    perimeter_label = tk.Label(circle_tab, text="Circumference: ")
    perimeter_label.grid(row=4, column=0, columnspan=2, pady=10)

    error_label = tk.Label(circle_tab, text="", fg="red")
    error_label.grid(row=5, column=0, columnspan=2)

    # Canvas to display the circle
    canvas = tk.Canvas(circle_tab, width=450, height=400, bg="white")
    canvas.grid(row=6, column=0, columnspan=2, pady=20)

    # Calculate button
    def calculate_circle():
        radius = radius_entry.get()

        if not radius:
            error_label.config(text="Please enter the radius of the circle.")
            return

        try:
            radius = float(radius)
            if radius <= 0:
                error_label.config(text="Radius must be a positive number.")
                return
        except ValueError:
            error_label.config(text="Invalid input. Please enter a numeric value for the radius.")
            return

        try:
            # Retrieve global JWT token
            token = token_callback()
            if not token:
                error_label.config(text="Error: No authentication token. Please log in.")
                return

            # Send POST request to the backend API
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                'http://localhost:5000/calculate_circle',
                json={'radius': radius},
                headers=headers,
                timeout=5
            )
            response.raise_for_status()
            data = response.json()

            # Update labels with results
            area_label.config(text=f"Area: {data['area']:.2f} square units")
            perimeter_label.config(text=f"Circumference: {data['perimeter']:.2f} units")
            error_label.config(text="")

            # Draw the circle on the canvas
            draw_circle(radius, data['area'], data['perimeter'])

        except requests.exceptions.RequestException as e:
            error_label.config(text=f"Error: {e}")

    calculate_button = tk.Button(circle_tab, text="Calculate", command=calculate_circle)
    calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Function to draw the circle dynamically scaled on the canvas
    def draw_circle(radius, area, perimeter):
        canvas.delete("all")  # Clear canvas before drawing

        # Scaling factor to fit the circle into the canvas
        scale_factor = 150 / radius
        scaled_radius = radius * scale_factor

        # Coordinates for the circle (centered)
        center_x, center_y = 225, 200

        # Draw the circle
        canvas.create_oval(center_x - scaled_radius, center_y - scaled_radius,
                           center_x + scaled_radius, center_y + scaled_radius,
                           outline="black", fill="lightblue", width=2)

        # Label the radius, area, and circumference
        canvas.create_text(center_x, center_y - scaled_radius - 10, text=f"Radius: {radius:.2f}", font=("Arial", 10))
        canvas.create_text(center_x, center_y, text=f"Area: {area:.2f}", font=("Arial", 12, "bold"))
        canvas.create_text(center_x, center_y + 20, text=f"Circumference: {perimeter:.2f}", font=("Arial", 12, "bold"))

    return circle_tab
