import sys
import os

# Agregar el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.firestore_initiator import db

def test_firestore():
    try:
        docs = db.collection('test').stream()
        print("Firestore conectado. Documentos:")
        for doc in docs:
            print(f"{doc.id} => {doc.to_dict()}")
    except Exception as e:
        print(f"Error conectando a Firestore: {e}")

if __name__ == "__main__":
    test_firestore()
