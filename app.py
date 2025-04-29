from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Folder to store uploaded files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "photo" not in request.files:
        return "No file part", 400
    file = request.files["photo"]
    if file.filename == "":
        return "No selected file", 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return "Thank you for uploading your photo!"
    else:
        return "Invalid file type. Only PNG, JPG, and JPEG are allowed.", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
