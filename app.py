from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Function to load cars from JSON file
def load_cars():
    """Load car data from cars.json, return empty list if file issues occur."""
    try:
        with open('cars.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return empty list if file not found
    except json.JSONDecodeError:
        return []  # Return empty list if JSON is invalid

# bubble sort function for sorting cars
def bubble_sort_cars(cars, key, reverse=False):
    #sort the cars list using bubble sort based on a key (price or year).
    n = len(cars)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            # compare the adjacent elements based on the specified key
            if not reverse:
                # Ascending order
                if cars[j][key] > cars[j + 1][key]:
                    cars[j], cars[j + 1] = cars[j + 1], cars[j]
                    swapped = True
            else:
                # Descending order
                if cars[j][key] < cars[j + 1][key]:
                    cars[j], cars[j + 1] = cars[j + 1], cars[j]
                    swapped = True
        # If no swaps occurred, the list is already sorted
        if not swapped:
            break
    return cars

# Route for the homepage
@app.route('/')
def home():
    """Display homepage with a list of cars. search and sort cars"""
    # Get search query and sort option from URL parameters
    search_query = request.args.get('search', '').lower()
    sort_option = request.args.get('sort', 'price_asc')
    
    # Load cars from JSON
    cars = load_cars()
    
    # Filter cars based on search query
    if search_query:
        cars = [car for car in cars if search_query in car['make'].lower() or search_query in car['model'].lower()]
    
    # Sort cars based on sort option
    if sort_option == 'price_asc':
        cars = bubble_sort_cars(cars, 'price', reverse=False)
    elif sort_option == 'price_desc':
        cars = bubble_sort_cars(cars, 'price', reverse=True)
    elif sort_option == 'year_asc':
        cars = bubble_sort_cars(cars, 'year', reverse=False)
    elif sort_option == 'year_desc':
        cars = bubble_sort_cars(cars, 'year', reverse=True)
    
    # Render the home template with the filtered and sorted cars
    return render_template('home.html', cars=cars)

# Route for car details page
@app.route('/car/<int:car_id>')
def car_details(car_id):
    """Display details of a specific car based on its id."""
    cars = load_cars()
    car = next((car for car in cars if car['id'] == car_id), None)
    if car:
        return render_template('details.html', car=car)
    else:
        # Return 404 if car not found
        return "Car not found", 404
    

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 error with a custom page"""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)