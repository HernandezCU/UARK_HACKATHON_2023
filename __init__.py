from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import requests
import hashlib
import bcrypt

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
    location = request.args.get('location')
    radius = request.args.get('radius', default=75)
    type = request.args.get('type', default='park')
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {'location': location, 'radius': radius, 'type': type, 'key': 'YOUR_API_KEY'}
    response = requests.get(url, params=params)
    data = response.json()
    if data['status'] == 'OK':
        places = []
        for result in data['results']:
            places.append({'name': result['name'], 'address': result['vicinity'], 'rating': result.get('rating', '-')})
        return jsonify({'results': places})
    else:
        return jsonify({'error': 'Unable to search for places'})

@app.route('/check_user', methods=['GET'])
def check_user():
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
    return 'Registration successful'
    
@app.route('/ping') # endpoint when user pings location
def ping():
    user_loc=request.args.get('user_loc')


if __name__ == '__main__':
    app.run(debug=True)