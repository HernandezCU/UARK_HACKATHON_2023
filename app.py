from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import requests
import bcrypt
import time

app = Flask(__name__)

cred = credentials.Certificate('serviceAccountKey.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hackathon-ac68a-default-rtdb.firebaseio.com/'
})

ref = db.reference('users')

@app.route('/')
def hello():
    return 'Home page of our python application.'

@app.route('/search') # Endpoint for whenever user searches for a place
def search():
    # Get the zip code from the request parameters
    zip_code = request.get_json()['zip_code']
    
    # Set up API key and endpoint URL
    api_key = "AIzaSyAmvzpQ5kva14bp16Q82uJ2DAHqsrI7Ltc"
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    # Get the latitude and longitude of the zip code using the Google Maps Geocoding API
    geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json"
    geocoding_params = {
        "address": zip_code, 
        "key": api_key
    }
    geocoding_response = requests.get(geocoding_url, params=geocoding_params)
    geocoding_data = geocoding_response.json()
    if len(geocoding_data["results"]) == 0:
        # Return an error message if the geocoding API does not return any results
        return jsonify({"error": "Invalid zip code"}), 400
    location = geocoding_data["results"][0]["geometry"]["location"]
    lat, lng = location["lat"], location["lng"]
    
    print(lat, lng)

    # Specify the location and keyword parameters for the API request
    params = {
        "key": api_key,
        "location": f"{lat},{lng}",
        "radius": "80467",
        "keyword": "park|beach|recreation",
    }
    
    places = []
    # Make the API request
    response = requests.get(endpoint_url, params=params)
    print(params)
    
    # Parse the response data as JSON
    data = response.json()
    # Extract the name and location of each place and store them in a list
    for result in data["results"]:
        place = {"name": result["name"], "location": result["geometry"]["location"]}
        places.append(place)
    
    # Return the list of places as a JSON response
    return jsonify(places)

@app.route('/login', methods=['GET'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    # Query the Firebase database for the user
    users = ref.order_by_child('email').equal_to(email).get()

    # Check if the user exists and the password matches
    for user_id, user in users.items():
        if user['password'] == password:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'User not found or password is incorrect'})
        
        
@app.route('/leaderboard_add', methods=['POST'])
def leaderboard():
    data = request.get_json()
    username = data['username']
    points = data['points']
    # specify the database reference to the users node
    users_ref = db.reference('scores')
    # push a new child node with a unique ID generated by Firebase
    new_user_ref = users_ref.push()
    # set the child node with the username and points data
    new_user_ref.set({
        'username': username,
        'points': points
    })
    # return a success message
    return {'message': 'User data added to database'}

        
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    username = data['username']
    email = data['email']
    password = data['password']
    zip = data['zip-code']
    points = 0
    # Hash the email and password using SHA-256 algorithm
    p = password.encode()
    # hashed_password = bcrypt.hashpw(p,"$2b$12$vj2GaHW10eRxDcJTTTAWI.".encode())
    # Store the hashed email and password in the Firebase database
    user_ref = ref.child(email)
    user_ref.set(
        {
            'email': email,
            'password': password,
            'name': name,
            'zip': zip,
            'points': points,
            'username': username,
            'ping': ''
        }
    )
    return {'status':200, 'message': 'Registration successful'}
    
@app.route('/ping',methods=['POST', 'GET']) # endpoint when user pings location
def ping():
    # user_lat=request.args.get('lat')
    # user_long=request.args.get('lng')
    request_data= request.get_json()
    lat = request_data['lat']
    long = request_data['long']
        
    # loc=str(loc)
    # user_ref=ref.child(loc)
    # user_ref.push.set(loc)
    return {'status':200, 'message': 'Ping successful'}


if __name__ == '__main__':
    app.run(debug=True)