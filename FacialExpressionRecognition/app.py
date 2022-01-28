from flask import Flask, render_template, Response, request, jsonify
import werkzeug
import os, shutil

import cv2
from model import FacialExpressionModel
import numpy as np

facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = FacialExpressionModel("model.json", "model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX
image_path = ""

app = Flask(__name__)



@app.route('/', methods=['GET','POST'])
def index():
    return "emotion flask server connected"


@app.route('/lol', methods=['POST'])
def index_lol():
    i = int(request.form.get('sent'))
    return str(i * i)

@app.route('/predict_emotion', methods=['POST'])
def get_emotion_prediction():
    cleanse_uploaded_directory()
    for key in request.files:
        read_and_save_file(key)

    prediction = get_emotion()
    return prediction

def get_emotion():
    print("PATH IS " + image_path)
    fr = cv2.imread(image_path)
    gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    faces = facec.detectMultiScale(gray_fr, 1.3, 5)
    for (x, y, w, h) in faces:
        fc = gray_fr[y:y+h, x:x+w]

        roi = cv2.resize(fc, (48, 48))
        pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])
    return pred

def read_and_save_file(file_key):
    imagefile = request.files[file_key]
    filename = werkzeug.utils.secure_filename(imagefile.filename)
    global image_path 
    image_path = "uploaded/" + filename
    print('Received image File name : ' + imagefile.filename)
    imagefile.save('uploaded/' + filename)  # save file to uploaded folder

def cleanse_uploaded_directory():
    folder = 'uploaded'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)