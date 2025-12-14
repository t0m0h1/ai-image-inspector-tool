from flask import Flask, request, jsonify, render_template
import os

from utils.exif_utils import extract_exif
from utils.vision_utils import analyse_image
from utils.insight_engine import generate_insights


UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# -----------------------
# Routes
# -----------------------

@app.route("/")
def index():
    """
    Main UI page (JS-driven)
    """
    return render_template("index.html")


@app.route("/api/upload", methods=["POST"])
def upload_image():
    """
    Uploads an image and returns analysis results as JSON
    """
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # ---- AI Pipeline ----
    exif_data = extract_exif(filepath)
    detections = analyse_image(filepath)
    insights = generate_insights(detections, exif_data)

    return jsonify({
        "success": True,
        "filename": file.filename,
        "image_url": f"/static/uploads/{file.filename}",
        "exif": exif_data,
        "detections": detections,
        "insights": insights
    })


@app.route("/api/delete/<filename>", methods=["DELETE"])
def delete_image(filename):
    """
    Deletes an uploaded image (API endpoint)
    """
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    os.remove(filepath)

    return jsonify({
        "success": True,
        "message": "Image deleted successfully"
    })


# -----------------------
# App Entry Point
# -----------------------

if __name__ == "__main__":
    app.run(debug=True)
