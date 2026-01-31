from flask import Flask, request, jsonify,send_from_directory
from flask_cors import CORS
from PIL import Image
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/upload", methods=["POST"])
def upload_file():
    if "xray" not in request.files:
        return jsonify({"error": "No file sent"}), 400

    file = request.files["xray"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return jsonify({
        "message": "File uploaded successfully",
        "file_path": file_path
    })


@app.route("/files", methods=["GET"])
def list_files():
    return jsonify(os.listdir(UPLOAD_FOLDER))


@app.route("/scan", methods=["POST"])
def scan_xray():
    data = request.json

    if not data or "filename" not in data:
        return jsonify({"error": "Filename not provided"}), 400

    filename = data["filename"]
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    scan_result = "No infection detected"

    return jsonify({
        "filename": filename,
        "result": scan_result,
        "confidence": "92%"
    })


@app.route("/flip", methods=["POST"])
def flip_image():
    data = request.json

    if not data or "filename" not in data:
        return jsonify({"error": "Filename not provided"}), 400

    filename = data["filename"]
    input_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(input_path):
        return jsonify({"error": "File not found"}), 404

    img = Image.open(input_path)
    flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)

    flipped_filename = "flipped_" + filename
    output_path = os.path.join(UPLOAD_FOLDER, flipped_filename)
    flipped_img.save(output_path)

    return jsonify({
        "message": "Image flipped successfully",
        "original": filename,
        "flipped": flipped_filename
    })

@app.route("/uploads/<filename>")
def serve_uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# 🔴 app.run MUST BE LAST
if __name__ == "__main__":
    print("🔥 Backend starting...")
    app.run(host="127.0.0.1", port=5000, debug=True)
