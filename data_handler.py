import os
from PIL import Image
import numpy as np


def save_training_image(image, digit, folder):
    os.makedirs(folder, exist_ok=True)
    resized_image = image.resize((28, 28))
    file_name = os.path.join(folder, f"{digit}_{np.random.randint(10000)}.png")
    resized_image.save(file_name)


def load_training_data(folder):
    X, y = [], []
    for file_name in os.listdir(folder):
        if file_name.endswith(".png"):
            label = int(file_name.split("_")[0])
            image_path = os.path.join(folder, file_name)
            image = Image.open(image_path).convert("L").resize((28, 28))
            X.append(np.array(image).flatten() / 255.0)
            y.append(label)
    return np.array(X), np.array(y)
