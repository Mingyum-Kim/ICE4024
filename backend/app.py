import os
import cv2
import numpy as np
import pickle
import torch
from torchvision import transforms
from PIL import Image
from werkzeug.utils import secure_filename

# Keras
from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img

# Flask utils
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# loading model
MODEL_PATH = 'models/aram_model1.pt'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.load(MODEL_PATH, map_location=device)
model.eval()

# Image preprocessing transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def preprocess_image(image):
    img = Image.open(image).convert("RGB")
    img = transform(img)
    img = img.unsqueeze(0)
    return img

# download image
DOWNLOAD_FOLDER = 'uploads'
@app.route('/predict', methods=['POST'])
def upload(): 
    # 클라이언트로부터 이미지를 받아와 서버에 저장
    file = request.files['file']

    # 서버에 이미지 파일 저장
    filename = secure_filename(file.filename)
    file.save(os.path.join(DOWNLOAD_FOLDER, filename))
    
    input_image = preprocess_image(file)
    with torch.no_grad():
        input_image = input_image.to(device)
        output = model(input_image)
    
    _, predicted_class = torch.max(output, 1)
    result = int(predicted_class.item())
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)