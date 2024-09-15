import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import json
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


class FoodClassifier:
    def __init__(self, model_path, mapping_path):
        # Load the model
        self.model = tf.keras.models.load_model(model_path)
        
        # Load the mapping
        with open(mapping_path) as f:
            self.food_to_broad_category = json.load(f)

    def preprocess_image(self, img):
        """Preprocess the image for the model."""
        img = img.resize((224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
        return img_array

    def load_image(self, image_path):
        """Load the image from a local path or URL."""
        if image_path.startswith("http://") or image_path.startswith("https://"):
            # If the input is a URL, download the image
            response = requests.get(image_path)
            img = Image.open(BytesIO(response.content))
        elif os.path.exists(image_path):
            # If it's a file path, load from disk
            img = Image.open(image_path)
        else:
            raise ValueError(f"Invalid image path or URL: {image_path}")
        return img

    def predict_and_map_class(self, image_path):
        """Predict and map the class to a broad category."""
        img = self.load_image(image_path)
        img_array = self.preprocess_image(img)
        predictions = self.model.predict(img_array)
        predicted_class_index = np.argmax(predictions[0])
        
        # Assuming the model's class indices match the keys in the mapping
        class_names = list(self.food_to_broad_category.keys())
        predicted_class = class_names[predicted_class_index]
        
        # Get the broad categories
        broad_categories = self.food_to_broad_category.get(predicted_class, ["Unknown"])
        
        return predicted_class, broad_categories


# # Example usage:
# if __name__ == "__main__":
#     # Initialize the classifier with model and mapping paths
#     classifier = FoodClassifier(model_path="path/to/your/model.h5", mapping_path="path/to/your/mapping.json")
    
#     # Predict using a local image or an image URL
#     image_path = "path/to/your/image.jpg"  # Can be a local file or URL
#     predicted_class, broad_categories = classifier.predict_and_map_class(image_path)
    
#     print(f"Predicted Class: {predicted_class}")
#     print(f"Broad Categories: {broad_categories}")
