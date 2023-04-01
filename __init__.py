from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

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


@app.route('/ping') # endpoint when user pings location
def ping():
    user_loc=request.args.get('user_loc')
    request_data= request.get_json()
    loc=request_data['pingloc']


@app.route('/leaderboard')#leaderpoint endpoint
def leaderboard():
    leaderboard

if __name__ == '__main__':
    app.run(debug=True)