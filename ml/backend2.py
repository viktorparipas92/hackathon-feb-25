from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from slash import text_response_V0  # your functions
import logging, os

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
    return render_template("index2.html")

@app.route("/process_text", methods=["POST"])
def process_text_route():
    app.logger.debug("Received request at /process_text")
    data = request.get_json()
    question = data.get("text", "")
    response = text_response_V0(question)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)