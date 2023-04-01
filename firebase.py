import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('serviceAccountKey.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hackathon-ac68a-default-rtdb.firebaseio.com/'
})

ref = db.reference('users')

new_user_ref = ref.push()
new_user_ref.set( 
    {
        'name': 'Carlos Borjes',
    'username': 'Barlitos',
    'email': 'carlosB@jbu.edu',
    'password': '1234567',
    'zip-code': '72761',
    'points': 0
    }) 