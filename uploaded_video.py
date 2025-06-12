import os,cv2, dlib, numpy as np
from tensorflow.keras.models import load_model
detector = dlib.get_frontal_face_detector()

MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'deepfake_landmark_lstm_cnn_model.h5')
SHAPE_PREDICTOR_PATH = os.path.join(MODELS_DIR, 'shape_predictor_68_face_landmarks.dat')
MIN_VAL_PATH = os.path.join(MODELS_DIR, 'min_val.npy')
MAX_VAL_PATH = os.path.join(MODELS_DIR, 'max_val.npy')
predictor = dlib.shape_predictor(SHAPE_PREDICTOR_PATH)

def extract_all_landmarks(video_path, target_fps=10):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or target_fps
    step = max(1, int(round(fps / target_fps)))

    landmarks = []
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % step == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            dets = detector(gray, 1)
            if dets:
                shape = predictor(gray, dets[0])
                coords = [(p.x, p.y) for p in shape.parts()]
                landmarks.append(coords)
        idx += 1
    cap.release()
    return np.array(landmarks) 

def split_into_chunks(landmarks_array, chunk_size=150):
    total = landmarks_array.shape[0]
    chunks = []
    for start in range(0, total, chunk_size):
        end = min(start + chunk_size, total)
        chunk = landmarks_array[start:end]
        # Pad if needed
        if chunk.shape[0] < chunk_size:
            if chunk.shape[0] == 0:
                chunk = np.zeros((chunk_size, 68, 2))
            else:
                pad_count = chunk_size - chunk.shape[0]
                chunk = np.concatenate([chunk, np.repeat(chunk[-1][np.newaxis, :, :], pad_count, axis=0)], axis=0)
        chunks.append(chunk)
    return chunks

# def predict_deepfake(landmarks_chunks):
#     # Load normalization values and model
#     min_val = np.load(MIN_VAL_PATH)
#     max_val = np.load(MAX_VAL_PATH)
    
#     model_lstm = load_model(MODEL_PATH)

#     # Use the first chunk for prediction (or loop over all if needed)
#     chunk = landmarks_chunks[0]
#     chunk_norm = (chunk - min_val) / (max_val - min_val + 1e-8)
#     chunk_input = chunk_norm.reshape(1, 150, 136)

#     # Predict
#     pred = model_lstm.predict(chunk_input)
#     label = np.argmax(pred)
#     confidence = float(np.max(pred))
#     classes = ['Real', 'Fake']

#     print(f"Video-level Prediction: {classes[label]} (Confidence: {confidence:.2f})")
#     print("Chunk softmax prediction:", pred)

#     return classes[label], confidence, pred.tolist()



def predict_deepfake(landmarks_chunks):
    # Load normalization values and model
    min_val = np.load(MIN_VAL_PATH)
    max_val = np.load(MAX_VAL_PATH)
    model_lstm = load_model(MODEL_PATH)

    classes = ['Real', 'Fake']
    fake_found = False
    max_confidence = 0.0
    all_softmax = []
    
    for idx, chunk in enumerate(landmarks_chunks):
        chunk_norm = (chunk - min_val) / (max_val - min_val + 1e-8)
        chunk_input = chunk_norm.reshape(1, 150, 136)
        pred = model_lstm.predict(chunk_input)
        label = np.argmax(pred)
        confidence = float(np.max(pred))
        all_softmax.append(pred.tolist()[0])
        print(f"Chunk {idx+1}: {classes[label]} (Confidence: {confidence:.2f}) - Softmax: {pred.tolist()}")

        
        if confidence > max_confidence:
            max_confidence = confidence

        if label == 1:  # Fake detected
            fake_found = True

    # Video-level decision
    if fake_found:
        print("Video-level Prediction: Fake (at least one chunk detected as fake)")
        video_pred = 'Fake'
    else:
        print("Video-level Prediction: Real (all chunks detected as real)")
        video_pred = 'Real'

    return video_pred, max_confidence, all_softmax