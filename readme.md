# GreenCityGo - University of Arkansas 2023 Hackathon

- Domain: greencitygo.net
- Swift GitHub Repo: https://github.com/HernandezCU/TrashGo

# Description

GreenCityGo is a mobile application that allows users to gain points and socialize through attending "raids" which are social environmental helpful events. This solves various
environmental problems such as sustaining a clean environment as well as incentivizing people to contribute. Through the game aspects of the application, users are motivated to
return to the app for a daily usage. There is a badge/level system to allow users to feel recognized and show off to their friends.

# Endpoint Functionalities
/search: This endpoint searches for parks, beaches, and recreational spots near a given zip code. It uses the Google Maps API to perform this search. The latitude and longitude of the zip code are obtained using the Google Maps Geocoding API. The endpoint returns a list of places as a JSON response. This endpoint expects a JSON payload with a single attribute, zip_code, which is a string representing the user's zip code. Example:

```json
{
    "zip_code": "90210"
}   
```

/login: This endpoint logs in a user by verifying their email and password. It checks if the user exists in the Firebase database and if the password matches the hashed password stored in the database. If the user is authenticated, it returns a JSON response with a "success" message. Otherwise, it returns a "User not found or password is incorrect" error message. This endpoint expects a JSON payload with two attributes, email and password, both of which are strings representing the user's email and password, respectively. Example:

```json
{
    "email": "example@email.com",
    "password": "password123"
}
```

/leaderboard: This endpoint retrieves a list of users from the Firebase database and sorts them by points in descending order. It returns the top 10 users as a JSON response.

/register: This endpoint registers a new user by storing their name, username, email, password, zip code, and points in the Firebase database. The password is hashed using the bcrypt library. If the registration is successful, it returns a JSON response with a "status" code of 200 and a "message" of "Registration successful". This endpoint expects a JSON payload with several attributes representing the user's information, including name, username, email, password, and zip-code. All of these attributes are strings except for zip-code, which is an integer. Example:

```json
{
    "name": "John Doe",
    "username": "jdoe",
    "email": "jdoe@example.com",
    "password": "password123",
    "zip-code": 90210
}
```

/ping: This endpoint updates a user's location by storing their latitude and longitude in the Firebase database. It takes the user's latitude, longitude, and key as inputs and updates the "ping" field in the user's data. If the update is successful, it returns a JSON response with a "status" code of 200 and a "message" of "Ping successful". This endpoint expects a JSON payload with three attributes, email, lat, and lng, representing the user's email and current latitude and longitude, respectively. Both lat and lng are floats. Example:

```json
{
    "email": "jdoe@example.com",
    "lat": 34.0522,
    "lng": -118.2437
}
```

/raids: This endpoint retrieves data about raids from the Firebase database. It returns a JSON response with the raid data. The code does not provide details about how the raid data is stored in the database. This endpoint expects a JSON payload with a single attribute, email, which is a string representing the user's email. Example:

```json
{
    "email": "jdoe@example.com"
}
```

# Tech Stack
- Google Maps API
- Flask
- Firebase
- Deta (for hosting)

# Credits
- Carlos Hernandez: https://github.com/HernandezCU
- Roberto Aguero: https://github.com/robPTY
- Matthew Anderson: https://github.com/notmatthewanderson8
- Carlos Borjes:
- Alexis Guzman: 