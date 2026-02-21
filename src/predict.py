import tensorflow as tf
import numpy as np
import cv2
from tensorflow.keras.applications.resnet50 import preprocess_input


IMG_SIZE = 224
CLASS_NAMES = ["NORMAL", "PNEUMONIA"]


print("Loading trained model...")
model = tf.keras.models.load_model("artifacts/best_model.keras")



def preprocess_image(image_path):

    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("❌ Image path is wrong!")

    # BGR → RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # resize to model input size
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

    # ⭐ IMPORTANT: ResNet50 preprocessing
    img = preprocess_input(img)

    # add batch dimension
    img = np.expand_dims(img, axis=0)

    return img



def predict(image_path):

    processed_img = preprocess_image(image_path)

    preds = model.predict(processed_img, verbose=0)

    class_index = np.argmax(preds[0])
    confidence = float(preds[0][class_index])

    print("\n✅ Prediction:", CLASS_NAMES[class_index])
    print("✅ Confidence:", confidence)



if __name__ == "__main__":

    # change image here to test
    image_path = "data/raw/test/PNEUMONIA/person1_virus_9.jpeg"

    predict(image_path)
