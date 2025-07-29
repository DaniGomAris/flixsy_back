import firebase_admin
from firebase_admin import credentials, firestore

# Route to downloaded file
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()