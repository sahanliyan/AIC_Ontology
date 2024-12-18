from flask import Flask, request, jsonify, abort
from flask_jwt_extended import JWTManager, jwt_required, create_access_token # type: ignore
from flask_limiter import Limiter  # type: ignore
from flask_limiter.util import get_remote_address # type: ignore
import rdflib
from shape_calculations import *
import redis # type: ignore

# Initialize Flask app
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'aic-ontology-ysju-jwt' 
jwt = JWTManager(app)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

# Redis for caching
try:
    cache = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    cache.ping()  # Test connection to Redis
except redis.ConnectionError as e:
    print(f"Redis connection error: {e}")
    cache = None

# Load the ontology using RDFlib
ontology_path = "OWLs/aic_ontology_on_math_shapes.owx"
g = rdflib.Graph()
try:
    g.parse(ontology_path, format="xml")
    print(f"Ontology loaded successfully from {ontology_path}.")
except Exception as e:
    print(f"Error loading ontology: {e}")
    g = None

# Helper function for input validation
def validate_request_data(required_keys, data):
    for key in required_keys:
        if key not in data:
            abort(400, f"Missing required field: {key}")

# Debugging: Print ontology classes
if g:
    print("Classes in the ontology:")
    for s, p, o in g.triples((None, rdflib.RDF.type, rdflib.OWL.Class)):
        print(f"- {s}")

# Authentication route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    # Replace with real authentication logic
    if username == "sahan" and password == "sahan":
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    else:
        abort(401, "Invalid credentials")


