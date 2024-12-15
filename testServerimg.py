import requests

url = "http://127.0.0.1:5000/detect"
files = {'image': open('bus.jpg', 'rb')}
response = requests.post(url, files=files)

# Salva l'immagine restituita
if response.status_code == 200:
    with open("detected_image.jpg", "wb") as f:
        f.write(response.content)
else:
    print("Errore:", response.json())