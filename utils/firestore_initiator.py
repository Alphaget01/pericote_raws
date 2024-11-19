import firebase_admin
from firebase_admin import credentials, firestore
import os
import base64
import json

# Inicialización de Firebase
def init_firestore():
    if not firebase_admin._apps:  # Evitar múltiples inicializaciones
        encoded_creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_BASE64")
        creds_json = base64.b64decode(encoded_creds)
        creds_dict = json.loads(creds_json)

        cred = credentials.Certificate(creds_dict)
        firebase_admin.initialize_app(cred)

    return firestore.client()  # Retornar el cliente Firestore

# Inicialización global del cliente Firestore
db = init_firestore()
