from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import requests
import bcrypt
import time
import os
import math

app = Flask(__name__)

cred = credentials.Certificate('serviceAccountKey.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hackathon-ac68a-default-rtdb.firebaseio.com/'
})

db_users = db.reference('users')
db_raids = db.reference('raids')

@app.route('/')
def hello():
    return 'Home page of our python application.'

@app.route('/search') # Endpoint for parks/beaches/recreational spots 80000 meters nearby
def search():
    zip_code = request.get_json()['zip_code']
    
    # get from environment variable
    api_key = os.getenv('API_KEY')
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json"
    geocoding_params = {
        "address": zip_code, 
        "key": api_key
    }
    geocoding_response = requests.get(geocoding_url, params=geocoding_params)
    geocoding_data = geocoding_response.json()
    print(api_key)
    if len(geocoding_data["results"]) == 0:
        # Return an error message if the geocoding API does not return any results
        return jsonify({"error": "Invalid zip code"}), 400
    location = geocoding_data["results"][0]["geometry"]["location"]
    lat, lng = location["lat"], location["lng"]
    
    print(lat, lng)

    params = {
        "key": api_key,
        "location": f"{lat},{lng}",
        "radius": "80467",
        "keyword": "park|beach|recreation",
    }
    
    places = []
    response = requests.get(endpoint_url, params=params)
    print(params)
    
    data = response.json()
    for result in data["results"]:
        place = {"name": result["name"], "location": result["geometry"]["location"]}
        places.append(place)
    
    # Return the list of places as a JSON response
    return jsonify(places)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    email = email.replace(".", "-")
    password = data['password']

    # Query the Firebase database for the user
    user = db_users.child(email).get()
    print(user)

    # Check if the user exists and the password matches
    if user['password'] == bcrypt.hashpw(password.encode(),"$2b$12$vj2GaHW10eRxDcJTTTAWI.".encode()).decode():
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'User not found or password is incorrect'})
        
@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    users = db_users.get()
    # Sort the users by points
    sorted_users = sorted(users.items(), key=lambda x: x[1]['points'], reverse=True)[:10]
    return jsonify(sorted_users)

def generate_login_token():
    # Generate a random token
    token = str(time.time())
    # Hash the token using SHA-256 algorithm
    hashed_token = bcrypt.hashpw(token.encode(),"$2b$12$vj2GaHW10eRxDcJTTTAWI.".encode())
    # Return the hashed token and the original token
    return hashed_token, token
        
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    username = data['username']
    email = data['email']
    email = email.replace(".", "-")
    password = data['password']
    zip = data['zip-code']
    p = password.encode()
    # hashed_password = bcrypt.hashpw(p,"$2b$12$vj2GaHW10eRxDcJTTTAWI.".encode())
    # Store the hashed email and password in db
    user_ref = db_users.child(email)
    user_ref.set(
        {
            'email': email,
            'password': bcrypt.hashpw(p,"$2b$12$vj2GaHW10eRxDcJTTTAWI.".encode()).decode(),
            'name': name,
            'zip': zip,
            'points': 0,
            'raids': 0,
            'completed_raids': [],
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
    long = request_data['lng']
    user_key = request_data['email']
    user_key = user_key.replace(".", "-")

    user = db_users.child(user_key).get()
    db_users.child(user_key).update({'ping': f'{lat},{long}'})
    db_users.push()
    return {'status':200, 'message': 'Ping successful'}

@app.route('/raids', methods=['GET'])
def raids():
    json = request.get_json()
    user_key = json['email']
    user_key = user_key.replace(".", "-")
    user = db_users.child(user_key).get()

    ping = user['ping']
    ping = ping.split(',')
    ping_lat = ping[0]
    ping_long = ping[1]

    zip = user['zip']
    raids = db_raids.get()
    nearby_raids = []
    for raid in raids:
        raid_lat = raid['lat']
        raid_long = raid['lng']
        if distance(float(ping_lat), float(ping_long), float(raid_lat), float(raid_long)) < 0.5:
            if raid['id'] not in user['raids']:
                nearby_raids.append(raid)
    return jsonify(nearby_raids) #returns all the nearby raids based on distance 


@app.route("/finish_raid", methods=['POST'])
def finish_raid():
    data = request.get_json()
    email = data['email']
    key = email.replace(".", "-")
    user = db_users.child(key).get()
    db_users.child(key).update( #after every raid add 100 points and a +1 completion to the user's raids
        {
            'points': user['points'] + 100, 
            'raids': user['raids'] + 1,
            'completed_raids': user['completed_raids'].append(data['id'])
        }
    )
    db_users.push()
    return {'status':200, 'message': 'Raid finished successfully'}

@app.route('/create_raid', methods=['POST'])
def create_raid():
    data = request.get_json()
    name = data['name']
    lat = data['lat']
    lng = data['lng']
    time = data['datetime']
    key = data['email']
    typ = data['type']
    key = key.replace(".", "-")
    id = math.random()
    while db_raids.child(id).get() != None:
        id = math.random()
    # Store the raid in the Firebase database
    raid_ref = db_raids.child(name)
    raid_ref.set(
        {
            'name': name,
            'lat': lat,
            'lng': lng,
            'date': time,
            'created_by': key,
            'id': id,
            'type': typ
        }
    )
    return {'status':200, 'message': 'Raid created successfully'}

@app.route('/badges', methods=['GET'])
def badges():
    # get the user's data from the database
    json = request.get_json()
    user_key = json['email']
    user_key = user_key.replace(".", "-")
    user = db_users.child(user_key).get()

    points = user['points'] #retrieve user points to determine badges
    raid_count = user['raids']

    all_badges = {
        "point_based": {
            "100": "100_points",
            "500": "500_points",
            "1000": "1000_points",
        },
        "raids": {
            "1": "1_raid",
            "5": "5_raids",
            "10": "10_raids",
            "30": "30_raids",
            "50": "50_raids",
            "100": "100_raids",
        }
    }

    badges = []
    for badge in all_badges['point_based']:
        if points >= int(badge):
            badges.append(all_badges['point_based'][badge])

    for badge in all_badges['raids']:
        if raid_count >= int(badge):
            badges.append(all_badges['raids'][badge])

    return jsonify(badges)

@app.route('/me', methods=['GET']) #just a me function
def me():
    json = request.get_json()
    user_key = json['email']
    user_key = user_key.replace(".", "-")
    user = db_users.child(user_key).get()

    return jsonify(user)


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295     #Pi/180
    a = 0.5 - math.cos((lat2 - lat1) * p)/2 + math.cos(lat1 * p) * math.cos(lat2 * p) * (1 - math.cos((lon2 - lon1) * p)) / 2
    return 12742 * math.asin(math.sqrt(a)) #2*R*asin...

example_datetime_string = "2020-10-10 10:10:10" #example of a date-time string

if __name__ == '__main__':
    app.run(debug=True)
    