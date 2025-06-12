# 🎭 Deepfake Video Detection Using CNN-LSTM

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.0+-orange.svg)](https://tensorflow.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A sophisticated deepfake video detection system powered by CNN-LSTM neural networks that analyzes facial landmarks to classify videos as real or fake with high accuracy.

## 🎯 Overview

This project implements a state-of-the-art deepfake detection system that:

- 🔍 Extracts facial landmarks from videos using dlib
- 🧠 Employs CNN-LSTM architecture for spatial-temporal analysis
- 🌐 Provides a user-friendly Flask web interface
- ⚡ Delivers real-time predictions with confidence scores

## 🗄️ Dataset

**Source:** [FaceForensics++](https://github.com/ondyari/FaceForensics) dataset

### Dataset Details:

- 📊 **Total Videos:** 2,000 (1,000 real + 1,000 fake)
- 🎯 **Training:** 70% (1,400 videos)
- 🧪 **Testing:** 20% (400 videos)
- ✅ **Validation:** 10% (200 videos)

> **Note:** Request access via the [FaceForensics++ website](https://github.com/ondyari/FaceForensics) and download using their provided script.

## 🔄 Project Workflow

### 1. 📁 Data Preparation

- Extract 68 facial landmarks from each video frame
- Save landmarks as `.npy` files for efficient processing
- Normalize landmark data for optimal model performance

### 2. 🏋️ Model Training

- Utilize CNN-LSTM architecture for spatial-temporal feature learning
- Train on normalized landmark sequences
- Validate performance on held-out validation set

### 3. 🎯 Prediction Pipeline

- Upload video via intuitive web interface
- Real-time facial landmark extraction and normalization
- Generate prediction with confidence scores

## 📁 Repository Structure

```
Flask_app/
│
├── 🐍 app.py                    # Flask application main file
├── 🎬 uploaded_video.py         # Video processing and prediction logic
├── 📋 requirements.txt          # Project dependencies
├── 📖 README.md                 # Project documentation
│
├── 🤖 models/                   # Model weights and data
│   ├── deepfake_landmark_lstm_cnn_model.h5
│   ├── min_val.npy
│   ├── max_val.npy
│   └── shape_predictor_68_face_landmarks.dat
│
├── 🎨 static/                   # Static web assets
│   ├── css/                     # Stylesheets
│   ├── js/                      # JavaScript files
│   ├── images/                  # Image assets
│   └── uploads/                 # Uploaded video storage
│
└── 📄 templates/                # HTML templates
    └── index.html
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/mfa1zan/deepfake-detection.git
   cd deepfake-detection
   ```

2. **Set up virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download model files**

   - Place your trained model files (`.h5`, `.npy`, `.dat`) in the `models/` directory
   - Contact the repository maintainer for access to pre-trained models

5. **Run the application**

   ```bash
   python3 app.py
   ```

6. **Access the web interface**
   - Open your browser and navigate to `http://127.0.0.1:5000`
   - Upload a video and get instant deepfake detection results!

## 🎮 Usage

1. **Upload Video:** Select an MP4, AVI, or MOV file
2. **Processing:** The system extracts facial landmarks automatically
3. **Detection:** Get real-time classification results
4. **Results:** View prediction labels, confidence scores, and detailed analysis

## 🔧 API Endpoints

| Endpoint  | Method | Description                 |
| --------- | ------ | --------------------------- |
| `/`       | GET    | Main web interface          |
| `/upload` | POST   | Upload video file           |
| `/detect` | POST   | Process and detect deepfake |

## 📊 Model Performance

- **Architecture:** CNN-LSTM hybrid network
- **Input:** Normalized facial landmark sequences
- **Output:** Binary classification (Real/Fake) with confidence scores
- **Features:** Temporal consistency analysis across video frames

## ⚠️ Important Notes

- 📦 Model files (`.h5`, `.npy`) are excluded from the repository due to size constraints
- 🔗 Contact the maintainer for access to pre-trained models
- 📚 Training notebooks and preprocessing scripts available upon request
- 🎯 Supports common video formats: MP4, AVI, MOV

> **Note:** This detector was developed and trained on my local machine, so results may not be state-of-the-art or perfect. Use accordingly.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- **Dataset:** [FaceForensics++](https://github.com/ondyari/FaceForensics) team
- **Landmark Detection:** [dlib](http://dlib.net/) shape predictor
- **Deep Learning:** [TensorFlow](https://tensorflow.org/) and [Keras](https://keras.io/)
- **Web Framework:** [Flask](https://flask.palletsprojects.com/)

## 📞 Contact

For questions, suggestions, or collaboration opportunities, please reach out:

- 📧 Email: me.faizan25@gmail.com
- 💼 LinkedIn: https://www.linkedin.com/in/muhammad-faizan-ba5587316/
- 🐙 GitHub: https://github.com/mfa1zan

---

⭐ **Star this repository if you found it helpful!** ⭐
