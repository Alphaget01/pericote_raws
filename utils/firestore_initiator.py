import firebase_admin
from firebase_admin import credentials, firestore
import os
import base64
import json

def init_firestore():
    """
    Inicializa y retorna el cliente de Firestore.
    Usa credenciales codificadas en base64 desde una variable de entorno.
    """
    # Verifica si Firebase ya fue inicializado
    if not firebase_admin._apps:
        # Obtén las credenciales codificadas desde la variable de entorno
        encoded_creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_BASE64")
        
        if not encoded_creds:
            raise EnvironmentError("La variable GOOGLE_APPLICATION_CREDENTIALS_BASE64 no está configurada.")

        # Decodifica las credenciales de base64 a JSON
        creds_json = base64.b64decode(encoded_creds).decode("utf-8")
        
        try:
            creds_dict = json.loads(creds_json)  # Convierte el JSON a un diccionario
        except json.JSONDecodeError as e:
            raise ValueError("Las credenciales decodificadas no son JSON válido.") from e

        # Crea las credenciales y inicializa la aplicación Firebase
        cred = credentials.Certificate(creds_dict)
        firebase_admin.initialize_app(cred)

    # Retorna el cliente Firestore
    return firestore.client()

# Inicialización global del cliente Firestore
try:
    db = init_firestore()
except Exception as e:
    raise RuntimeError(f"Error al inicializar Firestore: {e}")
