from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename
import uuid
import stat

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "private_uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

    files = request.files.getlist("photo")

    saved_files = []
    for file in files:
        if file.filename == "":
            continue
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit(".", 1)[1].lower()
            unique_name = f"{uuid.uuid4()}.{ext}"
            filename = secure_filename(unique_name)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            os.chmod(filepath, stat.S_IRUSR | stat.S_IWUSR)  # Owner read/write
            saved_files.append(filename)

    if not saved_files:
        return "No valid files uploaded.", 400

    return render_template("thank_you.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
