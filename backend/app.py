import os
import cv2
import numpy as np
import pickle

# Keras
from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img

# Flask utils
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load model
MODEL_PATH = './backend/models/model.h5'
model = load_model(MODEL_PATH)
model.make_predict_function()

PKL_PATH = './backend/models/label_encoder.pkl'
with open(PKL_PATH, 'rb') as f: 
    label_encoder = pickle.load(f)

def model_predict(img_path, model):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (224, 224))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0

    preds = model.predict(img)
    return preds

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']

        # Save the file
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)

        # Process the result
        pred_class = np.argmax(preds)
        class_label = label_encoder.inverse_transform([pred_class])
        result = "Predicted class : " + class_label[0]
        return result
    return None

if __name__ == '__main__':
    app.run(debug=True)