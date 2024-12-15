from flask import Flask, request, send_file
import torch
import os
import io
from PIL import Image

# Inizializza il modello YOLOv5
model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # or yolov5n - yolov5x6, custom

app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def detect_objects():
    try:
        # Controlla se il file è stato inviato
        if 'image' not in request.files:
            return {"error": "No image file provided"}, 400

        # Legge l'immagine inviata dal client
        file = request.files['image']
        image = Image.open(file.stream)  # Carica l'immagine in formato PIL

        # Inference con YOLOv5
        results = model(image)

        # Salva l'immagine elaborata in memoria
        results_dir = "runs/detect/exp"  # YOLOv5 salva qui per default
        results.save()  # Salva l'immagine con i rilevamenti

        # Trova l'immagine salvata da YOLOv5
        detected_image_path = os.path.join(results_dir, os.listdir(results_dir)[0])

        # Invia l'immagine come risposta
        return send_file(detected_image_path, mimetype="image/png")

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
