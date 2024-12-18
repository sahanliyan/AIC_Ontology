import tkinter as tk
import requests
import math

def create_pentagon_tab(notebook, token_callback):
    """
    Creates a tab for pentagon area and perimeter calculations.
    :param notebook: The parent notebook to attach this tab.
    :param token_callback: A function to retrieve the JWT token.
    :return: The created tab.
    """
    pentagon_tab = tk.Frame(notebook)

    # Input fields for side length
    side_label = tk.Label(pentagon_tab, text="Enter the side length of the pentagon:")
    side_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    side_entry = tk.Entry(pentagon_tab)
    side_entry.grid(row=0, column=1, padx=10, pady=10)

    # Labels for results
    area_label = tk.Label(pentagon_tab, text="Area: ")
    area_label.grid(row=3, column=0, columnspan=2, pady=10)

    perimeter_label = tk.Label(pentagon_tab, text="Perimeter: ")
    perimeter_label.grid(row=4, column=0, columnspan=2, pady=10)

    error_label = tk.Label(pentagon_tab, text="", fg="red")
    error_label.grid(row=5, column=0, columnspan=2)

    # Canvas to display the pentagon
    canvas = tk.Canvas(pentagon_tab, width=450, height=400, bg="white")
    canvas.grid(row=6, column=0, columnspan=2, pady=20)

    # Calculate button
    def calculate_pentagon():
        side = side_entry.get()

        if not side:
            error_label.config(text="Please enter the side length of the pentagon.")
            return

        try:
            side = float(side)
            if side <= 0:
                error_label.config(text="Side length must be positive.")
                return
        except ValueError:
            error_label.config(text="Invalid input. Please enter a numeric value for the side length.")
            return

        try:
            # Retrieve JWT token
            token = token_callback()
            if not token:
                error_label.config(text="Error: No authentication token. Please log in.")
                return

            # Send API request to the backend
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                'http://localhost:5000/calculate_pentagon',
                json={'side': side},
                headers=headers,
                timeout=5
            )
            response.raise_for_status()
            data = response.json()

            # Update labels with results
            area_label.config(text=f"Area: {data['area']:.2f} square units")
            perimeter_label.config(text=f"Perimeter: {data['perimeter']:.2f} units")
            error_label.config(text="")

            # Draw the pentagon on the canvas
            draw_pentagon(side, data['area'], data['perimeter'])

        except requests.exceptions.RequestException as e:
            error_label.config(text=f"Error: {e}")

    calculate_button = tk.Button(pentagon_tab, text="Calculate", command=calculate_pentagon)
    calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Function to draw the pentagon dynamically scaled on the canvas
    def draw_pentagon(side, area, perimeter):
        # Clear the canvas before drawing
        canvas.delete("all")

        # Scale the pentagon to fit the canvas
        scale_factor = 400 // (side * 2)
        scaled_side = side * scale_factor

        # Coordinates for the pentagon (centered)
        center_x, center_y = 450 // 2, 400 // 2
        angle = 72  # Angle for a regular pentagon (360° / 5)

        # Calculate the vertices of the pentagon
        points = []
        for i in range(5):
            x = center_x + scaled_side * math.cos(math.radians(i * angle))
            y = center_y - scaled_side * math.sin(math.radians(i * angle))
            points.append((x, y))

        # Draw the pentagon
        canvas.create_polygon(points, outline="black", fill="lightblue", width=2)

        # Label the side length
        canvas.create_text(center_x, center_y - scaled_side - 10, text=f"Side: {side:.2f}", font=("Arial", 10))

        # Display the area and perimeter in the center
        canvas.create_text(center_x, center_y, text=f"Area: {area:.2f}", font=("Arial", 12, "bold"))
        canvas.create_text(center_x, center_y + 20, text=f"Perimeter: {perimeter:.2f}", font=("Arial", 12, "bold"))

    return pentagon_tab
