from flask import Flask, request, render_template, jsonify
from keras_preprocessing import image
from keras.models import load_model
from keras.applications.vgg16 import preprocess_input
import numpy as np
import os

app = Flask(__name__)

# Load the trained model
model = load_model('our_model.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    img = request.files['file']
    img_path = os.path.join('uploads', img.filename)
    img.save(img_path)

    img = image.load_img(img_path, target_size=(224, 224))
    image_array = image.img_to_array(img)
    image_array = np.expand_dims(image_array, axis=0)
    img_data = preprocess_input(image_array)
    prediction = model.predict(img_data)

    result = 'Person is safe.' if prediction[0][0] > prediction[0][1] else 'Person is affected with Pneumonia.'
    
    return jsonify({'result': result})

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
