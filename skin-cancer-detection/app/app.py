from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
import cv2
from sklearn.pipeline import Pipeline
import os
from modules.preprocess import Resize, GaussianBlur, CLAHE_Color, Normalize, show_images
from modules.heatmap import saliency_map, visualize_saliency
import base64
from io import BytesIO
from tensorflow import keras


app = Flask(__name__)

model = keras.models.load_model('static/model/skin_cancer.keras')
preprocess_pipeline = Pipeline([
    ('resize', Resize((64, 64))),
    ('blur', GaussianBlur()),
    ('clahe', CLAHE_Color()),
    ('normalize', Normalize(scaling='minmax'))
])

def preprocess_and_load_image(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            return None
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        processed_img = preprocess_pipeline.transform([img_rgb])[0]
        return img_rgb, processed_img
    except Exception as e:
        print(f"Erro ao pré-processar/carregar imagem: {e}")
        return None, None

# Rota para exibir a página HTML
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    if file:
        try:
            file_path = 'ISIC_0052003.jpg'
            file.save(file_path)
            original_image, processed_image = preprocess_and_load_image(file_path)
            os.remove(file_path)

            if processed_image is None:
                return render_template('index.html', error='Erro ao pré-processar a imagem')

            prediction = model.predict(np.expand_dims(processed_image, axis=0))
            probability = prediction[0][0]
            class_label = "maligno" if probability > 0.5 else "benigno"

            # Gerar o mapa de saliência
            saliency = saliency_map(model, processed_image)

            # Visualizar o mapa de saliência sobre a imagem original
            saliency_overlayed = visualize_saliency(original_image, saliency)

            # Codificar a imagem com o mapa de saliência para base64
            _, img_encoded = cv2.imencode('.jpg', saliency_overlayed)
            base64_image = base64.b64encode(img_encoded).decode('utf-8')

            return render_template('index.html',
                                   prediction={'probability': float(probability), 'class': class_label},
                                   saliency_image=base64_image)
        
        except Exception as e:
            return render_template('index.html', error=f'Erro ao processar a requisição: {e}')

    return render_template('index.html', error='Erro desconhecido')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')