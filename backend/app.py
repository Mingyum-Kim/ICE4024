from io import BytesIO
import os
import cv2
import numpy as np
import pickle

# torch
import torch
from torch.utils.data import Dataset, DataLoader
import torchvision
from torchvision import transforms

# flask utils
from flask import Flask, request, render_template, jsonify, send_file
from werkzeug.utils import secure_filename
from PIL import Image
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# loading model
MODEL1_PATH = 'models/aram_model1.pt'
MODEL2_PATH = 'models/aram_model2.pt'
MODEL3_PATH = 'models/aram_model3.pt'
MODEL4_PATH = 'models/aram_model4.pt'
MODEL5_PATH = 'models/aram_model5.pt'
MODEL6_PATH = 'models/aram_model6.pt'

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model1 = torch.load(MODEL1_PATH, map_location=device)
model1.eval()

model2 = torch.load(MODEL2_PATH, map_location=device)
model2.eval()

model3 = torch.load(MODEL3_PATH, map_location=device)
model3.eval()

model4 = torch.load(MODEL4_PATH, map_location=device)
model4.eval()

model5 = torch.load(MODEL5_PATH, map_location=device)
model5.eval()

model6 = torch.load(MODEL6_PATH, map_location=device)
model6.eval()

# Image preprocessing transformation to tensor
preprocess = transforms.Compose([  transforms.Resize([int(600), int(600)], interpolation=transforms.InterpolationMode.BOX),
                                            transforms.ToTensor(),
                                            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])    ])

def predict_image(file):
    # Open the image
    image = Image.open(file)

    # Preprocess the image
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)

    # Make prediction
    with torch.no_grad():
        output1 = model1.forward(input_batch)
        output2 = model2.forward(input_batch)
        output3 = model3.forward(input_batch)
        output4 = model4.forward(input_batch)
        output5 = model5.forward(input_batch)
        output6 = model6.forward(input_batch)

    # Get the predicted class
    _, predicted_class1 = torch.max(output1, 1)
    _, predicted_class2 = torch.max(output2, 1)
    _, predicted_class3 = torch.max(output3, 1)
    _, predicted_class4 = torch.max(output4, 1)
    _, predicted_class5 = torch.max(output5, 1)
    _, predicted_class6 = torch.max(output6, 1)

    print("predicted_class1 : ", predicted_class1.item())
    print("predicted_class2 : ", predicted_class2.item())
    print("predicted_class3 : ", predicted_class3.item())
    print("predicted_class4 : ", predicted_class4.item())
    print("predicted_class5 : ", predicted_class5.item())
    print("predicted_class6 : ", predicted_class6.item())

    return [predicted_class1.item(), predicted_class2.item(), predicted_class3.item(), predicted_class4.item(), predicted_class5.item(), predicted_class6.item()]

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get the image from the request
            file = request.files['file']
            
            # Make prediction
            prediction = predict_image(file)

            response = {
                '미세각질': prediction[0],
                '피지과다': prediction[1],
                '모낭사이홍반': prediction[2],
                '모낭홍반/농포': prediction[3],
                '비듬': prediction[4],
                '탈모': prediction[5]
            }
            return jsonify(response)
        except Exception as e:
            print("error occurred  : ", str(e))
            return jsonify({'error': str(e)})

# get image to client
@app.route('/image', methods=['GET'])
def get_image():
    image_name = request.args.to_dict()['name']
    image_path = os.path.join(DOWNLOAD_FOLDER, image_name)
    return send_file(image_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)