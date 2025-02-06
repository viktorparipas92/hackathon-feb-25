from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from slash import text_response_V0 
from slash_img import process_image  # your functions
import logging,os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# run huggingface-cli login --token
cmd = "huggingface-cli login --token XXX"
os.system(cmd)
import torch
torch.cuda.empty_cache()



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    app.logger.debug("Received request at /chat")
    if "image" in request.files:
        app.logger.debug("Processing image")
        # Get the image file and save it temporarily (or process in memory)
        image_file = request.files["image"]
        image_path = "./temp_image.jpg"
        image_file.save(image_path)
        # Optionally use any accompanying text context (e.g., request.form.get("text"))
        response = process_image(image_path)
    else:
        app.logger.debug("Processing text")
        data = request.get_json()
        question = data.get("text", "")
        response = text_response_V0(question)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)