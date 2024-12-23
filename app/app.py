from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image
import os

app = Flask(__name__)

# Load the trained model
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flower_classifier_model.h5')
model = load_model(model_path)

# Define class labels
class_labels = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']

@app.route('/')
def index():
    """Render the main HTML page."""
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    """Handle file upload and make predictions."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Preprocess the image
        image = Image.open(file)
        if image.mode != 'RGB':
            image = image.convert('RGB')  # Ensure the image is in RGB format
        image = image.resize((240, 240))  # Resize to match the model's input size
        image = img_to_array(image) / 255.0  # Normalize the pixel values to [0, 1]
        image = np.expand_dims(image, axis=0)  # Add batch dimension

        # Make a prediction
        predictions = model.predict(image)
        predicted_index = np.argmax(predictions)
        confidence = np.max(predictions)
        predicted_class = class_labels[predicted_index]

        return jsonify({'class': predicted_class, 'confidence': float(confidence)})

    except IOError:
        return jsonify({'error': 'Invalid or corrupted image file. Please upload a valid image.'}), 400
    except Exception as e:
        return jsonify({'error': 'Error processing the image: ' + str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
