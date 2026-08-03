from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
from io import BytesIO
import base64

# Import our preprocessing function
from utils import preprocess_image

app = Flask(__name__)

# Load trained model
model = tf.keras.models.load_model("mnist_cnn.keras")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    data = request.json["image"]

    # Remove base64 header
    data = data.split(",")[1]

    image = Image.open(
        BytesIO(base64.b64decode(data))
    ).convert("L")

    # Convert to numpy array
    image = np.array(image)

    # Professional preprocessing
    image = preprocess_image(image)

    # Prediction
    prediction = model.predict(image, verbose=0)

    digit = int(np.argmax(prediction))

    confidence = float(np.max(prediction) * 100)

    return jsonify({
        "digit": digit,
        "confidence": round(confidence, 2)
    })


if __name__ == "__main__":
    app.run(debug=True)