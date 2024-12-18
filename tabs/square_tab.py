import tkinter as tk
import requests

def create_square_tab(notebook, token_callback):
    """
    Creates a tab for square area and perimeter calculations.
    :param notebook: The parent notebook to attach this tab.
    :param token_callback: A function to retrieve the JWT token.
    :return: The created tab.
    """
    square_tab = tk.Frame(notebook)

    # Input fields for side length
    side_label = tk.Label(square_tab, text="Enter the side length of the square:")
    side_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    side_entry = tk.Entry(square_tab)
    side_entry.grid(row=0, column=1, padx=10, pady=10)

    # Labels for results
    area_label = tk.Label(square_tab, text="Area: ")
    area_label.grid(row=3, column=0, columnspan=2, pady=10)

    perimeter_label = tk.Label(square_tab, text="Perimeter: ")
    perimeter_label.grid(row=4, column=0, columnspan=2, pady=10)

    error_label = tk.Label(square_tab, text="", fg="red")
    error_label.grid(row=5, column=0, columnspan=2)

    # Canvas to display the square
    canvas = tk.Canvas(square_tab, width=450, height=400, bg="white")
    canvas.grid(row=6, column=0, columnspan=2, pady=20)

    # Calculate button
    def calculate_square():
        side = side_entry.get()

        # Input validation
        if not side:
            error_label.config(text="Please enter the side length of the square.")
            return

        try:
            side = float(side)
            if side <= 0:
                error_label.config(text="Side length must be a positive number.")
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

            # Send API request
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                'http://localhost:5000/calculate_square',
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

            # Draw the square on the canvas
            draw_square(side, data['area'], data['perimeter'])

        except requests.exceptions.RequestException as e:
            error_label.config(text=f"Error: {e}")

    calculate_button = tk.Button(square_tab, text="Calculate", command=calculate_square)
    calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Function to draw the square dynamically scaled on the canvas
    def draw_square(side, area, perimeter):
        canvas.delete("all")  # Clear the canvas

        # Scale the square to fit the canvas
        scale_factor = 300 / side
        scaled_side = side * scale_factor

        # Coordinates for the square (centered)
        top_left_x = (450 - scaled_side) // 2
        top_left_y = (400 - scaled_side) // 2

        # Draw the square
        canvas.create_rectangle(
            top_left_x, top_left_y,
            top_left_x + scaled_side, top_left_y + scaled_side,
            outline="black", fill="lightblue", width=2
        )

        # Label the side length
        canvas.create_text(top_left_x + scaled_side / 2, top_left_y - 10, text=f"Side: {side:.2f}", font=("Arial", 10))

        # Display the area and perimeter in the center
        canvas.create_text(top_left_x + scaled_side / 2, top_left_y + scaled_side / 2, text=f"Area: {area:.2f}", font=("Arial", 12, "bold"))
        canvas.create_text(top_left_x + scaled_side / 2, top_left_y + scaled_side / 2 + 20, text=f"Perimeter: {perimeter:.2f}", font=("Arial", 12, "bold"))

    return square_tab
