import tkinter as tk
import requests


def create_rhombus_tab(notebook, token_callback):
    """
    Creates a tab for rhombus area and perimeter calculations.
    :param notebook: The parent notebook to attach this tab.
    :param token_callback: A function to retrieve the JWT token.
    :return: The created tab.
    """
    rhombus_tab = tk.Frame(notebook)

    # Input fields for diagonal lengths
    diagonal1_label = tk.Label(rhombus_tab, text="Enter the length of diagonal 1:")
    diagonal1_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    diagonal1_entry = tk.Entry(rhombus_tab)
    diagonal1_entry.grid(row=0, column=1, padx=10, pady=10)

    diagonal2_label = tk.Label(rhombus_tab, text="Enter the length of diagonal 2:")
    diagonal2_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    diagonal2_entry = tk.Entry(rhombus_tab)
    diagonal2_entry.grid(row=1, column=1, padx=10, pady=10)

    # Labels for results
    area_label = tk.Label(rhombus_tab, text="Area: ")
    area_label.grid(row=3, column=0, columnspan=2, pady=10)

    perimeter_label = tk.Label(rhombus_tab, text="Perimeter: ")
    perimeter_label.grid(row=4, column=0, columnspan=2, pady=10)

    error_label = tk.Label(rhombus_tab, text="", fg="red")
    error_label.grid(row=5, column=0, columnspan=2)

    # Canvas to display the rhombus
    canvas = tk.Canvas(rhombus_tab, width=450, height=400, bg="white")
    canvas.grid(row=6, column=0, columnspan=2, pady=20)

    # Calculate button
    def calculate_rhombus():
        diagonal1 = diagonal1_entry.get()
        diagonal2 = diagonal2_entry.get()

        # Input validation
        if not diagonal1 or not diagonal2:
            error_label.config(text="Please enter both diagonal lengths.")
            return

        try:
            diagonal1 = float(diagonal1)
            diagonal2 = float(diagonal2)

            if diagonal1 <= 0 or diagonal2 <= 0:
                error_label.config(text="Diagonals must be positive numbers.")
                return

        except ValueError:
            error_label.config(text="Invalid input. Please enter numeric values for diagonals.")
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
                'http://localhost:5000/calculate_rhombus',
                json={'diagonal1': diagonal1, 'diagonal2': diagonal2},
                headers=headers,
                timeout=5
            )
            response.raise_for_status()
            data = response.json()

            # Update labels with results
            area_label.config(text=f"Area: {data['area']:.2f} square units")
            perimeter_label.config(text=f"Perimeter: {data['perimeter']:.2f} units")
            error_label.config(text="")

            # Draw the rhombus on the canvas
            draw_rhombus(diagonal1, diagonal2, data['area'], data['perimeter'])

        except requests.exceptions.RequestException as e:
            error_label.config(text=f"Error: {e}")

    calculate_button = tk.Button(rhombus_tab, text="Calculate", command=calculate_rhombus)
    calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Function to draw the rhombus dynamically scaled on the canvas
    def draw_rhombus(diagonal1, diagonal2, area, perimeter):
        canvas.delete("all")  # Clear the canvas

        # Scale the rhombus to fit the canvas
        scale_factor = 200 / max(diagonal1, diagonal2)
        scaled_d1 = diagonal1 * scale_factor
        scaled_d2 = diagonal2 * scale_factor

        # Coordinates for the rhombus (centered)
        center_x, center_y = 225, 200
        points = [
            (center_x - scaled_d1 / 2, center_y),           # Left vertex
            (center_x, center_y - scaled_d2 / 2),           # Top vertex
            (center_x + scaled_d1 / 2, center_y),           # Right vertex
            (center_x, center_y + scaled_d2 / 2)            # Bottom vertex
        ]

        # Draw the rhombus
        canvas.create_polygon(points, outline="black", fill="lightblue", width=2)

        # Label the diagonals
        canvas.create_text(center_x, center_y - scaled_d2 / 2 - 10, text=f"Diagonal 2: {diagonal2:.2f}", font=("Arial", 10))
        canvas.create_text(center_x, center_y + scaled_d2 / 2 + 10, text=f"Diagonal 2: {diagonal2:.2f}", font=("Arial", 10))
        canvas.create_text(center_x - scaled_d1 / 2 - 20, center_y, text=f"Diagonal 1: {diagonal1:.2f}", font=("Arial", 10))

        # Display the area and perimeter
        canvas.create_text(center_x, center_y, text=f"Area: {area:.2f}", font=("Arial", 12, "bold"))
        canvas.create_text(center_x, center_y + 20, text=f"Perimeter: {perimeter:.2f}", font=("Arial", 12, "bold"))

    return rhombus_tab
