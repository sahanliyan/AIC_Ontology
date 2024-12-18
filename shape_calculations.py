import math

# Define a function to calculate the area and perimeter of a triangle
def calculate_triangle_area_and_perimeter(base, height):
    area = 0.5 * base * height
    # Calculate the hypotenuse using Pythagoras' theorem
    hypotenuse = math.sqrt(base**2 + height**2)
    perimeter = base + height + hypotenuse
    return area, perimeter

# Function to calculate the area and perimeter of the square
def calculate_square_area_and_perimeter(side):
    area = side ** 2  # Area = side^2
    perimeter = 4 * side  # Perimeter = 4 * side
    return area, perimeter


# Define a function to calculate the area and perimeter of a rectangle
def calculate_rectangle_area_and_perimeter(length, width):
    area = length * width
    perimeter = 2 * (length + width)
    return area, perimeter


# Function to calculate the area and perimeter of the pentagon
def calculate_pentagon_area_and_perimeter(side):
    # Formula for the area of a regular pentagon
    area = (5 * side**2) / (4 * math.tan(math.pi / 5))
    # Formula for the perimeter of a regular pentagon
    perimeter = 5 * side
    return area, perimeter


# Define a function to calculate the area and perimeter (circumference) of a circle
def calculate_circle_area_and_perimeter(radius):
    area = math.pi * (radius ** 2)  # Area = π * r²
    perimeter = 2 * math.pi * radius  # Perimeter (Circumference) = 2 * π * r
    return area, perimeter


# Ellipse Calculation Function
def calculate_ellipse_area_and_perimeter(major_axis, minor_axis):
    # Area = pi * a * b (a = major axis, b = minor axis)
    area = math.pi * major_axis * minor_axis
    
    # Perimeter approximation for ellipse
    perimeter = math.pi * (3 * (major_axis + minor_axis) - math.sqrt((3 * major_axis + minor_axis) * (major_axis + 3 * minor_axis)))
    
    return area, perimeter


# Function to calculate the area and perimeter of the rhombus
def calculate_rhombus_area_and_perimeter(diagonal1, diagonal2):
    # Formula for the area of a rhombus
    area = (diagonal1 * diagonal2) / 2
    # Formula for the perimeter of a rhombus (all sides are equal)
    side = math.sqrt((diagonal1 / 2) ** 2 + (diagonal2 / 2) ** 2)
    perimeter = 4 * side
    return area, perimeter


# Function to calculate the area and perimeter of the trapezoid
def calculate_trapezoid_area_and_perimeter(base1, base2, height):
    # Formula for the area of a trapezoid
    area = ((base1 + base2) * height) / 2
    # Formula for the perimeter of a trapezoid (using Pythagoras' theorem)
    side = math.sqrt(((base2 - base1) / 2) ** 2 + height ** 2)
    perimeter = base1 + base2 + 2 * side
    return area, perimeter