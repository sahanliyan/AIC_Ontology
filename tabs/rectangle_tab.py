import tkinter as tk
import requests


def create_rectangle_tab(notebook, token_callback):
    """
    Creates a tab for rectangle area and perimeter calculations.
    :param notebook: The parent notebook to attach this tab.
    :param token_callback: A function to retrieve the JWT token.
    :return: The created tab.
    """
    rectangle_tab = tk.Frame(notebook)

    # Input fields for length and width
    length_label = tk.Label(rectangle_tab, text="Enter the length of the rectangle:")
    length_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    length_entry = tk.Entry(rectangle_tab)
    length_entry.grid(row=0, column=1, padx=10, pady=10)

    width_label = tk.Label(rectangle_tab, text="Enter the width of the rectangle:")
    width_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    width_entry = tk.Entry(rectangle_tab)
    width_entry.grid(row=1, column=1, padx=10, pady=10)

    # Labels for results
    area_label = tk.Label(rectangle_tab, text="Area: ")
    area_label.grid(row=3, column=0, columnspan=2, pady=10)

    perimeter_label = tk.Label(rectangle_tab, text="Perimeter: ")
    perimeter_label.grid(row=4, column=0, columnspan=2, pady=10)

    error_label = tk.Label(rectangle_tab, text="", fg="red")
    error_label.grid(row=5, column=0, columnspan=2)

    # Canvas to display the rectangle
    canvas = tk.Canvas(rectangle_tab, width=450, height=400, bg="white")
    canvas.grid(row=6, column=0, columnspan=2, pady=20)

    # Calculate button
    def calculate_rectangle():
        length = length_entry.get()
        width = width_entry.get()

        # Input validation
        if not length or not width:
            error_label.config(text="Please enter both length and width.")
            return

        try:
            length = float(length)
            width = float(width)

            if length <= 0 or width <= 0:
                error_label.config(text="Length and width must be positive numbers.")
                return

        except ValueError:
            error_label.config(text="Invalid input. Please enter numeric values for length and width.")
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
                'http://localhost:5000/calculate_rectangle',
                json={'length': length, 'width': width},
                headers=headers,
                timeout=5
            )
            response.raise_for_status()
            data = response.json()

            # Update labels with results
            area_label.config(text=f"Area: {data['area']:.2f} square units")
            perimeter_label.config(text=f"Perimeter: {data['perimeter']:.2f} units")
            error_label.config(text="")

            # Draw the rectangle on the canvas
            draw_rectangle(length, width, data['area'], data['perimeter'])

        except requests.exceptions.RequestException as e:
            error_label.config(text=f"Error: {e}")

    calculate_button = tk.Button(rectangle_tab, text="Calculate", command=calculate_rectangle)
    calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Function to draw the rectangle dynamically scaled on the canvas
    def draw_rectangle(length, width, area, perimeter):
        # Clear the canvas before drawing
        canvas.delete("all")

        # Scale the rectangle to fit the canvas
        scale_factor = 300 / max(length, width)
        scaled_length = length * scale_factor
        scaled_width = width * scale_factor

        # Coordinates for the rectangle
        x1, y1 = 225-scaled_length/2, 350
        x2, y2 = x1 + scaled_length, y1
        x3, y3 = x1, y1 - scaled_width
        x4, y4 = x1 + scaled_length, y1 - scaled_width

        # Draw the rectangle
        canvas.create_rectangle(x1, y1, x2, y3, outline="black", fill="lightblue", width=2)

        # Label the dimensions
        canvas.create_text((x1 + x2) / 2, y1 + 10, text=f"Length: {length:.2f}", font=("Arial", 10))
        canvas.create_text((x1 + x3) / 2 - 10, (y3 + y1) / 2, text=f"Width: {width:.2f}", font=("Arial", 10))

        # Display the area and perimeter in the center
        canvas.create_text((x1 + x2) / 2, (y1 + y3) / 2, text=f"Area: {area:.2f}", font=("Arial", 12, "bold"))
        canvas.create_text((x1 + x2) / 2, (y1 + y3) / 2 + 20, text=f"Perimeter: {perimeter:.2f}", font=("Arial", 12, "bold"))

    return rectangle_tab
