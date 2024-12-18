import tkinter as tk
import requests


def create_trapezoid_tab(notebook, token_callback):
    """
    Creates a tab for trapezoid area and perimeter calculations.
    :param notebook: The parent notebook to attach this tab.
    :param token_callback: A function to retrieve the JWT token.
    :return: The created tab.
    """
    trapezoid_tab = tk.Frame(notebook)

    # Input fields for bases and height
    base1_label = tk.Label(trapezoid_tab, text="Enter the length of base 1:")
    base1_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    base1_entry = tk.Entry(trapezoid_tab)
    base1_entry.grid(row=0, column=1, padx=10, pady=10)

    base2_label = tk.Label(trapezoid_tab, text="Enter the length of base 2:")
    base2_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    base2_entry = tk.Entry(trapezoid_tab)
    base2_entry.grid(row=1, column=1, padx=10, pady=10)

    height_label = tk.Label(trapezoid_tab, text="Enter the height of the trapezoid:")
    height_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    height_entry = tk.Entry(trapezoid_tab)
    height_entry.grid(row=2, column=1, padx=10, pady=10)

    # Labels for results
    area_label = tk.Label(trapezoid_tab, text="Area: ")
    area_label.grid(row=4, column=0, columnspan=2, pady=10)

    perimeter_label = tk.Label(trapezoid_tab, text="Perimeter: ")
    perimeter_label.grid(row=5, column=0, columnspan=2, pady=10)

    error_label = tk.Label(trapezoid_tab, text="", fg="red")
    error_label.grid(row=6, column=0, columnspan=2)

    # Canvas to display the trapezoid
    canvas = tk.Canvas(trapezoid_tab, width=450, height=400, bg="white")
    canvas.grid(row=7, column=0, columnspan=2, pady=20)

    # Calculate button
    def calculate_trapezoid():
        base1 = base1_entry.get()
        base2 = base2_entry.get()
        height = height_entry.get()

        # Input validation
        if not base1 or not base2 or not height:
            error_label.config(text="Please enter all required values: Base 1, Base 2, and Height.")
            return

        try:
            base1 = float(base1)
            base2 = float(base2)
            height = float(height)
            if base1 <= 0 or base2 <= 0 or height <= 0:
                error_label.config(text="All values must be positive numbers.")
                return
        except ValueError:
            error_label.config(text="Invalid input. Please enter numeric values.")
            return

        try:
            # Retrieve JWT token
            token = token_callback()
            if not token:
                error_label.config(text="Error: No authentication token. Please log in.")
                return

            # Send API request
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                'http://localhost:5000/calculate_trapezoid',
                json={'base1': base1, 'base2': base2, 'height': height},
                headers=headers,
                timeout=5
            )
            response.raise_for_status()
            data = response.json()

            # Update labels with results
            area_label.config(text=f"Area: {data['area']:.2f} square units")
            perimeter_label.config(text=f"Perimeter: {data['perimeter']:.2f} units")
            error_label.config(text="")

            # Draw the trapezoid on the canvas
            draw_trapezoid(base1, base2, height, data['area'], data['perimeter'])

        except requests.exceptions.RequestException as e:
            error_label.config(text=f"Error: {e}")

    calculate_button = tk.Button(trapezoid_tab, text="Calculate", command=calculate_trapezoid)
    calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Function to draw the trapezoid dynamically scaled on the canvas
    def draw_trapezoid(base1, base2, height, area, perimeter):
        canvas.delete("all")  # Clear canvas

        # Scale values to fit the canvas
        scale_factor = 300 / max(base1, base2)
        scaled_base1 = base1 * scale_factor
        scaled_base2 = base2 * scale_factor
        scaled_height = height * scale_factor

        # Coordinates for trapezoid (centered)
        x1, y1 = (450 - scaled_base1) // 2, 350
        x2, y2 = x1 + scaled_base1, y1
        x3, y3 = (400 - scaled_base2) // 2, y1 - scaled_height
        x4, y4 = x3 + scaled_base2, y3

        # Draw the trapezoid
        canvas.create_polygon(x1, y1, x2, y2, x4, y4, x3, y3, outline="black", fill="lightblue", width=2)

        # Label the bases and height
        canvas.create_text((x1 + x2) / 2, y1 + 10, text=f"Base 1: {base1:.2f}", font=("Arial", 10))
        canvas.create_text((x3 + x4) / 2, y3 - 10, text=f"Base 2: {base2:.2f}", font=("Arial", 10))
        canvas.create_text((x1 + x3) / 2 - 20, (y1 + y3) / 2, text=f"Height: {height:.2f}", font=("Arial", 10))

        # Display the area and perimeter
        center_x = (x1 + x2 + x3 + x4) / 4
        center_y = (y1 + y2 + y3 + y4) / 4
        canvas.create_text(center_x, center_y, text=f"Area: {area:.2f}", font=("Arial", 12, "bold"))
        canvas.create_text(center_x, center_y + 20, text=f"Perimeter: {perimeter:.2f}", font=("Arial", 12, "bold"))

    return trapezoid_tab
