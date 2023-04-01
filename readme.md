# GreenCityGo - University of Arkansas 2023 Hackathon

# Endpoint Functionalities
/search: This endpoint searches for parks, beaches, and recreational spots near a given zip code. It uses the Google Maps API to perform this search. The latitude and longitude of the zip code are obtained using the Google Maps Geocoding API. The endpoint returns a list of places as a JSON response.

/login: This endpoint logs in a user by verifying their email and password. It checks if the user exists in the Firebase database and if the password matches the hashed password stored in the database. If the user is authenticated, it returns a JSON response with a "success" message. Otherwise, it returns a "User not found or password is incorrect" error message.

/leaderboard: This endpoint retrieves a list of users from the Firebase database and sorts them by points in descending order. It returns the top 10 users as a JSON response.

/register: This endpoint registers a new user by storing their name, username, email, password, zip code, and points in the Firebase database. The password is hashed using the bcrypt library. If the registration is successful, it returns a JSON response with a "status" code of 200 and a "message" of "Registration successful".

/ping: This endpoint updates a user's location by storing their latitude and longitude in the Firebase database. It takes the user's latitude, longitude, and key as inputs and updates the "ping" field in the user's data. If the update is successful, it returns a JSON response with a "status" code of 200 and a "message" of "Ping successful".

/raids: This endpoint retrieves data about raids from the Firebase database. It returns a JSON response with the raid data. The code does not provide details about how the raid data is stored in the database.

# Tech Stack
- Google Maps API
- Flask
- Firebase
- Deta (for hosting)