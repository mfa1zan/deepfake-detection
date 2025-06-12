import torch
import torchvision.transforms as transforms
from torchvision.models import resnet18
from PIL import Image
import os
import time


import uploaded_video as uv
# Flask imports


from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

model = resnet18(pretrained=True)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(f"File saved to {filepath}")
        return jsonify({'success': True, 'filename': filename})

    return jsonify({'success': False, 'error': 'Invalid file type'})

@app.route('/detect', methods=['POST'])
def detect():
    data = request.get_json()
    filename = data.get('filename')

    if not filename:
        return jsonify({'success': False, 'error': 'Filename not provided'})

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(filepath):
        return jsonify({'success': False, 'error': 'File not found'})

    if filename.lower().endswith(('mp4', 'avi', 'mov')):
        landmarks = uv.extract_all_landmarks(filepath)
        chunks = uv.split_into_chunks(landmarks, chunk_size=150)
        label, confidence, pred = uv.predict_deepfake(chunks)
        result = f"Video detected as: {label}" #(Confidence: {confidence:.2f})
        return jsonify({
            'success': True,
            'result': f"Video detected as: {label}",
            'label': label,  
            'confidence': confidence,
            'softmax': pred
        })

    return jsonify({'success': True, 'result': result})

if __name__ == '__main__':
    app.run(debug=True)
