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

if __name__ == '__main__':
    app.run(debug=True)