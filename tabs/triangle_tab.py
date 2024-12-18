import tkinter as tk
import requests
import math

# Global token variable
global_token = None

def create_triangle_tab(notebook, token_callback):
    """
    Creates a tab for Triangle area and perimeter calculations.
    :param notebook: The parent notebook to attach this tab.
    :param token_callback: A function to retrieve the JWT token.
    :return: The created tab.
    """
    triangle_tab = tk.Frame(notebook)
    
    # Input fields for base and height
    base_label = tk.Label(triangle_tab, text="Enter the base of the triangle:")
    base_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    base_entry = tk.Entry(triangle_tab)
    base_entry.grid(row=0, column=1, padx=10, pady=10)

    height_label = tk.Label(triangle_tab, text="Enter the height of the triangle:")
    height_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    height_entry = tk.Entry(triangle_tab)
    height_entry.grid(row=1, column=1, padx=10, pady=10)

    # Labels for results
    area_label = tk.Label(triangle_tab, text="Area: ")
    area_label.grid(row=3, column=0, columnspan=2, pady=10)

    perimeter_label = tk.Label(triangle_tab, text="Perimeter: ")
    perimeter_label.grid(row=4, column=0, columnspan=2, pady=10)

    error_label = tk.Label(triangle_tab, text="", fg="red")
    error_label.grid(row=5, column=0, columnspan=2)

    # Canvas to display the triangle
    canvas = tk.Canvas(triangle_tab, width=450, height=400, bg="white")
    canvas.place(relx=0.5, rely=0.5, anchor="center")
    canvas.grid(row=6, column=0, columnspan=2, pady=20)

    # Calculate button
    def calculate_triangle():
        base = base_entry.get()
        height = height_entry.get()

        if not base or not height:
            error_label.config(text="Please enter both base and height values.")
            return

        try:
            base = float(base)
            height = float(height)
        except ValueError:
            error_label.config(text="Invalid input. Please enter numeric values.")
            return

        try:
            # Retrieve global token
            token = token_callback()
            if not token:
                error_label.config(text="Error: No authentication token. Please log in.")
                return

            # Send API request
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                'http://localhost:5000/calculate_triangle',
                json={'base': base, 'height': height},
                headers=headers,
                timeout=5
            )
            response.raise_for_status()
            data = response.json()

            # Update labels
            area_label.config(text=f"Area: {data['area']:.2f} square units")
            perimeter_label.config(text=f"Perimeter: {data['perimeter']:.2f} units")
            error_label.config(text="")

            # Draw the triangle
            draw_triangle(base, height, data['area'], data['perimeter'])

        except requests.exceptions.RequestException as e:
            error_label.config(text=f"Error: {e}")

    calculate_button = tk.Button(triangle_tab, text="Calculate", command=calculate_triangle)
    calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Function to draw the triangle
    def draw_triangle(base, height, area, perimeter):
        canvas.delete("all")

        # Scale the triangle to fit the canvas
        scale_factor = 300 // max(base, height)
        scaled_base = base * scale_factor
        scaled_height = height * scale_factor

        hypotenuse_actual = math.sqrt(base ** 2 + height ** 2)

        # Coordinates
        x1, y1 = 225-scaled_base/2, 350
        x2, y2 = x1 + scaled_base, y1
        x3, y3 = x1 + (scaled_base / 2), y1 - scaled_height

        # Draw the triangle
        canvas.create_polygon(x1, y1, x2, y2, x3, y3, outline="black", fill="lightblue", width=2)

        # Label sides
        canvas.create_text((x1 + x2) / 2, y1 + 15, text=f"Base: {base:.2f}", font=("Arial", 10))
        canvas.create_text((x3 + x2) / 2, (y3 + y2) / 2, text=f"Hypotenuse: {hypotenuse_actual:.2f}", font=("Arial", 10))
        canvas.create_text((x3 + x1) / 2, (y3 + y1) / 2, text=f"Height: {height:.2f}", font=("Arial", 10))

        # Display area in the middle
        canvas.create_text((x1 + x2 + x3) / 3, (y1 + y2 + y3) / 3, text=f"Area: {area:.2f}", font=("Arial", 12, "bold"))

    return triangle_tab