# Define the API route to calculate the area and perimeter
@app.route('/calculate_triangle', methods=['POST'])
@jwt_required()
@limiter.limit("10/minute")
def calculate_triangle():
    if g is None:
        abort(500, "Ontology graph is not initialized. Check the ontology file.")

    data = request.get_json()
    validate_request_data(['base', 'height'], data)
    
    base = float(data['base'])
    height = float(data['height'])

    # Check cache
    cache_key = f"triangle:{base}:{height}"
    if cache:
        cached_result = cache.get(cache_key)
        if cached_result:
            return jsonify(eval(cached_result))  # Return cached result

    # Calculate area and perimeter
    try:
        area, perimeter = calculate_triangle_area_and_perimeter(base, height)
    except Exception as e:
        abort(500, f"Error calculating triangle area and perimeter: {e}")

    # Update ontology
    try:
        triangle_uri = rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/triangle1")
        g.add((triangle_uri, rdflib.RDF.type, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/Triangle")))
        g.add((triangle_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasBase"), rdflib.Literal(base)))
        g.add((triangle_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasHeight"), rdflib.Literal(height)))
        g.add((triangle_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasArea"), rdflib.Literal(area)))
        g.add((triangle_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasPerimeter"), rdflib.Literal(perimeter)))

        # Save updated ontology
        g.serialize(destination="OWLs/updated_Triangle.owl", format="xml")
    except Exception as e:
        abort(500, f"Error updating ontology: {e}")

    # Cache result
    result = {'area': area, 'perimeter': perimeter}
    if cache:
        cache.set(cache_key, str(result), ex=3600)  # Cache for 1 hour

    return jsonify(result)


# Define the API route to calculate the area and perimeter of a rectangle
@app.route('/calculate_rectangle', methods=['POST'])
def calculate_rectangle():
    data = request.get_json()
    
    # Get the length and width from the POST request
    length = float(data['length'])
    width = float(data['width'])
    
    # Calculate area and perimeter using the function
    area, perimeter = calculate_rectangle_area_and_perimeter(length, width)

    # Check if rectangle1 exists, otherwise create it
    rectangle_uri = rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/rectangle1")
    
    # Add the rectangle1 instance if it doesn't exist already
    g.add((rectangle_uri, rdflib.RDF.type, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/Rectangle")))
    
    # Add the data properties (hasLength, hasWidth, hasArea, hasPerimeter)
    g.add((rectangle_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasLength"), rdflib.Literal(length)))
    g.add((rectangle_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasWidth"), rdflib.Literal(width)))
    g.add((rectangle_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasArea"), rdflib.Literal(area)))
    g.add((rectangle_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasPerimeter"), rdflib.Literal(perimeter)))

    # Save the updated ontology to a new file
    g.serialize(destination="OWLs/updated_Rectangle.owl", format="xml")

    # Return the calculated area and perimeter as a response
    return jsonify({'area': area, 'perimeter': perimeter})



# Define the API route to calculate the area and perimeter (circumference) of a circle
@app.route('/calculate_circle', methods=['POST'])
def calculate_circle():
    data = request.get_json()

    # Get the radius from the POST request
    radius = float(data['radius'])

    # Calculate area and perimeter using the function
    area, perimeter = calculate_circle_area_and_perimeter(radius)

    # Check if circle1 exists, otherwise create it
    circle_uri = rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/circle1")

    # Add the circle1 instance if it doesn't exist already
    g.add((circle_uri, rdflib.RDF.type, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/Circle")))

    # Add the data properties (hasRadius, hasArea, hasPerimeter)
    g.add((circle_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasRadius"), rdflib.Literal(radius)))
    g.add((circle_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasArea"), rdflib.Literal(area)))
    g.add((circle_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasPerimeter"), rdflib.Literal(perimeter)))

    # Save the updated ontology to a new file
    g.serialize(destination="OWLs/updated_Circle.owl", format="xml")

    # Return the calculated area and perimeter as a response
    return jsonify({'area': area, 'perimeter': perimeter})



# Ellipse API Route
@app.route('/calculate_ellipse', methods=['POST'])
def calculate_ellipse():
    data = request.get_json()
    major_axis = float(data['major_axis'])
    minor_axis = float(data['minor_axis'])
    
    # Calculate the area and perimeter using the function
    area, perimeter = calculate_ellipse_area_and_perimeter(major_axis, minor_axis)

    # Update the ontology with the calculated values
    ellipse_uri = rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/ellipse1")
    g.add((ellipse_uri, rdflib.RDF.type, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/Ellipse")))
    g.add((ellipse_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasMajorAxis"), rdflib.Literal(major_axis)))
    g.add((ellipse_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasMinorAxis"), rdflib.Literal(minor_axis)))
    g.add((ellipse_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasArea"), rdflib.Literal(area)))
    g.add((ellipse_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasPerimeter"), rdflib.Literal(perimeter)))
    
    # Serialize the updated ontology to a new file
    g.serialize(destination="OWLs/updated_Ellipse.owl", format="xml")

    return jsonify({'area': area, 'perimeter': perimeter})



# API route to calculate square area and perimeter
@app.route('/calculate_square', methods=['POST'])
def calculate_square():
    data = request.get_json()

    # Get the side length from the POST request
    side = float(data['side'])

    # Calculate area and perimeter using the function
    area, perimeter = calculate_square_area_and_perimeter(side)

    # Now we need to update the square instance in the ontology
    square_uri = rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/square1")

    # Add the square instance if it doesn't exist
    g.add((square_uri, rdflib.RDF.type, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/Square")))

    # Add the data properties (hasSide, hasArea, hasPerimeter)
    g.add((square_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasSide"), rdflib.Literal(side)))
    g.add((square_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasArea"), rdflib.Literal(area)))
    g.add((square_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasPerimeter"), rdflib.Literal(perimeter)))

    # Save the updated ontology to a new file
    g.serialize(destination="OWLs/updated_Square.owl", format="xml")

    # Return the calculated area and perimeter as a response
    return jsonify({'area': area, 'perimeter': perimeter})



# API route to calculate pentagon area and perimeter
@app.route('/calculate_pentagon', methods=['POST'])
def calculate_pentagon():
    data = request.get_json()

    # Get the side length from the POST request
    side = float(data['side'])

    # Calculate area and perimeter using the function
    area, perimeter = calculate_pentagon_area_and_perimeter(side)

    # Now we need to update the pentagon instance in the ontology
    pentagon_uri = rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/pentagon1")

    # Add the pentagon instance if it doesn't exist
    g.add((pentagon_uri, rdflib.RDF.type, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/Pentagon")))

    # Add the data properties (hasSide, hasArea, hasPerimeter)
    g.add((pentagon_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasSide"), rdflib.Literal(side)))
    g.add((pentagon_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasArea"), rdflib.Literal(area)))
    g.add((pentagon_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasPerimeter"), rdflib.Literal(perimeter)))

    # Save the updated ontology to a new file
    g.serialize(destination="OWLs/updated_Pentagon.owl", format="xml")

    # Return the calculated area and perimeter as a response
    return jsonify({'area': area, 'perimeter': perimeter})



# API route to calculate rhombus area and perimeter
@app.route('/calculate_rhombus', methods=['POST'])
def calculate_rhombus():
    data = request.get_json()

    # Get the diagonal lengths from the POST request
    diagonal1 = float(data['diagonal1'])
    diagonal2 = float(data['diagonal2'])

    # Calculate area and perimeter using the function
    area, perimeter = calculate_rhombus_area_and_perimeter(diagonal1, diagonal2)

    # Now we need to update the rhombus instance in the ontology
    rhombus_uri = rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/rhombus1")

    # Add the rhombus instance if it doesn't exist
    g.add((rhombus_uri, rdflib.RDF.type, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/Rhombus")))

    # Add the data properties (hasDiagonal1, hasDiagonal2, hasArea, hasPerimeter)
    g.add((rhombus_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasDiagonal1"), rdflib.Literal(diagonal1)))
    g.add((rhombus_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasDiagonal2"), rdflib.Literal(diagonal2)))
    g.add((rhombus_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasArea"), rdflib.Literal(area)))
    g.add((rhombus_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasPerimeter"), rdflib.Literal(perimeter)))

    # Save the updated ontology to a new file
    g.serialize(destination="OWLs/updated_Rhombus.owl", format="xml")

    # Return the calculated area and perimeter as a response
    return jsonify({'area': area, 'perimeter': perimeter})


# API route to calculate trapezoid area and perimeter
@app.route('/calculate_trapezoid', methods=['POST'])
def calculate_trapezoid():
    data = request.get_json()

    # Get the base lengths and height from the POST request
    base1 = float(data['base1'])
    base2 = float(data['base2'])
    height = float(data['height'])

    # Calculate area and perimeter using the function
    area, perimeter = calculate_trapezoid_area_and_perimeter(base1, base2, height)

    # Now we need to update the trapezoid instance in the ontology
    trapezoid_uri = rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/trapezoid1")

    # Add the trapezoid instance if it doesn't exist
    g.add((trapezoid_uri, rdflib.RDF.type, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/Trapezoid")))

    # Add the data properties (hasBase1, hasBase2, hasHeight, hasArea, hasPerimeter)
    g.add((trapezoid_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasBase1"), rdflib.Literal(base1)))
    g.add((trapezoid_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasBase2"), rdflib.Literal(base2)))
    g.add((trapezoid_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasHeight"), rdflib.Literal(height)))
    g.add((trapezoid_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasArea"), rdflib.Literal(area)))
    g.add((trapezoid_uri, rdflib.URIRef("http://www.semanticweb.org/dell/ontologies/2024/11/aic_final_ontology/hasPerimeter"), rdflib.Literal(perimeter)))

    # Save the updated ontology to a new file
    g.serialize(destination="OWLs/updated_Trapezoid.owl", format="xml")

    # Return the calculated area and perimeter as a response
    return jsonify({'area': area, 'perimeter': perimeter})


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
