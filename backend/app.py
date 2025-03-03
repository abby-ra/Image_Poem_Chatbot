import os
import json
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
# from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Load API Key from .env file
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
api_key = "AIzaSyDmRfCf_5Y3gSDSIqmo4Jy3bVcRRWS497g"

# if not api_key:
    # raise ValueError("API key is missing! Set GEMINI_API_KEY in your .env file.")

genai.configure(api_key=api_key)

# Ensure 'static' directory exists for saving images
os.makedirs("static", exist_ok=True)

@app.route("/generate_poem", methods=["POST"])
def generate_poem():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files["image"]
    image_path = os.path.join("static", image_file.filename)
    image_file.save(image_path)

    # Load image
    image = Image.open(image_path)
    image = Image.open(image_path).convert("RGB")

    # Get the Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Generate a poem
    response = model.generate_content(["Write a poem based on this image with poem structure.", image])

    # Save poem to JSON
    poem_data = {"text": response.text}
    #poem_data = {"text": response._result.candidates[0]['content']}  # Adjust if necessary

    with open("data.json", "w") as json_file:
        json.dump(poem_data, json_file, indent=4)

    return jsonify(poem_data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)