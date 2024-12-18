import tkinter as tk
import requests


def create_ellipse_tab(notebook, token_callback):
    """
    Creates a tab for ellipse area and perimeter calculations.
    :param notebook: The parent notebook to attach this tab.
    :param token_callback: A function to retrieve the JWT token.
    :return: The created tab.
    """
    ellipse_tab = tk.Frame(notebook)

    # Input fields for major and minor axes
    major_axis_label = tk.Label(ellipse_tab, text="Enter the major axis of the ellipse:")
    major_axis_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    major_axis_entry = tk.Entry(ellipse_tab)
    major_axis_entry.grid(row=0, column=1, padx=10, pady=10)

    minor_axis_label = tk.Label(ellipse_tab, text="Enter the minor axis of the ellipse:")
    minor_axis_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    minor_axis_entry = tk.Entry(ellipse_tab)
    minor_axis_entry.grid(row=1, column=1, padx=10, pady=10)

    # Labels for results
    area_label = tk.Label(ellipse_tab, text="Area: ")
    area_label.grid(row=3, column=0, columnspan=2, pady=10)

    perimeter_label = tk.Label(ellipse_tab, text="Perimeter: ")
    perimeter_label.grid(row=4, column=0, columnspan=2, pady=10)

    error_label = tk.Label(ellipse_tab, text="", fg="red")
    error_label.grid(row=5, column=0, columnspan=2)

    # Canvas to display the ellipse
    canvas = tk.Canvas(ellipse_tab, width=450, height=400, bg="white")
    canvas.grid(row=6, column=0, columnspan=2, pady=20)

    # Calculate button
    def calculate_ellipse():
        major_axis = major_axis_entry.get()
        minor_axis = minor_axis_entry.get()

        # Input validation
        if not major_axis or not minor_axis:
            error_label.config(text="Please enter both major and minor axis values.")
            return

        try:
            major_axis = float(major_axis)
            minor_axis = float(minor_axis)

            if major_axis <= 0 or minor_axis <= 0:
                error_label.config(text="Major and minor axes must be positive numbers.")
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
                'http://localhost:5000/calculate_ellipse',
                json={'major_axis': major_axis, 'minor_axis': minor_axis},
                headers=headers,
                timeout=5
            )
            response.raise_for_status()
            data = response.json()

            # Update labels with results
            area_label.config(text=f"Area: {data['area']:.2f} square units")
            perimeter_label.config(text=f"Perimeter: {data['perimeter']:.2f} units")
            error_label.config(text="")

            # Draw the ellipse on the canvas
            draw_ellipse(major_axis, minor_axis, data['area'], data['perimeter'])

        except requests.exceptions.RequestException as e:
            error_label.config(text=f"Error: {e}")

    calculate_button = tk.Button(ellipse_tab, text="Calculate", command=calculate_ellipse)
    calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Function to draw the ellipse dynamically scaled on the canvas
    def draw_ellipse(major_axis, minor_axis, area, perimeter):
        # Clear the canvas
        canvas.delete("all")

        # Scale the ellipse to fit within the canvas
        scale_factor = 150 / max(major_axis, minor_axis)
        scaled_major_axis = major_axis * scale_factor
        scaled_minor_axis = minor_axis * scale_factor

        # Center coordinates
        center_x, center_y = 225, 200

        # Draw the ellipse
        canvas.create_oval(
            center_x - scaled_major_axis, center_y - scaled_minor_axis,
            center_x + scaled_major_axis, center_y + scaled_minor_axis,
            outline="black", fill="lightblue", width=2
        )

        # Label the axes and results
        canvas.create_text(center_x, center_y - scaled_minor_axis - 10, text=f"Major Axis: {major_axis:.2f}", font=("Arial", 10))
        canvas.create_text(center_x, center_y + scaled_minor_axis + 10, text=f"Minor Axis: {minor_axis:.2f}", font=("Arial", 10))
        canvas.create_text(center_x, center_y, text=f"Area: {area:.2f}", font=("Arial", 12, "bold"))
        canvas.create_text(center_x, center_y + 20, text=f"Perimeter: {perimeter:.2f}", font=("Arial", 12, "bold"))

    return ellipse_tab
