import base64

def convert_to_base64(filepath):
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode()

if __name__ == "__main__":
    filepath = "google_credentials.json"
    encoded = convert_to_base64(filepath)
    with open("encoded_google_credentials.txt", "w") as f:
        f.write(encoded)
    print("Archivo codificado guardado en encoded_google_credentials.txt")
