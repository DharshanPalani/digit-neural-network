import pickle
import numpy as np
from sklearn.neural_network import MLPClassifier
from data_handler import load_training_data

def train_model(folder, model_filename="digit_model.pkl"):
    X, y = load_training_data(folder)
    if len(X) == 0:
        return None
    model = MLPClassifier(hidden_layer_sizes=(128, 64), activation='relu', solver='adam', max_iter=500)
    model.fit(X, y)
    with open(model_filename, 'wb') as f:
        pickle.dump(model, f)
    return model

def predict_digit(image, model):
    pixel_values = np.array(image).reshape(1, -1) / 255.0
    return model.predict(pixel_values)[0]
