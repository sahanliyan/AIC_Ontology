import tkinter as tk
from tkinter import ttk
from tabs.triangle_tab import create_triangle_tab

# Import tabs
from tabs.home_tab import create_home_tab
from tabs.triangle_tab import create_triangle_tab
from tabs.circle_tab import create_circle_tab
from tabs.rectangle_tab import create_rectangle_tab
from tabs.ellipse_tab import create_ellipse_tab
from tabs.square_tab import create_square_tab
from tabs.pentagon_tab import create_pentagon_tab
from tabs.rhombus_tab import create_rhombus_tab
from tabs.trapezoid_tab import create_trapezoid_tab

# Global token to be shared across tabs
global_token = None

def set_global_token(token):
    global global_token
    global_token = token

def get_global_token():
    return global_token


# Main UI setup
def create_main_ui():
    root = tk.Tk()
    root.title("Geometric Shape Calculator")

    # Create a Notebook (Tabs container)
    notebook = ttk.Notebook(root)
    notebook.grid(row=0, column=0, padx=10, pady=10)

    # Home tab for login
    home_tab = create_home_tab(notebook, set_global_token)
    notebook.add(home_tab, text="Home")

    # Add remaining tabs
    triangle_tab = create_triangle_tab(notebook, get_global_token)
    square_tab = create_square_tab(notebook, get_global_token)
    rectangle_tab = create_rectangle_tab(notebook, get_global_token)
    pentagon_tab = create_pentagon_tab(notebook, get_global_token)
    rhombus_tab = create_rhombus_tab(notebook, get_global_token)
    trapezoid_tab = create_trapezoid_tab(notebook, get_global_token)
    circle_tab = create_circle_tab(notebook, get_global_token)
    ellipse_tab = create_ellipse_tab(notebook, get_global_token)
    

    # Add tabs to the notebook
    notebook.add(triangle_tab, text="Triangle")
    notebook.add(square_tab, text="Square")
    notebook.add(rectangle_tab, text="Rectangle")
    notebook.add(pentagon_tab, text="Pentagon")
    notebook.add(rhombus_tab, text="Rhombus")
    notebook.add(trapezoid_tab, text="Trapezoid")
    notebook.add(ellipse_tab, text="Ellipse")
    notebook.add(circle_tab, text="Circle")

    root.mainloop()


# Run the main UI
if __name__ == "__main__":
    create_main_ui()
